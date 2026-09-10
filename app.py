"""EZ-DLP — local Windows app to download MP4 and MP3."""

from __future__ import annotations

import json
import os
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import urllib.request
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk

YTDLP_URLS = (
    "https://github.com/yt-dlp/yt-dlp-nightly-builds/releases/latest/download/yt-dlp.exe",
    "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe",
)
YTDLP_MAX_AGE = timedelta(hours=24)
FFMPEG_ZIPS = (
    "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
    "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
)
UA = "Mozilla/5.0 EZ-DLP/1.0"

BG = "#111318"
SURFACE = "#1a1d24"
BORDER = "#2c313c"
TEXT = "#e8eaed"
MUTED = "#9aa0a6"
MP4 = "#c62828"
MP4_HOVER = "#e53935"
MP3 = "#1565c0"
MP3_HOVER = "#1e88e5"
BTN_FG = "#ffffff"
ENTRY_BG = "#0d0f14"
LOG_BG = "#0d0f14"
OK = "#66bb6a"
ERR = "#ef5350"
ACCENT = "#8ab4f8"


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def asset_path(*parts: str) -> Path | None:
    roots: list[Path] = []
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        roots.append(Path(meipass))
    roots.append(app_dir())
    for root in roots:
        path = root.joinpath(*parts)
        if path.is_file():
            return path
    return None


def load_photo(name: str, master: tk.Misc) -> tk.PhotoImage | None:
    path = asset_path("assets", name)
    if path is None:
        return None
    try:
        return tk.PhotoImage(file=str(path), master=master)
    except tk.TclError:
        return None


def config_path() -> Path:
    return app_dir() / "config.json"


def tools_dir() -> Path:
    return app_dir() / "tools"


def factory_output_dir() -> Path:
    downloads = Path.home() / "Downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    return downloads


def load_output_dir() -> Path:
    path = config_path()
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            saved = Path(str(data.get("output_dir", "")).strip())
            if saved and saved.is_dir():
                return saved
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            pass
    default = factory_output_dir()
    default.mkdir(parents=True, exist_ok=True)
    return default


