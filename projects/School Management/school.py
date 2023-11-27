from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import mysql.connector as con
import os
from dotenv import load_dotenv
load_dotenv()
pwd = os.getenv("PASS")

ui, _ = loadUiType('school.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # set 1st tab default
        self.tabWidget.setCurrentIndex(0)
        # hide visibility of other tabs
        self.tabWidget.tabBar().setVisible(False)
        # hide menu visibility
        self.menubar.setVisible(False)
        self.b01.clicked.connect(self.login)
        self.menu11.triggered.connect(self.show_add_new_student_tab)
        self.b12.clicked.connect(self.save_student_details)
   
    # LOGIN FORM
    def login(self):
        un = self.tb01.text()
        pw = self.tb02.text()
        if(un == 'admin' and pw == 'admin'):
            self.menubar.setVisible(True)
            self.tabWidget.setCurrentIndex(1)
        else:
            QMessageBox.information(self,"School Management System","Invalid admin login details, Try again !")
            self.l01.setText("Invalid admin login details, Try again !")

    # ADD NEW STUDENT
    def show_add_new_student_tab(self):
        self.tabWidget.setCurrentIndex(2)
        self.fill_next_registration_number()

    def fill_next_registration_number(self):
        try:
            rn = 0
            mydb = con.connect(host="localhost", user="root", password=pwd, db="school")
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM student")
            result = cursor.fetchall()
            if result:
                for stud in result:
                    rn +=1
            self.tb11.setText(str(rn+1))
        except con.Error as e:
            print("Error occured in select student reg number")
    
    def save_student_details(self):
        try:
            mydb = con.connect(host = "localhost", user="root", password = pwd, db="school")
            cursor = mydb.cursor()
            registration_number = self.tb11.text()
            full_name = self.tb12.text()
            gender = self.cb11.currentText()
            date_of_birth = self.tb13.text()
            age = self.tb14.text()
            address = self.mtb11.toPlainText()
            phone = self.tb15.text()
            email = self.tb16.text()
            standard = self.cb12.currentText()

            qry = "INSERT INTO student (registration_number, full_name,gender,date_of_birth, age, address, phone, email, standard) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            value = (registration_number, full_name,gender,date_of_birth, age, address, phone, email, standard)
            cursor.execute(qry,value)
            mydb.commit()

            self.l12.setText("Student details saved successfully")
            QMessageBox.information(self,"School Management System", "Student details saved successfully")

        except con.Error as e:
            self.l12.setText("Error in save student form "+ e)
            print("Error occured in saving student info")
        

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
