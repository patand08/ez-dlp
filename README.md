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

## Extra (only if you need it)

### Age-restricted videos

Normal public videos work with no extra file. For age-restricted YouTube:

1. In Chrome, while signed into YouTube, export cookies with the extension **Get cookies.txt LOCALLY**.
2. Save the file as `cookies.txt` in the same folder as the app, or inside `tools`.

Do not publish that file. It is a login.

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

## Extra (só se precisar)

### Vídeos com restrição de idade

Vídeo público normal não precisa de nada extra. Para YouTube com restrição de idade:

1. No Chrome, logado no YouTube, exporte os cookies com a extensão **Get cookies.txt LOCALLY**.
2. Salve o arquivo como `cookies.txt` na mesma pasta do app, ou dentro de `tools`.

Não publique esse arquivo. É um login.

### Se você já usa Git

```powershell
git clone https://github.com/patand08/ez-dlp.git
cd ez-dlp
```

Depois dê dois cliques em `Start.bat` ou `Build-exe.bat`.

### Atualizar o baixador

Se os downloads do YouTube começarem a falhar, abra o app mesmo assim — ele tenta atualizar o yt-dlp sozinho. Para forçar, apague `tools\yt-dlp.exe` e abra o app de novo.
