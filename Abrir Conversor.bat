@echo off
cd /d "%~dp0"

rem Se o servidor ja estiver rodando, so abre o navegador.
curl -s -o nul http://127.0.0.1:8765
if %errorlevel%==0 (
  start http://127.0.0.1:8765
  exit /b
)

rem Instala o que faltar (so na primeira vez).
set INSTALOU=0
python --version >nul 2>&1 || (winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements & set INSTALOU=1)
where yt-dlp >nul 2>&1 || (winget install -e --id yt-dlp.yt-dlp --accept-source-agreements --accept-package-agreements & set INSTALOU=1)
where ffmpeg >nul 2>&1 || (winget install -e --id Gyan.FFmpeg --accept-source-agreements --accept-package-agreements & set INSTALOU=1)
if %INSTALOU%==1 (
  echo.
  echo Instalacao concluida! Feche esta janela e de dois cliques em "Abrir Conversor.bat" de novo.
  pause
  exit /b
)

python server.py
pause
