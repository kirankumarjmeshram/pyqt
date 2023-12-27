import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSlot
from pymongo import MongoClient
from datetime import datetime

# MongoDB URI
mongo_uri = "mongodb://localhost:27017/myprocess"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client.get_database()
collection = db.get_collection('status')

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker_process = None

    def init_ui(self):
        self.input1 = QLineEdit(self)
        self.input2 = QLineEdit(self)

        add_button = QPushButton('Add', self)
        add_button.clicked.connect(self.add_button_clicked)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(QLabel('Input 1:'))
        self.vbox.addWidget(self.input1)
        self.vbox.addWidget(QLabel('Input 2:'))
        self.vbox.addWidget(self.input2)
        self.vbox.addWidget(add_button)

        self.setLayout(self.vbox)
        self.setWindowTitle('MongoDB Process Update')
        self.show()

    @pyqtSlot()
    def add_button_clicked(self):
        input1 = self.input1.text()
        input2 = self.input2.text()

        # Insert the input data into MongoDB with a timestamp
        doc_id = collection.insert_one({"input1": input1, "input2": input2, "process": "pending", "timestamp": datetime.now()}).inserted_id

        # Start the worker script if it's not already running
        if self.worker_process is None or self.worker_process.poll() is not None:
            self.worker_process = subprocess.Popen(['/usr/bin/python3', 'worker.py'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