def save_output_dir(folder: Path) -> None:
    folder = folder.expanduser()
    try:
        config_path().write_text(
            json.dumps({"output_dir": str(folder)}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError:
        pass


def find_cookies(ytdlp: Path) -> Path | None:
    candidates = [
        app_dir() / "cookies.txt",
        tools_dir() / "cookies.txt",
        ytdlp.parent / "cookies.txt",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def locate_ffmpeg_dir() -> Path | None:
    local = tools_dir() / "ffmpeg.exe"
    if local.is_file():
        return local.parent
    found = shutil.which("ffmpeg")
    if found:
        return Path(found).resolve().parent
    return None


def _is_stale(path: Path) -> bool:
    if not path.is_file():
        return True
    age = datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)
    return age > YTDLP_MAX_AGE


def _clear_ytdlp_cache(ytdlp: Path) -> None:
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    subprocess.run(
        [str(ytdlp), "--rm-cache-dir"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=flags,
    )


def is_youtube(url: str) -> bool:
    text = url.lower()
    return "youtube.com" in text or "youtu.be" in text or "youtube-nocookie.com" in text


def parse_timestamp(raw: str) -> tuple[int | None, bool]:
    """Parse hh:mm:ss, mm:ss, 00:ss, or ss. Empty = (None, True)."""
    text = (raw or "").strip().replace(" ", "")
    if not text:
        return None, True
    parts = text.split(":")
    if not (1 <= len(parts) <= 3) or any(p == "" or not p.isdigit() for p in parts):
        return None, False
    nums = [int(p) for p in parts]
    if len(nums) == 1:
        hours, minutes, seconds = 0, 0, nums[0]
    elif len(nums) == 2:
        hours, minutes, seconds = 0, nums[0], nums[1]
    else:
        hours, minutes, seconds = nums
    if minutes > 59 or seconds > 59 or hours < 0:
        return None, False
    return hours * 3600 + minutes * 60 + seconds, True


def format_hms(total: int) -> str:
    hours, rem = divmod(total, 3600)
    minutes, seconds = divmod(rem, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


def resolve_section(start_raw: str, end_raw: str) -> tuple[str | None, str | None]:
    """Return (yt-dlp spec or None, optional note). None spec = full video."""
    start, start_ok = parse_timestamp(start_raw)
    end, end_ok = parse_timestamp(end_raw)
    if not start_ok or not end_ok:
        return None, "Invalid timestamp — downloading the full video."
    if start is None and end is None:
        return None, None
    if start is None:
        start = 0
    if end is not None and start >= end:
        return None, "Invalid timestamp — downloading the full video."
    if end is None:
        if start == 0:
            return None, None
        return f"*{start}-inf", f"Clipping from {format_hms(start)}."
    return f"*{start}-{end}", f"Clipping {format_hms(start)} → {format_hms(end)}."


def _urlopen(url: str, timeout: int = 120):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(request, timeout=timeout)


def download_file(url: str, dest: Path, progress) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    last_pct = -1
    try:
        with _urlopen(url) as response, tmp.open("wb") as handle:
            total = int(response.headers.get("Content-Length") or 0)
            done = 0
            while True:
                chunk = response.read(1024 * 256)
                if not chunk:
                    break
                handle.write(chunk)
                done += len(chunk)
                if total > 0:
                    pct = min(100, done * 100 // total)
                    if pct != last_pct and pct % 2 == 0:
                        last_pct = pct
                        progress(f"Downloading {dest.name}… {pct}%")
        tmp.replace(dest)
    except Exception:
        if tmp.exists():
            tmp.unlink(missing_ok=True)
        raise


def extract_ffmpeg(zip_path: Path, dest_dir: Path) -> None:
    with tempfile.TemporaryDirectory() as raw:
        extracted = Path(raw)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extracted)
        ffmpeg = next(extracted.rglob("ffmpeg.exe"), None)
        ffprobe = next(extracted.rglob("ffprobe.exe"), None)
        if ffmpeg is None:
            raise FileNotFoundError("ffmpeg.exe was not in the zip.")
        shutil.copy2(ffmpeg, dest_dir / "ffmpeg.exe")
        if ffprobe is not None:
            shutil.copy2(ffprobe, dest_dir / "ffprobe.exe")


def ensure_ytdlp(progress) -> Path:
    dest = tools_dir()
    dest.mkdir(parents=True, exist_ok=True)
    ytdlp = dest / "yt-dlp.exe"
    if not _is_stale(ytdlp):
        return ytdlp

    last_error: Exception | None = None
    progress("Updating yt-dlp (YouTube changes its blocks often)…")
    for url in YTDLP_URLS:
        try:
            download_file(url, ytdlp, progress)
            _clear_ytdlp_cache(ytdlp)
            return ytdlp
        except Exception as exc:
            last_error = exc
            progress(f"Failed to download yt-dlp: {exc}")

    found = shutil.which("yt-dlp")
    if found:
        progress("Using yt-dlp from PATH. It may be outdated.")
        return Path(found).resolve()
    raise RuntimeError(
        "Could not download yt-dlp. Place yt-dlp.exe in the tools/ folder."
    ) from last_error


def ensure_tools(progress) -> tuple[Path, Path]:
    ytdlp = ensure_ytdlp(progress)
    ffmpeg_dir = locate_ffmpeg_dir()
    dest = tools_dir()
    dest.mkdir(parents=True, exist_ok=True)

    if ffmpeg_dir is None:
        zip_path = dest / "ffmpeg.zip"
        last_error: Exception | None = None
        for url in FFMPEG_ZIPS:
            try:
                progress("Downloading ffmpeg (this can take a while)…")
                download_file(url, zip_path, progress)
                progress("Extracting ffmpeg…")
                extract_ffmpeg(zip_path, dest)
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                progress(f"Failed {url.split('/')[2]}: {exc}")
        if zip_path.exists():
            zip_path.unlink(missing_ok=True)
        if last_error is not None and not (dest / "ffmpeg.exe").is_file():
            raise RuntimeError(
                "Could not download ffmpeg. "
                "Place ffmpeg.exe (and ffprobe.exe) in the tools/ folder."
            ) from last_error
        ffmpeg_dir = dest

    return ytdlp, ffmpeg_dir


def build_command(
    ytdlp: Path,
    ffmpeg_dir: Path,
    output_dir: Path,
    url: str,
    kind: str,
    extra: list[str] | None = None,
    use_cookies: bool = True,
    include_format: bool = True,
    section: str | None = None,
) -> list[str]:
    cmd = [
        str(ytdlp),
        "--ignore-config",
        "--no-update",
        "--ffmpeg-location",
        str(ffmpeg_dir),
        "-P",
        str(output_dir),
        "--newline",
        "--retries",
        "5",
        "--fragment-retries",
        "5",
    ]
    if extra:
        cmd.extend(extra)
    cookies = find_cookies(ytdlp) if use_cookies else None
    if cookies is not None:
        cmd.extend(["--cookies", str(cookies)])
    if shutil.which("node"):
        cmd.extend(["--js-runtimes", "node"])
    if include_format:
        if kind == "mp3":
            cmd.extend(
                ["-x", "--audio-format", "mp3", "--audio-quality", "0", "-f", "ba/b", "--keep-video"]
            )
        else:
            cmd.extend(["-S", "vcodec:h264,fps,res,acodec:m4a"])
    if section:
        cmd.extend(
            [
                "--download-sections",
                section,
                "-o",
                "%(title)s [%(id)s] %(section_start)s-%(section_end)s.%(ext)s",
            ]
        )
    cmd.append(url)
    return cmd


def move_outputs(src: Path, dest: Path, suffixes: tuple[str, ...]) -> list[Path]:
    dest.mkdir(parents=True, exist_ok=True)
    moved: list[Path] = []
    for path in src.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        target = dest / path.name
        if target.exists():
            target.unlink()
        shutil.move(str(path), str(target))
        moved.append(target)
    return moved


def youtube_attempts(_kind: str) -> list[tuple[str, list[str], bool, bool]]:
    """(label, extra args, use_cookies, include default format flags)."""
    return [
        (
            "h264",
            ["--impersonate", "chrome"],
            True,
            True,
        ),
        (
            "HLS",
            [
                "--impersonate",
                "chrome",
                "--extractor-args",
                "youtube:player_client=web_safari,ios,tv",
            ],
            True,
            True,
        ),
        (
            "Android",
            [
                "--impersonate",
                "chrome",
                "--extractor-args",
                "youtube:player_client=android",
            ],
            False,
            True,
        ),
    ]


class HoverButton(tk.Button):
    def __init__(self, master, bg: str, hover: str, **kwargs):
        super().__init__(master, bg=bg, activebackground=hover, **kwargs)
        self._bg = bg
        self._hover = hover
        self.bind("<Enter>", lambda _e: self.configure(bg=self._hover) if self["state"] == "normal" else None)
        self.bind("<Leave>", lambda _e: self.configure(bg=self._bg))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EZ-DLP")
        self.configure(bg=BG)
        self.minsize(720, 520)
        self.geometry("820x580")
        self._wm_icon = load_photo("icon-32.png", self)
        if self._wm_icon is not None:
            try:
                self.iconphoto(True, self._wm_icon)
            except tk.TclError:
                pass
        ico = asset_path("assets", "icon.ico")
        if ico is not None:
            try:
                self.iconbitmap(default=str(ico))
            except tk.TclError:
                try:
                    self.iconbitmap(str(ico))
                except tk.TclError:
                    pass
        self.q: queue.Queue[tuple[str, str]] = queue.Queue()
        self.busy = False
        self.output_var = tk.StringVar(value=str(load_output_dir()))
        self._build()
        self.after(80, self._pump)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _entry(self, parent, width: int | None = None) -> tk.Entry:
        opts = dict(
            bg=ENTRY_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            font=("Segoe UI", 11),
        )
        if width is not None:
            opts["width"] = width
        return tk.Entry(parent, **opts)

    def _build(self) -> None:
        pad = tk.Frame(self, bg=BG)
        pad.pack(fill="both", expand=True, padx=28, pady=22)

        title_row = tk.Frame(pad, bg=BG)
        title_row.pack(fill="x", pady=(0, 16))
        self._title_icon = self._wm_icon or load_photo("icon-32.png", self)
        if self._title_icon is not None:
            tk.Label(title_row, image=self._title_icon, bg=BG, bd=0, highlightthickness=0).pack(
                side="left", padx=(0, 10)
            )
        tk.Label(
            title_row,
            text="EZ-DLP",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        ).pack(side="left")

        labels = tk.Frame(pad, bg=BG)
        labels.pack(fill="x")
        tk.Label(labels, text="Link", bg=BG, fg=MUTED, font=("Segoe UI", 9), anchor="w").pack(
            side="left", fill="x", expand=True
        )
        tk.Label(labels, text="Start", bg=BG, fg=MUTED, font=("Segoe UI", 9), anchor="w", width=10).pack(
            side="left", padx=(8, 0)
        )
        tk.Label(labels, text="End", bg=BG, fg=MUTED, font=("Segoe UI", 9), anchor="w", width=10).pack(
            side="left", padx=(8, 0)
        )

        link_row = tk.Frame(pad, bg=BG)
        link_row.pack(fill="x", pady=(4, 14))
        self.url_entry = self._entry(link_row)
        self.url_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.start_entry = self._entry(link_row, width=10)
        self.start_entry.pack(side="left", padx=(8, 0), ipady=8)
        self.end_entry = self._entry(link_row, width=10)
        self.end_entry.pack(side="left", padx=(8, 0), ipady=8)
        self.url_entry.focus_set()

        tk.Label(pad, text="Output folder", bg=BG, fg=MUTED, font=("Segoe UI", 9), anchor="w").pack(fill="x")
        row = tk.Frame(pad, bg=BG)
        row.pack(fill="x", pady=(4, 16))
        self.out_entry = tk.Entry(
            row,
            textvariable=self.output_var,
            bg=ENTRY_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            font=("Segoe UI", 11),
        )
        self.out_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.out_entry.bind("<FocusOut>", lambda _e: self._persist_output())
        self.out_entry.bind("<Return>", lambda _e: self._persist_output())

        browse = HoverButton(
            row,
            text="Browse",
            bg=SURFACE,
            hover="#252a34",
            fg=TEXT,
            activeforeground=TEXT,
            relief="flat",
            font=("Segoe UI", 10),
            cursor="hand2",
            padx=16,
            command=self._browse,
        )
        browse.pack(side="left", fill="y", padx=(8, 0))

        btns = tk.Frame(pad, bg=BG)
        btns.pack(fill="x", pady=(0, 14))
        self.mp4_btn = HoverButton(
            btns,
            text="Download MP4",
            bg=MP4,
            hover=MP4_HOVER,
            fg=BTN_FG,
            activeforeground=BTN_FG,
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            padx=18,
            pady=10,
            command=lambda: self._start("mp4"),
        )
        self.mp4_btn.pack(side="left", expand=True, fill="x", padx=(0, 6))
        self.mp3_btn = HoverButton(
            btns,
            text="Download MP3",
            bg=MP3,
            hover=MP3_HOVER,
            fg=BTN_FG,
            activeforeground=BTN_FG,
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            padx=18,
            pady=10,
            command=lambda: self._start("mp3"),
        )
        self.mp3_btn.pack(side="left", expand=True, fill="x", padx=(6, 0))

        status_row = tk.Frame(pad, bg=BG)
        status_row.pack(fill="x", pady=(0, 6))
        self.status = tk.Label(
            status_row,
            text="Ready",
            bg=BG,
            fg=OK,
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.status.pack(side="left")

        log_wrap = tk.Frame(pad, bg=BORDER, highlightthickness=0)
        log_wrap.pack(fill="both", expand=True)
        inner = tk.Frame(log_wrap, bg=LOG_BG)
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        self.log = tk.Text(
            inner,
            bg=LOG_BG,
            fg=MUTED,
            insertbackground=TEXT,
            relief="flat",
            font=("Consolas", 9),
            wrap="word",
            state="disabled",
            highlightthickness=0,
            borderwidth=0,
        )
        scroll = tk.Scrollbar(inner, command=self.log.yview)
        self.log.configure(yscrollcommand=scroll.set)
        self.log.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        scroll.pack(side="right", fill="y")

    def _browse(self) -> None:
        current = self.output_var.get().strip() or str(factory_output_dir())
        chosen = filedialog.askdirectory(initialdir=current, title="Output folder")
        if chosen:
            self.output_var.set(chosen)
            self._persist_output()

    def _persist_output(self) -> None:
        raw = self.output_var.get().strip()
        if not raw:
            return
        save_output_dir(Path(raw))

    def _set_busy(self, busy: bool) -> None:
        self.busy = busy
        state = "disabled" if busy else "normal"
        self.mp4_btn.configure(state=state)
        self.mp3_btn.configure(state=state)
        cursor = "watch" if busy else "hand2"
        if not busy:
            self.mp4_btn.configure(bg=MP4, cursor=cursor)
            self.mp3_btn.configure(bg=MP3, cursor=cursor)
        else:
            self.mp4_btn.configure(cursor="arrow")
            self.mp3_btn.configure(cursor="arrow")

    def _emit(self, kind: str, text: str) -> None:
        self.q.put((kind, text))

    def _pump(self) -> None:
        try:
            while True:
                kind, text = self.q.get_nowait()
                if kind == "log":
                    self._append_log(text)
                elif kind == "status":
                    color, _, msg = text.partition("|")
                    self.status.configure(text=msg, fg=color)
                elif kind == "done":
                    self._set_busy(False)
        except queue.Empty:
            pass
        self.after(80, self._pump)

    def _append_log(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _start(self, kind: str) -> None:
        if self.busy:
            return
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("EZ-DLP", "Paste a link first.")
            self.url_entry.focus_set()
            return
        self._persist_output()
        out = Path(self.output_var.get().strip() or str(factory_output_dir()))
        self._set_busy(True)
        self._emit("status", f"{ACCENT}|Preparing…")
        threading.Thread(
            target=self._run,
            args=(url, out, kind, self.start_entry.get(), self.end_entry.get()),
            daemon=True,
        ).start()

    def _popen_ytdlp(self, cmd: list[str]) -> int:
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            creationflags=flags,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            line = line.rstrip("\n\r")
            if line:
                self._emit("log", line)
        return proc.wait()

    def _run(self, url: str, output_dir: Path, kind: str, start_raw: str, end_raw: str) -> None:
        work_dir: Path | None = None
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            save_output_dir(output_dir)
            ytdlp, ffmpeg_dir = ensure_tools(lambda msg: self._emit("log", msg))
            section, note = resolve_section(start_raw, end_raw)
            if note:
                self._emit("log", note)
            if kind == "mp3":
                work_dir = Path(tempfile.mkdtemp(prefix="ezdlp-mp3-"))
            else:
                work_dir = output_dir
            if is_youtube(url):
                attempts = youtube_attempts(kind)
            else:
                attempts = [("default", [], True, True)]

            code = 1
            for index, (label, extra, use_cookies, include_format) in enumerate(attempts, start=1):
                cmd = build_command(
                    ytdlp,
                    ffmpeg_dir,
                    work_dir,
                    url,
                    kind,
                    extra=extra,
                    use_cookies=use_cookies,
                    include_format=include_format,
                    section=section,
                )
                if len(attempts) > 1:
                    self._emit("log", f"— Attempt {index}/{len(attempts)}: {label}")
                self._emit("log", " ".join(cmd))
                self._emit("status", f"{ACCENT}|Downloading {kind.upper()} ({label})…")
                code = self._popen_ytdlp(cmd)
                if code == 0:
                    break
                if index < len(attempts):
                    self._emit("log", f"Failed (code {code}). Trying another method…")

            if code == 0:
                if kind == "mp3" and work_dir != output_dir:
                    moved = move_outputs(work_dir, output_dir, (".mp3",))
                    if not moved:
                        raise RuntimeError("The MP3 was created, but the final file was not found.")
                    self._emit("log", f"MP3 saved: {moved[0]}")
                self._emit("status", f"{OK}|Done — saved to {output_dir}")
                self._emit("log", f"Done. File saved to: {output_dir}")
            else:
                self._emit("status", f"{ERR}|Error (code {code})")
                self._emit("log", f"yt-dlp exited with code {code}.")
                if is_youtube(url):
                    self._emit(
                        "log",
                        "Age-restricted videos need a fresh cookies.txt "
                        "(Chrome, signed into YouTube, Get cookies.txt LOCALLY extension). "
                        "Save it as tools\\cookies.txt.",
                    )
        except Exception as exc:
            self._emit("status", f"{ERR}|Error")
            self._emit("log", str(exc))
        finally:
            if kind == "mp3" and work_dir is not None and work_dir != output_dir:
                shutil.rmtree(work_dir, ignore_errors=True)
            self._emit("done", "")


def _dpi() -> None:
    if sys.platform != "win32":
        return
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            from ctypes import windll

            windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def main() -> None:
    _dpi()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
