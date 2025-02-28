# A Library Management System (SQLite)
A Library Management System built with PyQt6 & SQLite

## build
1) Install PyInstaller
```
pip install pyinstaller
```
2) Navigate to Your Project Folder
3) Build the Executable
```
pyinstaller --name=LibrarySystem --windowed --onefile --icon=icons/library.ico --add-data "home.ui;." --add-data "login.ui;." --add-data "library_data.db;." --add-data "themes/*;themes/" --add-data "icons/*;icons/" --add-data "icons.qrc;." --hidden-import=icons_rc --exclude PySide6 index.py
```
    - PyInstaller will create a dist folder inside your project directory. Your executable will be located inside dist/LibrarySystem.exe.
4) Move the exe file out of /dist. Put it in your project folder (where index.py is located)

## Usage
Login with 
```
username: admin
password: 123
```