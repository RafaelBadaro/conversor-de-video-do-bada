@echo off
cd /d "%~dp0"

rem Se o servidor ja estiver rodando, so abre o navegador.
curl -s -o nul http://127.0.0.1:8765
if %errorlevel%==0 (
  start http://127.0.0.1:8765
  exit /b
)

python server.py
pause
