from PyQt5.QtCore import QTimer, QCoreApplication, QObject, QThread

class Worker(QObject):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.my_function)
        self.timer.start(1000)  # Timer will trigger my_function every 1 second

    def my_function(self):
        print("1 second has passed!")

class MyThread(QThread):
    def __init__(self):
        super().__init__()
        self.worker = Worker()

    def run(self):
        self.worker.moveToThread(self)
        self.started.connect(self.worker.my_function)

app = QCoreApplication([])
thread = MyThread()
thread.start()

# Add a QTimer to stop the application after 1 minute
quit_timer = QTimer()
quit_timer.singleShot(60000, app.quit)

app.exec_()
