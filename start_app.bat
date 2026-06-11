@echo off
cd /d "%~dp0"
echo Starting INTI Movie Recommendation...
echo Missing Python packages will be installed automatically.
python app.py
if errorlevel 1 (
  echo.
  echo The app could not start. Make sure Python is installed and added to PATH.
  pause
)
