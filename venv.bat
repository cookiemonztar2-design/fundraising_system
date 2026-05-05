REM setup python venv
@echo off
python -m venv fundraising_system\venv
if errorlevel 1 (
    echo Failed to create virtual environment. Please ensure Python is installed and added to PATH.
    exit /b 1
)
if not exist fundraising_system\venv\Scripts\activate.bat (
    echo Virtual environment was not created correctly. Activation script not found.
    exit /b 1
)
call fundraising_system\venv\Scripts\activate.bat
pip install -r requirements.txt
echo Virtual environment setup complete. To activate it, run:
echo fundraising_system\venv\Scripts\activate.bat