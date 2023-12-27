import sys
import time
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from pymongo import MongoClient

# MongoDB URI
mongo_uri = "mongodb://localhost:27017/myprocess"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client.get_database()
collection = db.get_collection('status')

class Worker(QThread):
    finished = pyqtSignal(str)  # Define the finished signal to emit a string

    def run(self):
        while True:
            # Check the MongoDB collection for any pending processes
            # Sort by timestamp to ensure FIFO order
            pending_document = collection.find_one({"process": "pending"}, sort=[("timestamp", 1)])
            if pending_document is not None:
                self.long_running_task(pending_document["_id"])
    
    def long_running_task(self, doc_id):
        print("run triggered")
        # Simulate a long-running process (sleep for 10 seconds)
        for _ in range(10):
            time.sleep(1)
        
        # Update the MongoDB document with the process status
        self.update_mongo_document(doc_id)
        self.finished.emit(f"Process {doc_id} completed.")  # Emit the finished signal with a string argument

    def update_mongo_document(self, doc_id):
        # Update the MongoDB document with "process" : "success"
        collection.update_one({"_id": doc_id}, {"$set": {"process": "success"}})

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.input1 = QLineEdit(self)
        self.input2 = QLineEdit(self)

        add_button = QPushButton('Add', self)
        add_button.clicked.connect(self.add_button_clicked)  # Connect the clicked signal to the add_button_clicked slot

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(QLabel('Input 1:'))
        self.vbox.addWidget(self.input1)
        self.vbox.addWidget(QLabel('Input 2:'))
        self.vbox.addWidget(self.input2)
        self.vbox.addWidget(add_button)

        self.setLayout(self.vbox)

        self.setWindowTitle('MongoDB Process Update')
        self.show()

        # Start the worker
        self.worker = Worker()
        self.worker.finished.connect(self.update_status_label)  # Connect the finished signal to the update_status_label slot
        self.worker.start()

    @pyqtSlot()
    def add_button_clicked(self):  # Define the add_button_clicked slot
        input1 = self.input1.text()
        input2 = self.input2.text()

        # Insert the input data into MongoDB with a timestamp
        collection.insert_one({"input1": input1, "input2": input2, "process": "pending", "timestamp": datetime.now()})

    @pyqtSlot(str)
    def update_status_label(self, message):
        label = QLabel(message)
        self.vbox.addWidget(label)
        QMessageBox.information(self, "Process Status", message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
