# EZ-DLP

Windows app to paste a media URL and download **MP4** or **MP3** with [yt-dlp](https://github.com/yt-dlp/yt-dlp).
<img width="831" height="617" alt="image" src="https://github.com/user-attachments/assets/7a1aa985-f5c9-413a-a607-01bf035ca119" />

## Install

### Option A — run from source

1. Install [Python 3](https://www.python.org/downloads/) (3.10+).
2. Clone this repo:

```powershell
git clone https://github.com/patand08/ez-dlp.git
cd ez-dlp
python app.py
```

### Option B — standalone `.exe`

From the project folder (Python required only to build):

```powershell
.\build.ps1
```

That creates `EZ-DLP.exe` and a desktop shortcut. Double-click the shortcut or the `.exe`.

On another PC, copy `EZ-DLP.exe` (or clone the repo and run `python app.py` / `.\build.ps1`).

## First run

The app looks for `yt-dlp.exe` and `ffmpeg.exe` in a `tools\` folder next to the app. If they are missing, it downloads them automatically. ffmpeg is large (~100 MB); that only happens once.

Those binaries are **not** stored in git (GitHub file size limits).

## How to use

1. Paste a URL.
2. Confirm the output folder (defaults to your user `Downloads` folder; the last folder you pick is remembered locally in `config.json`).
3. Optional **Start** / **End** times (`hh:mm:ss`, `mm:ss`, or `00:ss`):
   - both empty → full video
   - start only → from that time to the end
   - end only → from `00:00` to that time
   - both → that clip only
   - invalid values → full video
4. Click **Download MP4** or **Download MP3**.

## Cookies (age-restricted videos)

Public videos work without cookies. For age-restricted content:

1. In Chrome, signed into YouTube, export cookies with **Get cookies.txt LOCALLY**.
2. Save as `cookies.txt` next to the app or in `tools\`.

Never commit `cookies.txt`.

## YouTube and Node

If `node` is on PATH, the app passes `--js-runtimes node` (YouTube sometimes requires a JS runtime). Public downloads often still work without Node.

## Update yt-dlp

```powershell
.\tools\yt-dlp.exe -U
```

---

# EZ-DLP

App para Windows: cole um link e baixe **MP4** ou **MP3** com [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Instalar

### Opção A — rodar o código

1. Instale o [Python 3](https://www.python.org/downloads/) (3.10+).
2. Clone o repositório:

```powershell
git clone https://github.com/patand08/ez-dlp.git
cd ez-dlp
python app.py
```

### Opção B — `.exe` avulso

Na pasta do projeto (Python só é preciso para gerar o executável):

```powershell
.\build.ps1
```

Isso cria `EZ-DLP.exe` e um atalho na área de trabalho. Clique no atalho ou no `.exe`.

Em outro PC, copie o `EZ-DLP.exe` (ou clone o repo e rode `python app.py` / `.\build.ps1`).

## Primeira execução

O app procura `yt-dlp.exe` e `ffmpeg.exe` na pasta `tools\` ao lado do app. Se não existirem, baixa sozinho. O ffmpeg é grande (~100 MB); isso acontece só uma vez.

Esses binários **não** entram no git (limite de tamanho do GitHub).

## Como usar

1. Cole o link.
2. Confira a pasta de saída (padrão: `Downloads` do usuário; a última pasta escolhida fica salva localmente em `config.json`).
3. **Start** / **End** opcionais (`hh:mm:ss`, `mm:ss` ou `00:ss`):
   - os dois vazios → vídeo inteiro
   - só início → daí até o fim
   - só fim → de `00:00` até esse ponto
   - os dois → só o trecho
   - valor inválido → vídeo inteiro
4. Clique em **Download MP4** ou **Download MP3**.

## Cookies (vídeos com restrição de idade)

Vídeos públicos funcionam sem cookies. Para conteúdo age-restricted:

1. No Chrome, logado no YouTube, exporte com **Get cookies.txt LOCALLY**.
2. Salve como `cookies.txt` ao lado do app ou em `tools\`.

Não commite `cookies.txt`.

## YouTube e Node

Se o `node` estiver no PATH, o app usa `--js-runtimes node` (o YouTube às vezes exige um runtime JS). Sem Node, o download de vídeos públicos ainda costuma funcionar.

## Atualizar o yt-dlp

```powershell
.\tools\yt-dlp.exe -U
```
