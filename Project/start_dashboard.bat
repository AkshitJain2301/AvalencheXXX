@echo off
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
    py -3 -m pip install -r requirements.txt
    py -3 -m streamlit run app.py --server.headless true
) else (
    python -m pip install -r requirements.txt
    python -m streamlit run app.py --server.headless true
)
