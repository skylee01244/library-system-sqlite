# A Library Management System
This Library Management System is a robust application built using Python **PyQt6** and integrated with a **SQLite** local database. The system offers comprehensive features to manage library operations efficiently

## Build Instructions
**1) Install Required Packages**  
> For a multi-configuration generator (Windows)
```
pip install PyQt6 xlrd xlsxwriter mysql-connector-python pyinstaller
```
> For a single-configuration generator (LINUX & MACOS)  
> ⚠️ **Warning** First option will need a virtual env while option 2 & 3 are risky
```
pip install PyQt6 xlrd xlsxwriter mysql-connector-python pyinstaller
or
python3 -m pip install --user PyQt6 xlrd xlsxwriter mysql-connector-python pyinstaller
or
python3 -m pip install --break-system-packages PyQt6 xlrd xlsxwriter mysql-connector-python pyinstaller
```
**2) Navigate to Your Project Directory**  
Open your terminal and navigate to the project directory where `index.py` is located.  

**3) Build the Executable**  
```
pyinstaller --name=LibrarySystem --windowed --onefile --icon=icons/library.ico --add-data "home.ui;." --add-data "login.ui;." --add-data "library_data.db;." --add-data "themes/*;themes/" --add-data "icons/*;icons/" --add-data "icons.qrc;." --hidden-import=icons_rc --exclude PySide6 index.py
```
↳ PyInstaller will create a `dist` folder inside your project directory. Your executable will be located inside `dist/LibrarySystem.exe`.

**4) Relocate the Executable**  
 Move the executable file out of the `dist` directory and place it in your project directory (where `index.py` is located).

**5) Run the Application**  
 To run the application, execute the `LibrarySystem.exe` file in your project directory.  

## Usage
Login with 
```
username: admin
password: 123
```

## Capabilities and Functionalities
- **User Authentication and Management**: Seamlessly login, create, edit, and delete user accounts ensuring robust security and user privacy.  
- **Client Management**: Efficiently add, update, and remove client records with comprehensive details to enhance customer relations.  
- **Book Inventory Management**: Flawlessly manage the library's book inventory by adding, updating, and deleting book records, ensuring accurate and up-to-date cataloging.  
- **Borrowing and Returning Management**: Record and track book borrowing and return transactions effortlessly, ensuring accurate and real-time updates of the library's collection.  
- **Category, Author, and Publisher Management**: Maintain a meticulously organized library database by managing book categories, authors, and publishers.  
- **Data Exportation**: Easily export all data to an Excel sheet for systematic record-keeping and analytical purposes.  