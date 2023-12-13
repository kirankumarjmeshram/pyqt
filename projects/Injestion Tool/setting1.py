from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('SETTINGS')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

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
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
