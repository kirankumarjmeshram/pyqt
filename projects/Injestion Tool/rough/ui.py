from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QGroupBox
from pymongo import MongoClient
import hashlib
import sys

class ConfigPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("CONFIG")

    def initUI(self):
        layout = QVBoxLayout()

        case_owner_layout = QHBoxLayout()
        case_id_label = QLabel("CASE ID")
        case_owner_layout.addWidget(case_id_label)
        self.case_id_input = QLineEdit()
        case_owner_layout.addWidget(self.case_id_input)

        owner_id_label = QLabel("OWNER ID")
        case_owner_layout.addWidget(owner_id_label)
        self.owner_id_input = QLineEdit()
        case_owner_layout.addWidget(self.owner_id_input)
        layout.addLayout(case_owner_layout)

        group_box = QGroupBox()
        group_layout = QVBoxLayout()

        input_path_layout = QHBoxLayout()
        input_path_label = QLabel("INPUT PATH")
        input_path_layout.addWidget(input_path_label)
        self.input_path_input = QLineEdit()
        input_path_layout.addWidget(self.input_path_input)
        browse_button = QPushButton("BROWSE FOLDER AS INPUT")
        browse_button.clicked.connect(self.browse_folder)
        input_path_layout.addWidget(browse_button)
        group_layout.addLayout(input_path_layout)

        add_button = QPushButton("ADD")
        add_button.clicked.connect(self.add_button_clicked)
        group_layout.addWidget(add_button)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        self.setLayout(layout)

    def browse_folder(self):
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory()
        self.input_path_input.setText(folder_path)

    def add_button_clicked(self):
        # Add data to status collection with preprocessing_status = pending
        self.update_status_collection("pending")

    def update_status_collection(self, preprocessing_status):
        mongo_uri = "mongodb://localhost:27017/"
        mongo_db = "GARUDA"
        input_folder = self.input_path_input.text()

        mongo_client = MongoClient(mongo_uri)
        garuda_db = mongo_client[mongo_db]
        status_collection = garuda_db['status']

        existing_document = status_collection.find_one({"input_folder": input_folder})

        if existing_document:
            # Folder already exists, update the preprocessing_status
            status_collection.update_one(
                {"input_folder": input_folder},
                {"$set": {"preprocessing_status": preprocessing_status}}
            )
        else:
            # Insert new document with preprocessing_status = pending
            update_data = {
                "input_folder": input_folder,
                "preprocessing_status": preprocessing_status,
                "owner_id": self.owner_id_input.text(),
                "case_id": self.case_id_input.text()
            }
            status_collection.insert_one(update_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ConfigPage()
    ex.show()
    sys.exit(app.exec_())
