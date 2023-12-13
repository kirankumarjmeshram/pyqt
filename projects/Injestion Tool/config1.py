from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QGroupBox, QMessageBox
from pymongo import MongoClient
import os
from dotenv import load_dotenv

class ConfigPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setGeometry(300, 300, 800, 600) 
        self.setWindowTitle("CONFIG") 

    def initUI(self):
        layout = QVBoxLayout()

        # Create the input fields
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

        # Create a group box
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
        add_button.clicked.connect(self.add_to_database)
        group_layout.addWidget(add_button)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        self.setLayout(layout)

    def browse_folder(self):
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory()
        self.input_path_input.setText(folder_path)

    def add_to_database(self):
        load_dotenv()
        MONGO_URI = os.getenv('URI')
        client = MongoClient(MONGO_URI) 
        db = client['configdb'] 
        collection = db['configs_paths'] 

        data = {
            'input_path': self.input_path_input.text()
        }

        collection.insert_one(data) 

         # Show a message box when data is added successfully
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Path added successfully!")
        msg.setWindowTitle("Success")
        msg.exec_()

if __name__ == "__main__":
    app = QApplication([])
    ex = ConfigPage()
    ex.show()
    app.exec_()
