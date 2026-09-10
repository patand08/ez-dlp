"""Build a Windows ICO (BMP 16–64 + PNG 256) from the PNG sizes."""

from __future__ import annotations

import struct
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SIZES = (16, 24, 32, 48, 64)


def _dib(im: Image.Image) -> bytes:
    im = im.convert("RGBA")
    width, height = im.size
    flipped = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    xor = bytearray(flipped.tobytes())
    for i in range(0, len(xor), 4):
        xor[i], xor[i + 2] = xor[i + 2], xor[i]
    header = struct.pack(
        "<IIIHHIIIIII",
        40,
        width,
        height * 2,
        1,
        32,
        0,
        len(xor),
        0,
        0,
        0,
        0,
    )
    row = ((width + 31) // 32) * 4
    mask = bytes(row * height)
    return header + xor + mask


def _png(im: Image.Image) -> bytes:
    buf = BytesIO()
    im.convert("RGBA").save(buf, format="PNG")
    return buf.getvalue()


def write_ico(path: Path, images: list[tuple[int, bytes]]) -> None:
    count = len(images)
    offset = 6 + 16 * count
    header = struct.pack("<HHH", 0, 1, count)
    directory = b""
    body = b""
    for size, payload in images:
        stored = 0 if size >= 256 else size
        directory += struct.pack("<BBBBHHII", stored, stored, 0, 0, 1, 32, len(payload), offset)
        body += payload
        offset += len(payload)
    path.write_bytes(header + directory + body)


def main() -> None:
    images: list[tuple[int, bytes]] = []
    for size in SIZES:
        png = Image.open(ASSETS / f"icon-{size}.png")
        images.append((size, _dib(png)))
    png256 = Image.open(ASSETS / "icon-256.png")
    images.append((256, _png(png256)))
    out = ASSETS / "icon.ico"
    write_ico(out, images)
    print(f"wrote {out} ({out.stat().st_size} bytes, {len(images)} sizes)")


if __name__ == "__main__":
    main()
