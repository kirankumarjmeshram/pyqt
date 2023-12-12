from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QStackedWidget

class IngestionTool(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setGeometry(300, 300, 800, 600)  

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

        # Create the stacked widget
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Create the main page
        self.main_page = QWidget()
        main_layout = QVBoxLayout()

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
        main_layout.addWidget(file_parser_row)

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
        main_layout.addWidget(ner_parser_row)

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
        main_layout.addWidget(semantic_parser_row)

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
        main_layout.addWidget(topic_parser_row)

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
        main_layout.addWidget(tanity_row)

        # Create the logs section
        logs = QLabel("LOGS")
        main_layout.addWidget(logs)

        # Create the text area
        self.text_area = QTextEdit()
        main_layout.addWidget(self.text_area)

        self.main_page.setLayout(main_layout)
        self.stacked_widget.addWidget(self.main_page)

        self.setLayout(layout)

    def open_settings(self):
        settings_page = QWidget()
        settings_layout = QVBoxLayout()
        back_btn = QPushButton("BACK")
        back_btn.clicked.connect(self.go_back)
        settings_layout.addWidget(back_btn)
        settings_label = QLabel("Settings content goes here.")
        settings_layout.addWidget(settings_label)
        settings_page.setLayout(settings_layout)
        self.stacked_widget.addWidget(settings_page)
        self.stacked_widget.setCurrentWidget(settings_page)

    def open_config(self):
        config_page = QWidget()
        config_layout = QVBoxLayout()
        back_btn = QPushButton("BACK")
        back_btn.clicked.connect(self.go_back)
        config_layout.addWidget(back_btn)
        config_label = QLabel("Config content goes here.")
        config_layout.addWidget(config_label)
        config_page.setLayout(config_layout)
        self.stacked_widget.addWidget(config_page)
        self.stacked_widget.setCurrentWidget(config_page)

    def go_back(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

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
