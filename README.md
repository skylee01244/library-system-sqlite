# A Library Management System (SQLite)
A Library Management System built with PyQt6 & SQLite  

## Build Instructions
**1) Install Required Packages**  
```
pip install PyQt6 xlrd xlsxwriter mysql-connector-python pyinstaller
```
**2) Navigate to Your Project Directory**  
Open your terminal and navigate to the project directory where index.py is located.
**3) Build the Executable**  
```
pyinstaller --name=LibrarySystem --windowed --onefile --icon=icons/library.ico --add-data "home.ui;." --add-data "login.ui;." --add-data "library_data.db;." --add-data "themes/*;themes/" --add-data "icons/*;icons/" --add-data "icons.qrc;." --hidden-import=icons_rc --exclude PySide6 index.py
```
↳ PyInstaller will create a dist folder inside your project directory. Your executable will be located inside dist/LibrarySystem.exe.

**4) Relocate the Executable**  
Move the executable file out of the dist directory and place it in your project directory (where index.py is located).

**5) Run the Application**  
To run the application, execute the LibrarySystem.exe file in your project directory.  

## Usage
Login with 
```
username: admin
password: 123
```