import sys
import shutil
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

class FileOperationThread(QThread):
    update_speed = pyqtSignal(float)

    def __init__(self, source, destination, operation):
        super().__init__()
        self.source = source
        self.destination = destination
        self.operation = operation

    def run(self):
        start_time = time.time()

        if self.operation == "copy":
            try:
                shutil.copy2(self.source, self.destination)
            except FileNotFoundError as e:
                print("FileNotFoundError:", e)
            except Exception as e:
                print("Error:", e)

        elif self.operation == "move":
            try:
                shutil.move(self.source, self.destination)
            except FileNotFoundError as e:
                print("FileNotFoundError:", e)
            except Exception as e:
                print("Error:", e)

        end_time = time.time()
        elapsed_time = end_time - start_time
        file_size = self.get_file_size(self.source)

        if elapsed_time > 0:
            speed_mbps = file_size / (elapsed_time * 1024 * 1024)
            self.update_speed.emit(speed_mbps)

    def get_file_size(self, file_path):
        file_size = 0
        try:
            file_size = os.path.getsize(file_path)
        except FileNotFoundError as e:
            print("FileNotFoundError:", e)
        except Exception as e:
            print("Error:", e)
        return file_size

class FileMoverApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 400, 250)
        self.setWindowTitle("File Mover")

        self.input1_label = QLabel('Source Path:', self)
        self.input1_label.move(20, 20)
        self.input1 = QLineEdit(self)
        self.input1.setGeometry(120, 20, 200, 25)

        self.browse_btn1 = QPushButton('Browse', self)
        self.browse_btn1.setGeometry(330, 20, 60, 25)
        self.browse_btn1.clicked.connect(self.browse_source)

        self.input2_label = QLabel('Destination Path:', self)
        self.input2_label.move(20, 60)
        self.input2 = QLineEdit(self)
        self.input2.setGeometry(120, 60, 200, 25)

        self.browse_btn2 = QPushButton('Browse', self)
        self.browse_btn2.setGeometry(330, 60, 60, 25)
        self.browse_btn2.clicked.connect(self.browse_destination)

        self.copy_btn = QPushButton('Copy', self)
        self.copy_btn.setGeometry(120, 100, 80, 30)
        self.copy_btn.clicked.connect(self.copy_files)

        self.move_btn = QPushButton('Move', self)
        self.move_btn.setGeometry(230, 100, 80, 30)
        self.move_btn.clicked.connect(self.move_files)

        self.progress_label = QLabel('Progress:', self)
        self.progress_label.move(20, 150)
        self.progress = QProgressBar(self)
        self.progress.setGeometry(120, 150, 270, 25)

        self.speed_label = QLabel('Speed: 0 MBps', self)
        self.speed_label.move(20, 180)

        self.operation_thread = None
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(1000)  # Update every 1 second

    def browse_source(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, False)
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            self.input1.setText(file_paths[0])

    def browse_destination(self):
        folder_dialog = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_dialog:
            self.input2.setText(folder_dialog)

    def copy_files(self):
        self.progress.setValue(0)
        source_path = self.input1.text()
        destination_path = self.input2.text()

        if self.operation_thread and self.operation_thread.isRunning():
            return

        self.operation_thread = FileOperationThread(source_path, destination_path, "copy")
        self.operation_thread.update_speed.connect(self.update_speed_label)
        self.operation_thread.start()

    def move_files(self):
        self.progress.setValue(0)
        source_path = self.input1.text()
        destination_path = self.input2.text()

        if self.operation_thread and self.operation_thread.isRunning():
            return

        self.operation_thread = FileOperationThread(source_path, destination_path, "move")
        self.operation_thread.update_speed.connect(self.update_speed_label)
        self.operation_thread.start()

    def update_speed_label(self, speed_mbps):
        self.speed_label.setText(f"Speed: {speed_mbps:.2f} MBps")

    def update_progress(self):
        if self.operation_thread and self.operation_thread.isRunning():
            source_path = self.input1.text()
            file_size = self.operation_thread.get_file_size(source_path)
            copied_size = file_size - self.operation_thread.get_file_size(source_path)
            progress_percentage = int((copied_size / file_size) * 100) if file_size > 0 else 0
            self.progress.setValue(progress_percentage)

def main():
    app = QApplication(sys.argv)
    file_mover = FileMoverApp()
    file_mover.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
