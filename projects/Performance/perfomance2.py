import sys
import psutil
from PyQt5 import QtWidgets
import pyqtgraph as pg
import time

class PerformanceMonitor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a PlotWidget object, which will be the graphical representation of our data
        self.graphWidget = pg.PlotWidget()

        # Set the PlotWidget as the central widget of the QMainWindow
        self.setCentralWidget(self.graphWidget)

        # Initialize x and y data lists
        self.x = list(range(100))  # 100 time points
        self.y = [0 for _ in range(100)]  # 100 data points

        # Create a line at the PlotWidget with our data
        self.data_line =  self.graphWidget.plot(self.x, self.y)  

    def update_graph(self):
        # Get the current CPU usage percentage
        cpu_percent = psutil.cpu_percent()

        # Shift y data in the array one sample left (discard oldest sample)
        self.y = self.y[1:]  

        # Append the new data to the array
        self.y.append(cpu_percent)  

        # Update the data of the line object
        self.data_line.setData(self.x, self.y)  

def main():
    # Create a QApplication object, which is used for event handling and overall management of the GUI application
    app = QtWidgets.QApplication(sys.argv)

    # Create an instance of our class
    main = PerformanceMonitor()

    # Show the instance
    main.show()

    # Create a QTimer object
    timer = pg.QtCore.QTimer()

    # Connect the QTimer timeout signal (which is emitted every x milliseconds, x being the interval we set on it) to our update function
    timer.timeout.connect(main.update_graph)

    # Start the timer with an interval of 1000 milliseconds (1 second)
    timer.start(1000)  

    # Enter the application main loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
