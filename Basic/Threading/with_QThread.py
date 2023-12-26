import sys
from time import sleep
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Step 1: Create a worker class
class Worker(QObject):
    # WORKER'S SIGNALS (finished and progress)
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    # THIS IS THE MAIN FUNCTION FOR OUR APP
    def run(self):
        """Long-running task."""
        for i in range(5):
            sleep(1)
            self.progress.emit(i + 1)
        self.finished.emit()

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()

        self.setGeometry(300,300, 500, 300)
        

    def setupUi(self):
        self.setWindowTitle("Freezing GUI")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        layout = QVBoxLayout()

        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        layout.addWidget(self.clicksLabel)
        
        self.countBtn = QPushButton("Click me!", self)
        layout.addWidget(self.countBtn)

        # layout.addStretch()
        self.stepLabel = QLabel("Long-Running Step: 0")
        layout.addWidget(self.stepLabel)
        self.countBtn.clicked.connect(self.countClicks)

        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        layout.addWidget(self.longRunningBtn)
        self.longRunningBtn.clicked.connect(self.runLongTask)

        self.centralWidget.setLayout(layout)

    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    def reportProgress(self, n):
        self.stepLabel.setText(f"Long-Running Step: {n}")

    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )
app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())