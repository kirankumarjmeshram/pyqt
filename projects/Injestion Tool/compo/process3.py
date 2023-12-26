import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
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
    def __init__(self, doc_id, signals):
        super().__init__()
        self.signals = signals
        self.doc_id = doc_id

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

class ProcessChecker(QRunnable):
    def __init__(self, threadpool):
        super().__init__()
        self.threadpool = threadpool

    def run(self):
        while True:
            # Check the MongoDB collection for documents with "process": "pending"
            pending_documents = collection.find({"process": "pending"})
            for doc in pending_documents:
                # Start a new worker for each pending document
                signals = WorkerSignals()
                worker = Worker(doc["_id"], signals)
                self.threadpool.start(worker)
            time.sleep(1)  # Sleep for a while before checking again

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

        # Start the process checker
        self.process_checker = ProcessChecker(self.threadpool)
        self.threadpool.start(self.process_checker)

    def add_button_clicked(self):
        input1 = self.input1.text()
        input2 = self.input2.text()

        # Insert the input data into MongoDB
        collection.insert_one({"input1": input1, "input2": input2, "process": "pending"})

    def update_status_label(self, message):
        self.status_label.setText(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
