from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
import json

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('SETTINGS')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # DEFAULT VALUES getting from default_config.json
        with open('default_config.json') as f:
            config_val = json.load(f)
        
        default_mongo_port = config_val["default_mongo_port"]
        default_mongo_ip = config_val["default_mongo_ip"]
        default_database_name = config_val["default_database_name"]
        default_backup_path = config_val["default_backup_path"]

 
        # default_mongo_port = "127.0.0.1"
        # default_mongo_ip = "27017"
        # default_database_name = "GARUDA"
        # default_backup_path = "/home/$user/GARUDA/"


        update_reset_layout = QHBoxLayout()
        reset_btn = QPushButton("RESET")
        update_btn = QPushButton("UPDATE")
        update_reset_layout.addWidget(reset_btn)
        update_reset_layout.addWidget(update_btn)
        layout.addLayout(update_reset_layout)

        mongo_port_layout = QHBoxLayout()
        mongo_port_label = QLabel("MONGO PORT")
        mongo_port_label.setFixedWidth(150)
        mongo_port_input = QLineEdit(default_mongo_port)
        mongo_port_btn = QPushButton("UPDATE")
        mongo_port_layout.addWidget(mongo_port_label)
        mongo_port_layout.addWidget(mongo_port_input)
        mongo_port_layout.addWidget(mongo_port_btn)
        layout.addLayout(mongo_port_layout)

        mongo_ip_layout = QHBoxLayout()
        mongo_ip_label = QLabel("MONGO IP")
        mongo_ip_label.setFixedWidth(150)
        mongo_ip_input = QLineEdit(default_mongo_ip)
        mongo_ip_btn = QPushButton("UPDATE")
        mongo_ip_layout.addWidget(mongo_ip_label)
        mongo_ip_layout.addWidget(mongo_ip_input)
        mongo_ip_layout.addWidget(mongo_ip_btn)
        layout.addLayout(mongo_ip_layout)

        database_name_layout = QHBoxLayout()
        database_name_label = QLabel("DATABASE NAME")
        database_name_label.setFixedWidth(150)
        database_name_input = QLineEdit(default_database_name)
        database_name_btn = QPushButton("UPDATE")
        database_name_layout.addWidget(database_name_label)
        database_name_layout.addWidget(database_name_input)
        database_name_layout.addWidget(database_name_btn)
        layout.addLayout(database_name_layout)

        backup_path_layout = QHBoxLayout()
        backup_path_label = QLabel("BACKUP PATH")
        backup_path_label.setFixedWidth(150)
        backup_path_input = QLineEdit(default_backup_path)
        backup_path_btn = QPushButton("UPDATE")
        backup_path_layout.addWidget(backup_path_label)
        backup_path_layout.addWidget(backup_path_input)
        backup_path_layout.addWidget(backup_path_btn)
        layout.addLayout(backup_path_layout)
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
