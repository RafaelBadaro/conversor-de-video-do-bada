#!/bin/zsh
# Clique duas vezes no Finder para abrir o Conversor do Bada.
# Na primeira vez, instala sozinho o que faltar (pode pedir a senha do Mac).
cd "$(dirname "$0")"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

# Se o servidor já estiver rodando, só abre o navegador.
if curl -s -o /dev/null http://127.0.0.1:8765; then
  open http://127.0.0.1:8765
  exit 0
fi

# Homebrew (instalador de programas do Mac)
if ! command -v brew >/dev/null; then
  echo "Instalando o Homebrew (só na primeira vez, pode demorar)..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || exit 1
  eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"
fi

command -v yt-dlp >/dev/null || brew install yt-dlp
command -v ffmpeg >/dev/null || brew install ffmpeg
python3 -c "" 2>/dev/null || brew install python

python3 server.py
