@echo off
echo Building Admin EXE using PyInstaller...
pip install pyinstaller flet
pyinstaller --noconsole --onefile --name "AdminDashboard" admin_app.py
echo.
echo Note: Flet apps work best with PyInstaller.
echo The EXE can be found in the "dist" folder.
pause
