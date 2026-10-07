# Conversor do Bada

Página local para converter vídeos do YouTube em MP3. Você cola o link e ela roda:

```bash
yt-dlp -x --audio-format mp3 "link"
```

Uso pessoal, só roda na sua máquina.

## Como rodar

```bash
cd ~/Documents/Coding/conversor-de-video-do-bada
python3 server.py
```

O navegador padrão abre sozinho em http://127.0.0.1:8765. Cole o link e clique em **Converter**.

Para parar o servidor, aperte `Ctrl+C` no terminal.

## Onde ficam os arquivos

Os MP3 são salvos em `~/Music/yt-mp3`.
Para mudar a pasta, edite `OUT_DIR` no `server.py`.

## Requisitos

- `yt-dlp` (`brew install yt-dlp`)
- `ffmpeg` (`brew install ffmpeg`), necessário para converter em MP3
- Python 3 (não precisa instalar nenhuma biblioteca)

Se o yt-dlp parar de funcionar, atualize com `brew upgrade yt-dlp`. O YouTube muda com frequência.

## Arquivos

- `server.py`: servidor local que serve a página e executa o yt-dlp
- `index.html`: a página, com campo de link e log em tempo real

## Segurança

O servidor escuta só em `127.0.0.1`, então ninguém na sua rede acessa.
Ele aceita só links `http(s)://`.
