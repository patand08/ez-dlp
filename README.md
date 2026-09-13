# EZ-DLP

Windows app: paste a link and download **MP4**, **MP3**, or a **thumbnail** with [yt-dlp](https://github.com/yt-dlp/yt-dlp).

<img width="821" height="608" alt="EZ-DLP window" src="https://github.com/user-attachments/assets/98f01690-1224-4746-b58c-9e9913e0d692" />

You do **not** need Git. You do **not** need to know how to program.

---

## Install

Pick **one** path. Both need [Python 3](https://www.python.org/downloads/) the first time (3.10 or newer).

On the Python installer, check the box **Add python.exe to PATH**, then click **Install Now**. If you skip that box, the next steps will fail.

### Option A — just open the app

Use this if you only want the window to appear.

1. On this GitHub page, click the green **Code** button → **Download ZIP**.
2. In **Downloads**, right-click `ez-dlp-main.zip` → **Extract All…** → **Extract**.
3. Open the unzipped folder until you see `app.py` and `Start.bat`.
4. Double-click **Start.bat**.

EZ-DLP should open. If Windows shows **Windows protected your PC**, click **More info** → **Run anyway**.

If a black window says Python was not found, install Python again and check **Add python.exe to PATH**.

### Option B — put EZ-DLP on the Desktop (like a normal program)

GitHub does **not** come with a ready `EZ-DLP.exe`. That file is built **on your PC**, once.

After this, you open EZ-DLP from the Desktop. You do not click `Start.bat` again.

1. Do Option A steps 1–3 first (Python + unzipped folder). You can skip opening the app.
2. In that same folder, double-click **Build-exe.bat**.
3. A black window opens. **Do not close it.** Wait until it says the shortcut was created (about 1 minute).
4. On your **Desktop**, double-click the **EZ-DLP** icon.

To use it on another Windows PC, copy `EZ-DLP.exe` (it is inside the unzipped folder) and double-click it there.

---

## First time you download something

The app also downloads two helpers into a `tools` folder next to itself: **yt-dlp** and **ffmpeg**. ffmpeg is large (~100 MB). That happens **once**. After that, the app starts faster.

Keep `EZ-DLP.exe` (or the unzipped folder) in a place you will not delete. If you move the app, the helpers go with it only if you move the whole folder.

---

## How to use

1. Paste the video link.
2. Check the save folder (default: your **Downloads** folder). The app remembers the last folder you pick.
3. **Start** / **End** are optional (`1:30`, `01:30`, or `00:01:30`):
   - both empty → the whole video
   - start only → from that time to the end
   - end only → from the beginning to that time
   - both → only that clip
   - invalid values → the whole video
4. Click **Download MP4**, **Download MP3**, or **Thumbnail** (saves a PNG; Start/End are ignored).

---

## Cookies (age-restricted YouTube)

Public videos work with no extra file. Age-restricted videos need a **YouTube login** saved as `cookies.txt`.

`cookies.txt` is a login. It is **gitignored** (`cookies.txt`, `**/cookies.txt`, and the whole `tools/` folder). Never commit it, never put it on GitHub, never send it to anyone.

### 1. Install an extension (Chrome or Firefox)

**Chrome / Edge**

1. Install **[Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)**.
2. Open `chrome://extensions` (or `edge://extensions`), find that extension, and turn on **Allow in Incognito**.

**Firefox**

1. Install **[cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)**.
2. Open `about:addons` → **cookies.txt** → turn on **Run in Private Windows** / **Allow** for private windows.

Without the private-window permission, you cannot export from Incognito / Private Browsing.

### 2. Export so YouTube does not rotate the cookies

From the [official yt-dlp docs](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies): YouTube rotates account cookies on open YouTube tabs. To keep a file that still works with yt-dlp, export a session that is **never opened in the browser again**.

1. Open a **new Incognito / Private window** (Chrome, Edge, or Firefox) and log into YouTube there (not your everyday window).
2. In **that same window and same tab**, go to `https://www.youtube.com/robots.txt`. This should be the **only** private tab open.
3. Click the extension icon (**Get cookies.txt LOCALLY** or **cookies.txt**) → export **youtube.com** cookies.
4. **Close the entire private window** right after. Do not open YouTube again in that session.
5. Rename the downloaded file to `cookies.txt`.
6. Put it in `tools\cookies.txt` (next to `yt-dlp.exe`), or in the same folder as `EZ-DLP.exe` / `app.py`.

Do **not** export from your normal browser window. Those cookies rotate and stop working. Do **not** use “copy cookies from the browser” to create this file — that copies the everyday session, not the private one.

If downloads start asking you to sign in again, repeat this export (the old file expired or was rotated).

---

## Extra

### If you already use Git

```powershell
git clone https://github.com/patand08/ez-dlp.git
cd ez-dlp
```

Then double-click `Start.bat` or `Build-exe.bat`.

### Update the downloader

If YouTube downloads start failing, double-click `Start.bat` / the Desktop icon anyway — the app tries to refresh yt-dlp by itself. To force it, open the `tools` folder and run `yt-dlp.exe` with `-U`, or delete `tools\yt-dlp.exe` and open the app again.

---

# EZ-DLP

App para Windows: cole um link e baixe **MP4**, **MP3** ou a **thumbnail** com [yt-dlp](https://github.com/yt-dlp/yt-dlp).

Você **não** precisa de Git. Você **não** precisa saber programar.

---

## Instalar

Escolha **um** caminho. Os dois precisam do [Python 3](https://www.python.org/downloads/) na primeira vez (3.10 ou mais novo).

No instalador do Python, marque a caixa **Add python.exe to PATH** e clique em **Install Now**. Se pular essa caixa, os próximos passos não funcionam.

### Opção A — só abrir o app

Use esta se você só quer a janela aparecer.

1. Nesta página do GitHub, clique no botão verde **Code** → **Download ZIP**.
2. Em **Downloads**, clique com o botão direito em `ez-dlp-main.zip` → **Extrair Tudo…** → **Extrair**.
3. Abra a pasta descompactada até ver `app.py` e `Start.bat`.
4. Dê dois cliques em **Start.bat**.

O EZ-DLP deve abrir. Se o Windows mostrar **O Windows protegeu o seu PC**, clique em **Mais informações** → **Executar assim mesmo**.

Se a janela preta disser que não achou o Python, instale o Python de novo e marque **Add python.exe to PATH**.

### Opção B — colocar o EZ-DLP na Área de trabalho (como um programa normal)

O GitHub **não** vem com o `EZ-DLP.exe` pronto. Esse arquivo é **gerado no seu PC**, uma vez.

Depois disso, você abre o EZ-DLP pelo ícone da Área de trabalho. Não precisa clicar de novo no `Start.bat`.

1. Faça antes os passos 1–3 da Opção A (Python + pasta descompactada). Não precisa abrir o app.
2. Nessa mesma pasta, dê dois cliques em **Build-exe.bat**.
3. Abre uma janela preta. **Não feche.** Espere até ela dizer que o atalho foi criado (cerca de 1 minuto).
4. Na **Área de trabalho**, dê dois cliques no ícone **EZ-DLP**.

Para usar em outro Windows, copie o `EZ-DLP.exe` (ele fica dentro da pasta descompactada) e dê dois cliques lá.

---

## Primeira vez que você baixar alguma coisa

O app também baixa dois programas auxiliares para uma pasta `tools` ao lado dele: **yt-dlp** e **ffmpeg**. O ffmpeg é grande (~100 MB). Isso acontece **uma vez**. Depois o app começa mais rápido.

Deixe o `EZ-DLP.exe` (ou a pasta descompactada) num lugar que você não vá apagar. Se mover o app, os auxiliares só vão junto se você mover a pasta inteira.

---

## Como usar

1. Cole o link do vídeo.
2. Confira a pasta de destino (padrão: **Downloads**). O app lembra a última pasta que você escolher.
3. **Start** / **End** são opcionais (`1:30`, `01:30` ou `00:01:30`):
   - os dois vazios → vídeo inteiro
   - só o início → daí até o fim
   - só o fim → do começo até esse ponto
   - os dois → só aquele trecho
   - valor inválido → vídeo inteiro
4. Clique em **Download MP4**, **Download MP3** ou **Thumbnail** (salva um PNG; Start/End são ignorados).

---

## Cookies (YouTube com restrição de idade)

Vídeo público funciona sem arquivo extra. Vídeo com restrição de idade precisa de um **login do YouTube** salvo como `cookies.txt`.

`cookies.txt` é um login. Ele está no **.gitignore** (`cookies.txt`, `**/cookies.txt` e a pasta `tools/` inteira). Nunca dê commit, nunca suba no GitHub, nunca mande esse arquivo para ninguém.

### 1. Instale uma extensão (Chrome ou Firefox)

**Chrome / Edge**

1. Instale **[Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)**.
2. Abra `chrome://extensions` (ou `edge://extensions`), ache a extensão e ligue **Permitir no modo de navegação anônima** / **Allow in Incognito**.

**Firefox**

1. Instale **[cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)**.
2. Abra `about:addons` → **cookies.txt** → ligue **Executar em janelas privativas** / **Run in Private Windows**.

Sem essa permissão, não dá para exportar da janela anônima / privativa.

### 2. Exporte de um jeito que o YouTube não gire os cookies

Pela [documentação oficial do yt-dlp](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies): o YouTube gira os cookies da conta em abas abertas do YouTube. Para o arquivo continuar válido no yt-dlp, exporte uma sessão que **nunca seja aberta de novo no navegador**.

1. Abra uma **janela anônima / privativa nova** (Chrome, Edge ou Firefox) e entre no YouTube **ali** (não na janela do dia a dia).
2. **Na mesma janela e na mesma aba**, vá em `https://www.youtube.com/robots.txt`. Essa deve ser a **única** aba privativa aberta.
3. Clique no ícone da extensão (**Get cookies.txt LOCALLY** ou **cookies.txt**) → exporte os cookies de **youtube.com**.
4. **Feche a janela privativa inteira** na hora. Não abra o YouTube de novo nessa sessão.
5. Renomeie o arquivo baixado para `cookies.txt`.
6. Coloque em `tools\cookies.txt` (ao lado do `yt-dlp.exe`), ou na mesma pasta do `EZ-DLP.exe` / `app.py`.

**Não** exporte da janela normal do navegador. Esses cookies giram e param de funcionar. **Não** use “copiar cookies do navegador” para criar esse arquivo — isso copia a sessão do dia a dia, não a privativa.

Se o download voltar a pedir login, faça essa exportação de novo (o arquivo antigo expirou ou foi girado).

---

## Extra

### Se você já usa Git

```powershell
git clone https://github.com/patand08/ez-dlp.git
cd ez-dlp
```

Depois dê dois cliques em `Start.bat` ou `Build-exe.bat`.

### Atualizar o baixador

Se os downloads do YouTube começarem a falhar, abra o app mesmo assim — ele tenta atualizar o yt-dlp sozinho. Para forçar, apague `tools\yt-dlp.exe` e abra o app de novo.
