# Conversor do Bada

Fiquei cansado de ver tanto anúncio e ter um trilhão de sites pra converter tudo, então juntei tudo em um que roda na sua prórpia máquina.

Ele tem 3 funcionalidades:
- [Baixar vídeo do YouTube em MP3](#baixar-vídeo-do-youtube-em-mp3)
- [Extrair áudio de um vídeo](#extrair-áudio-de-um-vídeo)
- [Comprimir vídeo](#comprimir-vídeo)

## Requisitos

Nenhum! Na primeira vez, o próprio **Abrir Conversor** instala o que faltar (Python, `yt-dlp` e `ffmpeg`). Pode demorar um pouco e, no Mac, pedir a senha.

Se o yt-dlp parar de funcionar, atualize com `brew upgrade yt-dlp` (Mac) ou `winget upgrade yt-dlp` (Windows). O YouTube muda com frequência.

## Como rodar

## Baixar vídeo do YouTube em MP3

Página local para converter vídeos do YouTube em MP3. Você cola o link e ela roda:

```bash
yt-dlp -x --audio-format mp3 "link"
```

Uso pessoal, só roda na sua máquina.

Jeito fácil: dê dois cliques em **`Abrir Conversor.command`** no Finder (Mac) ou **`Abrir Conversor.bat`** (Windows). O Terminal abre, o servidor sobe e o navegador abre a página. Se o servidor já estiver rodando, ele só abre a página.

Pelo terminal:

```bash
cd ~/Documents/Coding/conversor-de-video-do-bada
python3 server.py
```

O navegador padrão abre sozinho em http://127.0.0.1:8765. Cole o link e clique em **Converter**.

Para parar o servidor, aperte `Ctrl+C` no terminal.

## Extrair áudio de um vídeo

Na seção **Extrair áudio de um vídeo**, escolha um arquivo (MP4, MOV...) e clique em **Extrair áudio**. Ele roda:

```bash
ffmpeg -i video.MP4 -vn -acodec libmp3lame -q:a 2 video.mp3
```

O MP3 fica em `~/Downloads/audios-extraidos-video`, com o nome do vídeo. Para mudar a pasta, edite `EXTRACT_DIR` no `server.py`.

## Comprimir vídeo

Na aba **Comprimir vídeo**, escolha (ou arraste) um vídeo, defina a compressão (Leve, Média ou Forte) e clique em **Comprimir**. Ele roda:

```bash
ffmpeg -i video.MP4 -c:v libx264 -crf 28 -preset medium -c:a aac -b:a 128k -movflags +faststart video.mp4
```

Leve, Média e Forte usam CRF 23, 28 e 32 (quanto maior, menor o arquivo e a qualidade). O resultado fica em `~/Downloads/videos-comprimidos`. Para mudar a pasta, edite `COMPRESS_DIR` no `server.py`.

## Onde ficam os arquivos

Os MP3 são salvos em `~/Downloads`.
Para mudar a pasta, edite `OUT_DIR` no `server.py`.

## Arquivos

- `server.py`: servidor local que serve a página e executa o yt-dlp e o ffmpeg
- `index.html`: a página, com campo de link e log em tempo real

## Segurança

O servidor escuta só em `127.0.0.1`, então ninguém na sua rede acessa.
Ele aceita só links `http(s)://`.