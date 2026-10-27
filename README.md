# Conversor do Bada

Página local para converter vídeos do YouTube em MP3. Você cola o link e ela roda:

```bash
yt-dlp -x --audio-format mp3 "link"
```

Uso pessoal, só roda na sua máquina.

## Requisitos

- `yt-dlp`, baixa os vídeos do youtube
- `ffmpeg`, converter para MP3

Roda esse comando que baixa os dois:
```bash
brew install yt-dlp ffmpeg
```

- Python 3 (não precisa instalar nenhuma biblioteca)

Se o yt-dlp parar de funcionar, atualize com `brew upgrade yt-dlp`. O YouTube muda com frequência.

## Como rodar

Jeito fácil: dê dois cliques em **`Abrir Conversor.command`** no Finder. O Terminal abre, o servidor sobe e o navegador abre a página. Se o servidor já estiver rodando, ele só abre a página.

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
