#!/bin/zsh
# Clique duas vezes no Finder para abrir o Conversor do Bada.
cd "$(dirname "$0")"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

# Se o servidor já estiver rodando, só abre o navegador.
if curl -s -o /dev/null http://127.0.0.1:8765; then
  open http://127.0.0.1:8765
  exit 0
fi

python3 server.py
