import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel
from PyQt5.QtCore import QProcess
from datetime import datetime 
import os

class CommandApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # create widgets
        self.cmd_label = QLabel("Add Command:")
        self.command_line = QLineEdit()
        self.run_button = QPushButton("Run")
        self.output_box = QTextEdit()
        self.path_label = QLabel("Folder path:")
        self.path_line = QLineEdit()

        # layout widgets
        layout = QVBoxLayout()
        layout.addWidget(self.cmd_label)
        layout.addWidget(self.command_line)
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_line)
        layout.addWidget(self.run_button)
        layout.addWidget(self.output_box)
        self.setLayout(layout)

        # connect signals and slots
        self.run_button.clicked.connect(self.run_command)
        self.show()

    def run_command(self):
        # get the command and the folder path from the line edits
        command = self.command_line.text()
        folder_path = self.path_line.text()
        if command and folder_path:
            # create a QProcess object
            self.process = QProcess()
            # connect the signals for output and error
            self.process.readyReadStandardOutput.connect(self.read_output)
            self.process.readyReadStandardError.connect(self.read_error)
            # start the process with the given command
            self.process.start(command)
            # create a file name with the command and the current date and time
            file_name = f"{command.replace(' ', '_')}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            # open the file in append mode
            self.file = open(os.path.join(folder_path, file_name), "a")

    def read_output(self):
        # read the standard output from the process
        output = self.process.readAllStandardOutput().data().decode()
        # append the output to the text box and the file
        self.output_box.append(output)
        self.file.write(output)

    def read_error(self):
        # read the standard error from the process
        error = self.process.readAllStandardError().data().decode()
        # append the error to the text box and the file
        self.output_box.append(error)
        self.file.write(error)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CommandApp()
    sys.exit(app.exec_())
