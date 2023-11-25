from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType

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

    def login(self):
        un = self.tb01.text()
        pw = self.tb02.text()
        if(un == 'admin' and pw == 'admin'):
            self.menubar.setVisible(True)
            self.tabWidget.setCurrentIndex(1)
        else:
            QMessageBox.information(self,"School Management System","Invalid admin login details, Try again !")
            self.l01.setText("Invalid admin login details, Try again !")

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
