RME setup python venv
@echo off
python3 -m venv ..\fundraising_system\venv
..\fundraising_system\venv\Scripts\activate.bat
pip install -r requirements.txt
echo Virtual environment setup complete. To activate it, run:
echo ..\fundraising_system\venv\Scripts\activate.bat