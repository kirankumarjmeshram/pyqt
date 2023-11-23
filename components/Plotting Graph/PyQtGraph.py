#https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
import sys
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Temperature vs time plot
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)

        #Styling
        self.plot_graph.setBackground("w") # gackground color
        # pen = pg.mkPen(color=(255, 0, 0)) # line color
        pen = pg.mkPen(color=(255, 0, 0), width=5, style=QtCore.Qt.DashLine)
        # You can use all other Qt's line styles, including Qt.SolidLine, Qt.DotLine, Qt.DashDotLine, and Qt.DashDotDotLine. 
        
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        # self.plot_graph.plot(time, temperature)
        self.plot_graph.plot(time, temperature, pen = pen)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

