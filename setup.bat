@echo off
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Attempting to install CLI tools via winget...
winget install WhoisLookup.WhoisLookup -e --accept-package-agreements --accept-source-agreements
winget install nmap.nmap -e --accept-package-agreements --accept-source-agreements

echo.
echo Setup complete.
pause
