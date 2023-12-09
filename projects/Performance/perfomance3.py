import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal, QTimer


class PerformanceThread(QThread):
    """Thread to collect system performance data."""
    dataReady = pyqtSignal(dict)

    def run(self):
        while True:
            data = {
                "cpu_usage": psutil.cpu_percent(),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage("/").percent,
            }
            self.dataReady.emit(data)
            self.sleep(1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window title
        self.setWindowTitle("System Performance Monitor")

        # Layout
        layout = QVBoxLayout()

        # CPU Progress Bar
        cpu_layout = QHBoxLayout()
        cpu_layout.addWidget(QLabel("CPU Usage:"))
        self.cpu_progress_bar = QProgressBar()
        self.cpu_progress_bar.setMaximum(100)
        cpu_layout.addWidget(self.cpu_progress_bar)
        layout.addLayout(cpu_layout)

        # Memory Progress Bar
        memory_layout = QHBoxLayout()
        memory_layout.addWidget(QLabel("Memory Usage:"))
        self.memory_progress_bar = QProgressBar()
        self.memory_progress_bar.setMaximum(100)
        memory_layout.addWidget(self.memory_progress_bar)
        layout.addLayout(memory_layout)

        # Disk Progress Bar
        disk_layout = QHBoxLayout()
        disk_layout.addWidget(QLabel("Disk Usage:"))
        self.disk_progress_bar = QProgressBar()
        self.disk_progress_bar.setMaximum(100)
        disk_layout.addWidget(self.disk_progress_bar)
        layout.addLayout(disk_layout)

        # Performance thread
        self.performance_thread = PerformanceThread()
        self.performance_thread.dataReady.connect(self.update_performance)
        self.performance_thread.start()

        # Timer to update progress bars
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_progress_bars)
        self.timer.start()

        # Set main layout
        self.setLayout(layout)

    def update_performance(self, data):
        self.cpu_progress_bar.setValue(data["cpu_usage"])
        self.memory_progress_bar.setValue(data["memory_usage"])
        self.disk_progress_bar.setValue(data["disk_usage"])

    def update_progress_bars(self):
        self.cpu_progress_bar.update()
        self.memory_progress_bar.update()
        self.disk_progress_bar.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
