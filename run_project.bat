@echo off
cd /d "%~dp0"
set PYTHON_EXE=%~dp0.venv\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
  echo [ERRO] Python da virtualenv nao encontrado em:
  echo %PYTHON_EXE%
  pause
  exit /b 1
)

echo Iniciando projeto Django em http://127.0.0.1:8010/tarefas/
"%PYTHON_EXE%" manage.py runserver 127.0.0.1:8010
