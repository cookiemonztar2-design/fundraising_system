RME setup python venv
@echo off
python3 -m venv %userprofile%\fundraising_system\venv
%userprofile%\fundraising_system\venv\Scripts\activate.bat
pip install -r requirements.txt
echo Virtual environment setup complete. To activate it, run:
echo %userprofile%\fundraising_system\venv\Scripts\activate.bat