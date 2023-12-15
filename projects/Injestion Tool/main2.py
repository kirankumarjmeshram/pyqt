from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit,  QDesktopWidget, QMainWindow, QLineEdit, QMessageBox, QGroupBox, QFileDialog
from pymongo import MongoClient
import os
from dotenv import load_dotenv

class IngestionTool(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setGeometry(300, 300, 800, 600)  
        self.setWindowTitle("Ingection Tool")

    def initUI(self):
        layout = QVBoxLayout()

        # Create the top bar
        top_bar = QHBoxLayout()
        top_label = QLabel("INGESTION TOOL")
        top_bar.addWidget(top_label)
        top_bar.addStretch(1)
        settings_btn = QPushButton("SETTINGS")
        settings_btn.clicked.connect(self.open_settings)
        top_bar.addWidget(settings_btn)
        config_btn = QPushButton("CONFIG")
        config_btn.clicked.connect(self.open_config)
        top_bar.addWidget(config_btn)
        layout.addLayout(top_bar)

        # Manually add each row
        # FILE PARSER
        file_parser_row = QWidget()
        file_parser_layout = QHBoxLayout()
        file_parser_label = QLabel("FILE PARSER")
        file_parser_layout.addWidget(file_parser_label)

        file_parser_pid_btn = QPushButton("PID")
        file_parser_pid_btn.clicked.connect(self.file_parser_pid)
        file_parser_layout.addWidget(file_parser_pid_btn)

        file_parser_start_btn = QPushButton("START")
        file_parser_start_btn.clicked.connect(self.file_parser_start)
        file_parser_layout.addWidget(file_parser_start_btn)

        file_parser_config_btn = QPushButton("CONFIG")
        file_parser_config_btn.clicked.connect(self.file_parser_config)
        file_parser_layout.addWidget(file_parser_config_btn)

        file_parser_status_btn = QPushButton("STATUS")
        file_parser_status_btn.clicked.connect(self.file_parser_status)
        file_parser_layout.addWidget(file_parser_status_btn)

        file_parser_row.setLayout(file_parser_layout)
        layout.addWidget(file_parser_row)

        # NER PARSER
        ner_parser_row = QWidget()
        ner_parser_layout = QHBoxLayout()
        ner_parser_label = QLabel("NER PARSER")
        ner_parser_layout.addWidget(ner_parser_label)

        ner_parser_pid_btn = QPushButton("PID")
        ner_parser_pid_btn.clicked.connect(self.ner_parser_pid)
        ner_parser_layout.addWidget(ner_parser_pid_btn)

        ner_parser_start_btn = QPushButton("START")
        ner_parser_start_btn.clicked.connect(self.ner_parser_start)
        ner_parser_layout.addWidget(ner_parser_start_btn)

        ner_parser_config_btn = QPushButton("CONFIG")
        ner_parser_config_btn.clicked.connect(self.ner_parser_config)
        ner_parser_layout.addWidget(ner_parser_config_btn)

        ner_parser_status_btn = QPushButton("STATUS")
        ner_parser_status_btn.clicked.connect(self.ner_parser_status)
        ner_parser_layout.addWidget(ner_parser_status_btn)

        ner_parser_row.setLayout(ner_parser_layout)
        layout.addWidget(ner_parser_row)

        # SEMANTIC PARSER
        semantic_parser_row = QWidget()
        semantic_parser_layout = QHBoxLayout()
        semantic_parser_label = QLabel("SEMANTIC PARSER")
        semantic_parser_layout.addWidget(semantic_parser_label)

        semantic_parser_pid_btn = QPushButton("PID")
        semantic_parser_pid_btn.clicked.connect(self.semantic_parser_pid)
        semantic_parser_layout.addWidget(semantic_parser_pid_btn)

        semantic_parser_start_btn = QPushButton("START")
        semantic_parser_start_btn.clicked.connect(self.semantic_parser_start)
        semantic_parser_layout.addWidget(semantic_parser_start_btn)

        semantic_parser_config_btn = QPushButton("CONFIG")
        semantic_parser_config_btn.clicked.connect(self.semantic_parser_config)
        semantic_parser_layout.addWidget(semantic_parser_config_btn)

        semantic_parser_status_btn = QPushButton("STATUS")
        semantic_parser_status_btn.clicked.connect(self.semantic_parser_status)
        semantic_parser_layout.addWidget(semantic_parser_status_btn)

        semantic_parser_row.setLayout(semantic_parser_layout)
        layout.addWidget(semantic_parser_row)

        # TOPIC PARSER
        topic_parser_row = QWidget()
        topic_parser_layout = QHBoxLayout()
        topic_parser_label = QLabel("TOPIC PARSER")
        topic_parser_layout.addWidget(topic_parser_label)

        topic_parser_pid_btn = QPushButton("PID")
        topic_parser_pid_btn.clicked.connect(self.topic_parser_pid)
        topic_parser_layout.addWidget(topic_parser_pid_btn)

        topic_parser_start_btn = QPushButton("START")
        topic_parser_start_btn.clicked.connect(self.topic_parser_start)
        topic_parser_layout.addWidget(topic_parser_start_btn)

        topic_parser_config_btn = QPushButton("CONFIG")
        topic_parser_config_btn.clicked.connect(self.topic_parser_config)
        topic_parser_layout.addWidget(topic_parser_config_btn)

        topic_parser_status_btn = QPushButton("STATUS")
        topic_parser_status_btn.clicked.connect(self.topic_parser_status)
        topic_parser_layout.addWidget(topic_parser_status_btn)

        topic_parser_row.setLayout(topic_parser_layout)
        layout.addWidget(topic_parser_row)

        # TANITY
        tanity_row = QWidget()
        tanity_layout = QHBoxLayout()
        tanity_label = QLabel("TANITY")
        tanity_layout.addWidget(tanity_label)

        tanity_pid_btn = QPushButton("PID")
        tanity_pid_btn.clicked.connect(self.tanity_pid)
        tanity_layout.addWidget(tanity_pid_btn)

        tanity_start_btn = QPushButton("START")
        tanity_start_btn.clicked.connect(self.tanity_start)
        tanity_layout.addWidget(tanity_start_btn)

        tanity_config_btn = QPushButton("CONFIG")
        tanity_config_btn.clicked.connect(self.tanity_config)
        tanity_layout.addWidget(tanity_config_btn)

        tanity_status_btn = QPushButton("STATUS")
        tanity_status_btn.clicked.connect(self.tanity_status)
        tanity_layout.addWidget(tanity_status_btn)
        
        tanity_row.setLayout(tanity_layout)
        layout.addWidget(tanity_row)

        # Create the logs section
        logs = QLabel("LOGS")
        layout.addWidget(logs)

        # Create the text area
        self.text_area = QTextEdit()
        layout.addWidget(self.text_area)

        self.setLayout(layout)

    # SETTING
    # def open_settings(self):
    #     self.settings_window = QMainWindow()
    #     self.settings_window.setWindowTitle("Settings")
    #     self.settings_window.setGeometry(0, -100, 600, 400)
    #     self.settings_window.move(QDesktopWidget().availableGeometry().center() - self.settings_window.frameGeometry().center())
       
    #     # 
    #     layout = QVBoxLayout()
    #     self.setLayout(layout)

    #     mongo_ip_label = QLabel("MONGO IP")
    #     mongo_ip_label.setFixedWidth(150)
    #     mongo_ip_input = QLineEdit()
    #     mongo_ip_layout = QHBoxLayout()
    #     mongo_ip_layout.addWidget(mongo_ip_label)
    #     mongo_ip_layout.addWidget(mongo_ip_input)
    #     layout.addLayout(mongo_ip_layout)

    #     database_name_label = QLabel("DATABASE NAME")
    #     database_name_label.setFixedWidth(150)
    #     database_name_input = QLineEdit()
    #     database_name_layout = QHBoxLayout()
    #     database_name_layout.addWidget(database_name_label)
    #     database_name_layout.addWidget(database_name_input)
    #     layout.addLayout(database_name_layout)

    #     backup_path_label = QLabel("DEFAULT BACKUP PATH")
    #     backup_path_label.setFixedWidth(150)
    #     backup_path_input = QLineEdit()
    #     backup_path_layout = QHBoxLayout()
    #     backup_path_layout.addWidget(backup_path_label)
    #     backup_path_layout.addWidget(backup_path_input)
    #     layout.addLayout(backup_path_layout)

    #     mongo_port_label = QLabel("MONGO PORT")
    #     mongo_port_label.setFixedWidth(150)
    #     mongo_port_input = QLineEdit()
    #     mongo_port_layout = QHBoxLayout()
    #     mongo_port_layout.addWidget(mongo_port_label)
    #     mongo_port_layout.addWidget(mongo_port_input)
    #     layout.addLayout(mongo_port_layout)
    #     # 

    #     self.settings_window.show()
    def open_settings(self):
        self.settings_window = QMainWindow()
        self.settings_window.setWindowTitle("Settings")
        self.settings_window.setGeometry(0, -100, 600, 400)
        self.settings_window.move(QDesktopWidget().availableGeometry().center() - self.settings_window.frameGeometry().center())

        central_widget = QWidget(self.settings_window)
        layout = QVBoxLayout(central_widget)
        self.settings_window.setCentralWidget(central_widget)

        mongo_ip_label = QLabel("MONGO IP")
        mongo_ip_label.setFixedWidth(150)
        mongo_ip_input = QLineEdit()
        mongo_ip_layout = QHBoxLayout()
        mongo_ip_layout.addWidget(mongo_ip_label)
        mongo_ip_layout.addWidget(mongo_ip_input)
        layout.addLayout(mongo_ip_layout)

        database_name_label = QLabel("DATABASE NAME")
        database_name_label.setFixedWidth(150)
        database_name_input = QLineEdit()
        database_name_layout = QHBoxLayout()
        database_name_layout.addWidget(database_name_label)
        database_name_layout.addWidget(database_name_input)
        layout.addLayout(database_name_layout)

        backup_path_label = QLabel("DEFAULT BACKUP PATH")
        backup_path_label.setFixedWidth(150)
        backup_path_input = QLineEdit()
        backup_path_layout = QHBoxLayout()
        backup_path_layout.addWidget(backup_path_label)
        backup_path_layout.addWidget(backup_path_input)
        layout.addLayout(backup_path_layout)

        mongo_port_label = QLabel("MONGO PORT")
        mongo_port_label.setFixedWidth(150)
        mongo_port_input = QLineEdit()
        mongo_port_layout = QHBoxLayout()
        mongo_port_layout.addWidget(mongo_port_label)
        mongo_port_layout.addWidget(mongo_port_input)
        layout.addLayout(mongo_port_layout)

        self.settings_window.show()


        # CONFIG
    # def open_config(self):
    #     self.config_window = QMainWindow()
    #     self.config_window.setWindowTitle("Config")
    #     self.config_window.setGeometry(-100, -200, 600, 400)
    #     self.config_window.move(QDesktopWidget().availableGeometry().center() - self.config_window.frameGeometry().center())
    #     self.config_window.show()

    def open_config(self):
        self.config_window = QMainWindow()
        self.config_window.setWindowTitle("Config")
        self.config_window.setGeometry(-100, -200, 600, 400)
        self.config_window.move(QDesktopWidget().availableGeometry().center() - self.config_window.frameGeometry().center())

        central_widget = QWidget(self.config_window)  # Create a central widget
        layout = QVBoxLayout(central_widget)
        self.config_window.setCentralWidget(central_widget)

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

        self.config_window.show()


    def browse_folder(self):
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory()
        self.input_path_input.setText(folder_path)

    def add_to_database(self):
        # Your existing code for adding to the database
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


    # Define the individual functions for each button
    def file_parser_pid(self):
        self.text_area.setText("Clicked on FILE PARSER's PID button")

    def file_parser_start(self):
        self.text_area.setText("Clicked on FILE PARSER's START button")

    def file_parser_config(self):
        self.text_area.setText("Clicked on FILE PARSER's CONFIG button")

    def file_parser_status(self):
        self.text_area.setText("Clicked on FILE PARSER's STATUS button")

    def ner_parser_pid(self):
        self.text_area.setText("Clicked on NER PARSER's PID button")

    def ner_parser_start(self):
        self.text_area.setText("Clicked on NER PARSER's START button")

    def ner_parser_config(self):
        self.text_area.setText("Clicked on NER PARSER's CONFIG button")

    def ner_parser_status(self):
        self.text_area.setText("Clicked on NER PARSER's STATUS button")

    def semantic_parser_pid(self):
        self.text_area.setText("Clicked on SEMANTIC PARSER's PID button")

    def semantic_parser_start(self):
        self.text_area.setText("Clicked on SEMANTIC PARSER's START button")

    def semantic_parser_config(self):
        self.text_area.setText("Clicked on SEMANTIC PARSER's CONFIG button")

    def semantic_parser_status(self):
        self.text_area.setText("Clicked on SEMANTIC PARSER's STATUS button")

    def topic_parser_pid(self):
        self.text_area.setText("Clicked on TOPIC PARSER's PID button")

    def topic_parser_start(self):
        self.text_area.setText("Clicked on TOPIC PARSER's START button")

    def topic_parser_config(self):
        self.text_area.setText("Clicked on TOPIC PARSER's CONFIG button")

    def topic_parser_status(self):
        self.text_area.setText("Clicked on TOPIC PARSER's STATUS button")

    def tanity_pid(self):
        self.text_area.setText("Clicked on TANITY's PID button")

    def tanity_start(self):
        self.text_area.setText("Clicked on TANITY's START button")

    def tanity_config(self):
        self.text_area.setText("Clicked on TANITY's CONFIG button")

    def tanity_status(self):
        self.text_area.setText("Clicked on TANITY's STATUS button")

if __name__ == "__main__":
    app = QApplication([])
    ex = IngestionTool()
    ex.show()
    app.exec_()
