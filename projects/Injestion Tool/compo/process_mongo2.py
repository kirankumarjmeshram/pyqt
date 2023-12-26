import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot
from pymongo import MongoClient

# MongoDB URI
mongo_uri = "mongodb://localhost:27017/myprocess"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client.get_database()
collection = db.get_collection('status')

class WorkerSignals(QObject):
    finished = pyqtSignal(str, QLabel)

class Worker(QRunnable):
    def __init__(self, doc_id, signals, label):
        super().__init__()
        self.signals = signals
        self.doc_id = doc_id
        self.label = label

    def run(self):
        print("run triggered")
        # Simulate a long-running process (sleep for 10 seconds)
        for _ in range(10):
            time.sleep(1)
        
        # Update the MongoDB document with the process status
        self.update_mongo_document()
        self.signals.finished.emit(f"Process {self.doc_id} completed.", self.label)

    def update_mongo_document(self):
        # Update the MongoDB document with "process" : "success"
        collection.update_one({"_id": self.doc_id}, {"$set": {"process": "success"}})

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

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

        self.threadpool = QThreadPool()

    @pyqtSlot()
    def add_button_clicked(self):
        input1 = self.input1.text()
        input2 = self.input2.text()

        # Insert the input data into MongoDB
        doc_id = collection.insert_one({"input1": input1, "input2": input2, "process": "pending"}).inserted_id

        # Create a new QLabel for the process
        label = QLabel(f"Process {input1} is running...")
        self.vbox.addWidget(label)

        # Start a separate runnable for the long-running process
        signals = WorkerSignals()
        worker = Worker(doc_id, signals, label)
        signals.finished.connect(self.update_status_label)
        self.threadpool.start(worker)

        # Check the MongoDB collection for any pending processes
        pending_documents = collection.find({"process": "pending"})
        for doc in pending_documents:
            # Start a separate runnable for each pending process
            signals = WorkerSignals()
            worker = Worker(doc["_id"], signals, label)
            signals.finished.connect(self.update_status_label)
            self.threadpool.start(worker)

    @pyqtSlot(str, QLabel)
    def update_status_label(self, message, label):
        label.setText(message)
        QMessageBox.information(self, "Process Status", message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
