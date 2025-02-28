from PyQt6.QtCore import * 
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from xlrd import *
import xlsxwriter
import sys
import mysql.connector
import datetime
import sqlite3

from PyQt6.uic import loadUiType

ui,_ = loadUiType('home.ui')
login,_ = loadUiType('login.ui')


class Login(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        
        self.pushButton.clicked.connect(self.Handle_Login)
        
    def Handle_Login(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        
        sql = ''' SELECT * FROM users '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if(username == row[1] and password == row[3]):
                print("Login Successful")
                self.window2 = MainApp()
                self.close()
                self.window2.show()
            else:
                self.label.setText('Wrong Username and Password')
                self.lineEdit.setText('')
                self.lineEdit_2.setText('')
                
        

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()

        self.Show_Category()
        self.Show_Author()
        self.Show_Publisher()

        self.Show_Category_Combobox()
        self.Show_Author_Combobox()
        self.Show_Publisher_Combobox()
        
        self.Show_All_Clients()
        self.Show_All_Books()
        
        self.Show_All_Operations()

    
    def Handle_UI_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)       # hide the top tab bar 

    def Handle_Buttons(self):
        self.pushButton_5.clicked.connect(self.Show_Themes)
        self.pushButton_21.clicked.connect(self.Hiding_Themes)

        self.pushButton.clicked.connect(self.Open_Day_To_Day_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_26.clicked.connect(self.Open_Clients_Tab)
        self.pushButton_3.clicked.connect(self.Open_Users_Tab)
        self.pushButton_4.clicked.connect(self.Open_Settings_Tab)

        self.pushButton_7.clicked.connect(self.Add_New_Book)
        self.pushButton_9.clicked.connect(self.Search_Books)
        self.pushButton_8.clicked.connect(self.Edit_Books)
        self.pushButton_10.clicked.connect(self.Delete_Books)

        self.pushButton_14.clicked.connect(self.Add_Category)
        self.pushButton_15.clicked.connect(self.Add_Author)
        self.pushButton_16.clicked.connect(self.Add_Publisher)
        
        self.pushButton_11.clicked.connect(self.Add_New_User)
        self.pushButton_12.clicked.connect(self.Login)
        self.pushButton_13.clicked.connect(self.Edit_User)
        
        self.pushButton_19.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_18.clicked.connect(self.Dark_Grey_Theme)
        self.pushButton_20.clicked.connect(self.Classic_Theme)
        self.pushButton_22.clicked.connect(self.Dark_Orange_Theme)
        
        self.pushButton_17.clicked.connect(self.Add_New_Client)
        self.pushButton_24.clicked.connect(self.Search_Client)
        self.pushButton_23.clicked.connect(self.Edit_Client)
        self.pushButton_25.clicked.connect(self.Delete_Client)
        
        self.pushButton_6.clicked.connect(self.Handle_Day_Operations)
        
        self.pushButton_29.clicked.connect(self.Export_Day_Operations)
        self.pushButton_27.clicked.connect(self.Export_Books)
        self.pushButton_28.clicked.connect(self.Export_Clients)


    def Show_Themes(self):
        self.groupBox_3.show()

    def Hiding_Themes(self):
        self.groupBox_3.hide()

    #################################
    ########## OPENING TABS #########

    def Open_Day_To_Day_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)
        
    def Open_Clients_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(4)

    #################################
    ########## DAY 2 DAY ############
    
    def Handle_Day_Operations(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        book_title = self.lineEdit.text()
        client_name = self.lineEdit_29.text()
        book_type = self.comboBox.currentText()
        days_number = self.comboBox_2.currentIndex() + 1
        today_date = datetime.date.today()
        to_date = today_date + datetime.timedelta(days=int(days_number))
        
        self.cur.execute('''
            INSERT INTO dayoperations(book_name, client, type, days, date, to_date) 
            VALUES (?, ?, ?, ?, ?, ?)           
        ''', (book_title, client_name, book_type, days_number, today_date.isoformat(), to_date.isoformat()))
        
        self.db.commit()
        self.statusBar().showMessage('New Operations Added')
        
        self.Show_All_Operations()

    def Show_All_Operations(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT book_name, client, type, date, to_date FROM dayoperations''')
        data = self.cur.fetchall()
        
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            
        column_widths = [150, 150, 150, 150, 150] 

        for col in range(len(column_widths)):
            self.tableWidget.setColumnWidth(col, column_widths[col])
            
        self.db.close()
        

    #################################
    ########## BOOKS ################
    
    def Add_New_Book(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_description = self.textEdit.toPlainText() 
        book_code = self.lineEdit_5.text()
        book_category = self.comboBox_5.currentText()
        book_author = self.comboBox_6.currentText()
        book_publisher = self.comboBox_7.currentText()
        book_price = self.lineEdit_6.text()

        self.cur.execute(''' 
            INSERT INTO book(book_name, book_description, book_code, book_category, book_author, book_publisher, book_price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''' ,(book_title, book_description, book_code, book_category, book_author, book_publisher, book_price))
        self.db.commit()
        self.statusBar().showMessage('New Book Added')
        
        self.lineEdit_2.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_5.setText('')
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        self.lineEdit_6.setText('')
        self.Show_All_Books()
        
    def Show_All_Books(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT book_code, book_name, book_description, book_category, book_author, book_publisher, book_price FROM book''')
        data = self.cur.fetchall()
        # print(data)
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)
        for row, form in enumerate(data):
            for col , item in enumerate(form):
                self.tableWidget_6.setItem(row,col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)
        # self.tableWidget_6.resizeColumnsToContents()
        # self.tableWidget_6.resizeRowsToContents()
        # self.tableWidget_6.resizeColumnsToContents()
        # self.tableWidget_6.resizeRowToContents(0)
        
        column_widths = [100, 200, 200, 150, 150, 150, 100] 

        for col in range(len(column_widths)):
            self.tableWidget_6.setColumnWidth(col, column_widths[col])
        self.db.close()
        # self.Show_All_Books()
        
    def Search_Books(self):
        book_title = self.lineEdit_3.text()
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        search_book_title = self.lineEdit_3.text().strip()
        if not search_book_title: self.lineEdit_3.setText("Enter book name.."); return
        
        self.cur.execute("SELECT * FROM book WHERE book_name = ?", (search_book_title,))
        data = self.cur.fetchone()
        if data is None: self.lineEdit_3.setText("Book does not exist"); return
        
        sql =  ''' SELECT * FROM book WHERE book_name = ?'''
        self.cur.execute(sql, [(book_title)])
        
        data = self.cur.fetchone()
        # print(data)
        self.lineEdit_10.setText(data[1])           # title
        self.textEdit_2.setPlainText(data[2])       # description
        self.lineEdit_9.setText(data[3])            # code
        self.comboBox_8.setCurrentText(data[4])    # category
        self.comboBox_9.setCurrentText(data[5])    # author
        self.comboBox_10.setCurrentText(data[6])   # publisher
        self.lineEdit_7.setText(str(data[7]))       # price
        

    def Edit_Books(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        book_title = self.lineEdit_10.text()                # title
        book_description = self.textEdit_2.toPlainText()    # description
        book_code = self.lineEdit_9.text()                  # code
        book_category = self.comboBox_8.currentText()      # category
        book_author = self.comboBox_9.currentText()        # author
        book_publisher = self.comboBox_10.currentText()    # publisher
        book_price = self.lineEdit_7.text()                 # price
        
        search_book_title = self.lineEdit_3.text().strip()
        if not search_book_title: self.lineEdit_3.setText("Enter book name.."); return
        
        self.cur.execute("SELECT * FROM book WHERE book_name = ?", (search_book_title,))
        data = self.cur.fetchone()
        if data is None: self.lineEdit_3.setText("Book does not exist"); return
        
        self.cur.execute('''
            UPDATE book SET book_name=? ,book_description=? ,book_code=? ,book_category=? ,book_author=? ,book_publisher=? ,book_price=? WHERE book_name=?              
        ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price, search_book_title))
        self.db.commit()
        self.statusBar().showMessage('Book Updated')
        self.Show_All_Books()
        
    def Delete_Books(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        book_title = self.lineEdit_3.text()
        warning = QMessageBox.warning(self, 'Delete Book', "Are you sure you want to delete this book?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if warning == QMessageBox.StandardButton.Yes:
            sql = '''DELETE FROM book WHERE book_name = ?'''
            self.cur.execute(sql, (book_title,))  # Use tuple format
            self.db.commit()

            self.statusBar().showMessage('Book Deleted Successfully')
            self.Show_All_Books()
    
    #################################
    ########## Clients ##############

    def Add_New_Client(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        client_name = self.lineEdit_4.text()
        client_email = self.lineEdit_8.text()
        client_passport_id = self.lineEdit_24.text()
        
        self.cur.execute('''
            INSERT INTO clients(client_name, client_email, client_passport_number)
            VALUES (?, ?, ?)    
        ''', (client_name, client_email, client_passport_id))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('New Client Added')   
        self.Show_All_Clients()     
    
    def Show_All_Clients(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT client_name, client_email, client_passport_number FROM clients''')
        data = self.cur.fetchall()
        # print(data)
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)
        for row, form in enumerate(data):
            for col , item in enumerate(form):
                self.tableWidget_5.setItem(row,col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)
        
        column_widths = [200, 200, 200] 

        for col in range(len(column_widths)):
            self.tableWidget_5.setColumnWidth(col, column_widths[col])
        
        self.db.close()
    
    def Search_Client(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        client_passport_id = self.lineEdit_27.text()
        
        sql = ''' SELECT * FROM clients WHERE client_passport_number = ?'''
        self.cur.execute(sql, [(client_passport_id)])
        data = self.cur.fetchone()
        # print(data)
        if data != None:
            self.lineEdit_25.setText(data[1])
            self.lineEdit_26.setText(data[2])
            self.lineEdit_28.setText(data[3])
        else:
            self.lineEdit_27.setText('No Client is found')
            self.statusBar().showMessage('No Client is found')
        
    
    def Edit_Client(self):
        client_original_passport_id = self.lineEdit_27.text()
        client_name = self.lineEdit_25.text()
        client_email = self.lineEdit_26.text()
        client_passport_id = self.lineEdit_28.text()
        
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        self.cur.execute('''
            UPDATE clients SET client_name=?, client_email=?, client_passport_number=? WHERE client_passport_number = ?  
        ''', (client_name, client_email, client_passport_id,client_original_passport_id))
        self.db.commit()
        self.statusBar().showMessage('Client Data Updated')
        self.Show_All_Clients()
    
    def Delete_Client(self):
        client_original_passport_id = self.lineEdit_27.text()
        
        warning = QMessageBox.warning(self, 'Delete Client', "Are you sure you want to delete this client?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if warning == QMessageBox.StandardButton.Yes:
            self.db = sqlite3.connect("library_data.db")
            self.cur = self.db.cursor()
            
            sql = ('''DELETE FROM clients WHERE client_passport_number = ?''')
            self.cur.execute(sql, [(client_original_passport_id)])
            self.db.commit()
            self.db.close()
            self.statusBar().showMessage('Client Deleted Successfully')
            self.Show_All_Clients()

    #################################
    ########## USERS ################

    def Add_New_User(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        username = self.lineEdit_11.text()
        email = self.lineEdit_12.text()
        password = self.lineEdit_13.text()
        password2 = self.lineEdit_14.text()
        
        if(password == password2): 
            self.cur.execute('''
                INSERT INTO users(user_name, user_email, user_password)
                VALUES (?, ?, ?)           
            ''', (username, email, password))
            self.db.commit()
            self.statusBar().showMessage('New User Added')
            self.label_30.setText('User Successfully Added')
            
            self.lineEdit_11.setText('')
            self.lineEdit_12.setText('')
            self.lineEdit_13.setText('')
            self.lineEdit_14.setText('')
        else:
            self.label_30.setText('Passwords do not match')
        

    def Login(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        username = self.lineEdit_17.text()
        password = self.lineEdit_15.text()
        
        sql = ''' SELECT * FROM users '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if(username == row[1] and password == row[3]):
                self.statusBar().showMessage('Valid Username & Password')
                self.groupBox_4.setEnabled(True)
                self.lineEdit_20.setText(row[1])
                self.lineEdit_19.setText(row[2])
                self.lineEdit_16.setText(row[3])

    def Edit_User(self):
        username = self.lineEdit_20.text()
        useremail = self.lineEdit_19.text()
        password = self.lineEdit_16.text()
        password2 = self.lineEdit_18.text()
        
        original_name = self.lineEdit_17.text()

        if(password == password2):
            self.db = sqlite3.connect("library_data.db")
            self.cur = self.db.cursor()
            
            self.cur.execute('''
                UPDATE users SET user_name = ?, user_email = ?, user_password = ? WHERE user_name = ?                
            ''', (username, useremail, password, original_name))
            self.db.commit()
            self.statusBar().showMessage('User Data Updated Successfully')
        else:
            print('Make sure you entered your password correctly')
    #################################
    ########## SETTINGS #############

    def Add_Category(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()

        category_name = self.lineEdit_21.text().strip()
        if not category_name: 
            self.lineEdit_21.setText('')
            return
        
        self.cur.execute('''
            INSERT INTO category (category_name) VALUES (?)
        ''', (category_name,))

        self.db.commit()
        self.statusBar().showMessage('New Category Added ')
        self.lineEdit_21.setText('')
        self.Show_Category()
        self.Show_Category_Combobox()

    def Show_Category(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category ''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)
                
        column_widths = [300] 

        for col in range(len(column_widths)):
            self.tableWidget_2.setColumnWidth(col, column_widths[col])


    def Add_Author(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()

        author_name = self.lineEdit_22.text().strip()
        if not author_name: 
            self.lineEdit_22.setText('')
            return
        self.cur.execute('''
            INSERT INTO author (author_name) VALUES (?)
        ''', (author_name,))

        self.db.commit()
        self.lineEdit_22.setText('')
        self.statusBar().showMessage('New Author Added ')
        self.Show_Author()
        self.Show_Author_Combobox()

    def Show_Author(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM author ''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)
                
        column_widths = [300] 

        for col in range(len(column_widths)):
            self.tableWidget_3.setColumnWidth(col, column_widths[col])

    def Add_Publisher(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()

        publisher_name = self.lineEdit_23.text().strip()
        if not publisher_name: 
            self.lineEdit_23.setText('')
            return
        self.cur.execute('''
            INSERT INTO publisher (publisher_name) VALUES (?)
        ''', (publisher_name,))

        self.db.commit()
        self.lineEdit_23.setText('')
        self.statusBar().showMessage('New Publisher Added ')
        self.Show_Publisher()
        self.Show_Publisher_Combobox()

    def Show_Publisher(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)
                
        column_widths = [300] 

        for col in range(len(column_widths)):
            self.tableWidget_4.setColumnWidth(col, column_widths[col])


    #################################
    #### SHOW SETTINGS DATA IN UI ###

    def Show_Category_Combobox(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category ''')
        data = self.cur.fetchall()

        self.comboBox_5.clear()
        self.comboBox_8.clear()
        for category in data:
            self.comboBox_5.addItem(category[0]) 
            self.comboBox_8.addItem(category[0])

    def Show_Author_Combobox(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM author ''')
        data = self.cur.fetchall()

        self.comboBox_6.clear()
        self.comboBox_9.clear()
        for author in data:
            self.comboBox_6.addItem(author[0])
            self.comboBox_9.addItem(author[0])

    def Show_Publisher_Combobox(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()

        self.comboBox_7.clear()
        self.comboBox_10.clear()
        for publisher in data:
            self.comboBox_7.addItem(publisher[0])
            self.comboBox_10.addItem(publisher[0])
            
    #################################
    ########## UI ###################   
    
    def Export_Day_Operations(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT book_name, client, type, date, to_date FROM dayoperations''')
        data = self.cur.fetchall()
        wb = xlsxwriter.Workbook('day_operations.xlsx')
        sheet1 = wb.add_worksheet()

        # Write headers
        headers = ['Book Title', 'Client Title', 'Type', 'From - Date', 'To - Date']
        for col, header in enumerate(headers):
            sheet1.write(0, col, header)

        # Write data
        for row, row_data in enumerate(data, start=1):
            for col, item in enumerate(row_data):
                sheet1.write(row, col, str(item))

        self.statusBar().showMessage('Operations Report Created Successfully')
        wb.close()
        self.db.close()
        
    
    def Export_Books(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT book_code, book_name, book_description, book_category, book_author, book_publisher, book_price FROM book''')
        data = self.cur.fetchall()
        wb = xlsxwriter.Workbook('books.xlsx')
        sheet1 = wb.add_worksheet()

        # Write headers
        headers = ['Book Code', 'Book Name', 'Book Description', 'Book Category', 'Book Author', 'Book Publisher', 'Book Price']
        for col, header in enumerate(headers):
            sheet1.write(0, col, header)

        # Write data
        for row, row_data in enumerate(data, start=1):
            for col, item in enumerate(row_data):
                sheet1.write(row, col, str(item))

        self.statusBar().showMessage('Book Report Created Successfully')
        wb.close()
        self.db.close()
    
    def Export_Clients(self):
        self.db = sqlite3.connect("library_data.db")
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT client_name, client_email, client_passport_number FROM clients''')
        data = self.cur.fetchall()
        wb = xlsxwriter.Workbook('clients.xlsx')
        sheet1 = wb.add_worksheet()

        # Write headers
        headers = ['Client Name', 'Client Email', 'Client Passport Number']
        for col, header in enumerate(headers):
            sheet1.write(0, col, header)

        # Write data
        for row, row_data in enumerate(data, start=1):
            for col, item in enumerate(row_data):
                sheet1.write(row, col, str(item))

        self.statusBar().showMessage('Clients Report Created Successfully')
        wb.close()
        self.db.close()
         
    #################################
    ########## UI ###################

    def Dark_Blue_Theme(self):
        style = open('themes/dark_blue.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    
    def Dark_Grey_Theme(self):
        style = open('themes/style_gray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    
    def Classic_Theme(self):
        style = open('themes/classic.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    
    def Dark_Orange_Theme(self):
        style = open('themes/dark_orange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    
def main():
    app = QApplication(sys.argv)
    # window = MainApp()
    window = Login()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()

