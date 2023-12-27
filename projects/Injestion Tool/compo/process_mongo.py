import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot
from pymongo import MongoClient

# MongoDB URI (replace with your actual values)
mongo_uri = "mongodb://localhost:27017/myprocess"

# Connect to MongoDB
try:
    client = MongoClient(mongo_uri)
    db = client.get_database()
    collection = db.get_collection('status')
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)

class WorkerSignals(QObject):
    finished = pyqtSignal(str)

class Worker(QRunnable):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals

    def run(self):
        while True:
            try:
                # Check the MongoDB collection for any pending processes
                pending_document = collection.find_one({"process": "pending"})
                if pending_document is not None:
                    print("run triggered")
                    # Simulate a long-running process (sleep for 10 seconds)
                    for _ in range(10):
                        time.sleep(1)

                    # Update the MongoDB document with the process status
                    self.update_mongo_document(pending_document["_id"])
                    self.signals.finished.emit(f"Process {pending_document['_id']} completed.")
            except Exception as e:
                print(f"Error in worker run: {e}")

    def update_mongo_document(self, doc_id):
        try:
            # Update the MongoDB document with "process" : "success"
            collection.update_one({"_id": doc_id}, {"$set": {"process": "success"}})
        except Exception as e:
            print(f"Error updating MongoDB document: {e}")

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

        # Start the worker
        signals = WorkerSignals()
        worker = Worker(signals)
        signals.finished.connect(self.update_status_label)
        self.threadpool.start(worker)

    @pyqtSlot()
    def add_button_clicked(self):
        try:
            input1 = self.input1.text()
            input2 = self.input2.text()

            # Insert the input data into MongoDB
            collection.insert_one({"input1": input1, "input2": input2, "process": "pending"})
        except Exception as e:
            print(f"Error adding data to MongoDB: {e}")

    @pyqtSlot(str)
    def update_status_label(self, message):
        # Find the existing QLabel in the layout and update its text
        for i in range(self.vbox.count()):
            item = self.vbox.itemAt(i)
            if isinstance(item.widget(), QLabel):
                item.widget().setText(message)
                break
        else:
            # If no existing QLabel is found, create a new one and add it to the layout
            label = QLabel(message)
            self.vbox.addWidget(label)

        QMessageBox.information(self, "Process Status", message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
