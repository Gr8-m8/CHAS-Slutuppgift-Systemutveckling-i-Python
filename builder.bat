venv\Scripts\python.exe -m PyInstaller main.py -n "Monitor" --onefile --collect-submodules "logger.py" --collect-submodules "menu.py" --collect-submodules "psmonitor.py" --collect-submodules "saver.py" --collect-submodules "textefficiency.py"
mkdir dist\data
mkdir dist\data\log
mkdir dist\data\save