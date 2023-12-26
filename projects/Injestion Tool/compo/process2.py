import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal
from pymongo import MongoClient

# MongoDB URI
mongo_uri = "mongodb://localhost:27017/myprocess"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client.get_database()
collection = db.get_collection('status')

class WorkerSignals(QObject):
    finished = pyqtSignal(str)

class Worker(QRunnable):
    def __init__(self, doc_id, input1, input2, signals):
        super().__init__()
        self.signals = signals
        self.doc_id = doc_id
        self.input1 = input1
        self.input2 = input2

    def run(self):
        # Simulate a long-running process (sleep for 30 seconds)
        for _ in range(30):
            time.sleep(1)
        
        # Update the MongoDB document with the process status
        self.signals.finished.emit(f"Process {self.doc_id} completed.")
        self.update_mongo_document()

    def update_mongo_document(self):
        # Update the MongoDB document with "process" : "success"
        collection.update_one({"_id": self.doc_id}, {"$set": {"process": "success"}})
        self.signals.finished.emit(f"Document {self.input1} success")

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.input1 = QLineEdit(self)
        self.input2 = QLineEdit(self)
        self.status_label = QLabel(self)

        add_button = QPushButton('Add', self)
        add_button.clicked.connect(self.add_button_clicked)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Input 1:'))
        vbox.addWidget(self.input1)
        vbox.addWidget(QLabel('Input 2:'))
        vbox.addWidget(self.input2)
        vbox.addWidget(add_button)
        vbox.addWidget(self.status_label)

        self.setLayout(vbox)

        self.setWindowTitle('MongoDB Process Update')
        self.show()

        self.threadpool = QThreadPool()

    def add_button_clicked(self):
        input1 = self.input1.text()
        input2 = self.input2.text()

        # Insert the input data into MongoDB
        doc_id = collection.insert_one({"input1": input1, "input2": input2, "process": "pending"}).inserted_id

        # Start a separate runnable for the long-running process
        signals = WorkerSignals()
        worker = Worker(doc_id, input1, input2, signals)
        signals.finished.connect(self.update_status_label)
        self.threadpool.start(worker)

    def update_status_label(self, message):
        self.status_label.setText(message)
        self.show_popup(message)

    def show_popup(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
