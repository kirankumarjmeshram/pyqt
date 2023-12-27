import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt5.QtCore import QProcess

class CommandApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # create widgets
        self.command_line = QLineEdit()
        self.run_button = QPushButton("Run")
        self.output_box = QTextEdit()

        # layout widgets
        layout = QVBoxLayout()
        layout.addWidget(self.command_line)
        layout.addWidget(self.run_button)
        layout.addWidget(self.output_box)
        self.setLayout(layout)

        # connect signals and slots
        self.run_button.clicked.connect(self.run_command)
        self.show()

    def run_command(self):
        # get the command from the line edit
        command = self.command_line.text()
        if command:
            # create a QProcess object
            self.process = QProcess()
            # connect the signals for output and error
            self.process.readyReadStandardOutput.connect(self.read_output)
            self.process.readyReadStandardError.connect(self.read_error)
            # start the process with the given command
            self.process.start(command)

    def read_output(self):
        # read the standard output from the process
        output = self.process.readAllStandardOutput().data().decode()
        # append the output to the text box
        self.output_box.append(output)

    def read_error(self):
        # read the standard error from the process
        error = self.process.readAllStandardError().data().decode()
        # append the error to the text box
        self.output_box.append(error)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CommandApp()
    sys.exit(app.exec_())
