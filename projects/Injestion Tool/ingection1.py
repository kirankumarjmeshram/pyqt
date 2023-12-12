from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit

class IngestionTool(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setGeometry(300, 300, 800, 600)  

    def initUI(self):
        layout = QVBoxLayout()

        # Create the top bar
        top_bar = QLabel("INGESTION TOOL")
        layout.addWidget(top_bar)

        # Create the rows
        rows = ["FILE PARSER", "NER PARSER", "SEMANTIC PARSER", "TOPIC PARSER", "TANITY"]
        for row in rows:
            layout.addWidget(self.createRow(row))

        # Create the logs section
        logs = QLabel("LOGS")
        layout.addWidget(logs)

        # Create the text area
        self.text_area = QTextEdit()
        layout.addWidget(self.text_area)

        self.setLayout(layout)

    def createRow(self, label):
        row = QWidget()  # Create a QWidget for the row
        layout = QHBoxLayout()  # Change this to QHBoxLayout

        # Create the label
        row_label = QLabel(label)
        layout.addWidget(row_label)

        # Create the buttons
        # PID Button
        pid_btn = QPushButton("PID")
        pid_btn.clicked.connect(lambda checked, l=label: self.updateLog(l, "PID"))
        layout.addWidget(pid_btn)

        # START Button
        start_btn = QPushButton("START")
        start_btn.clicked.connect(lambda checked, l=label: self.updateLog(l, "START"))
        layout.addWidget(start_btn)

        # CONFIG Button
        config_btn = QPushButton("CONFIG")
        config_btn.clicked.connect(lambda checked, l=label: self.updateLog(l, "CONFIG"))
        layout.addWidget(config_btn)

        # STATUS Button
        status_btn = QPushButton("STATUS")
        status_btn.clicked.connect(lambda checked, l=label: self.updateLog(l, "STATUS"))
        layout.addWidget(status_btn)

        row.setLayout(layout)  # Set the layout of the row QWidget
        return row  # Return the QWidget instead of the layout

    def updateLog(self, label, button):
        self.text_area.setText(f"Clicked on {label} {button} button")

if __name__ == "__main__":
    app = QApplication([])
    ex = IngestionTool()
    ex.show()
    app.exec_()
