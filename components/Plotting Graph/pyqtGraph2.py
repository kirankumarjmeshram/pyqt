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
        # Plot Tiles
        # self.plot_graph.setTitle("Temperature vs Time")
        # self.plot_graph.setTitle("Temperature vs Time", color="b", size="20pt")
         # USING basic HTML syntax and CSS
        self.plot_graph.setTitle(
            '<span style="color: blue; font-size: 20pt">Temperature vs Time</span>'
        )
        self.plot_graph.setBackground("w") # gackground color

        # AXIS LABELS (x,y axis)
        # self.plot_graph.setLabel("left", "Temperature (°C)")
        # self.plot_graph.setLabel("bottom", "Time (min)")

        # styles = {"color": "red", "font-size": "18px"}
        # self.plot_graph.setLabel("left", "Temperature (°C)", **styles)
        # self.plot_graph.setLabel("bottom", "Time (min)", **styles)
        # USING basic HTML syntax and CSS
        self.plot_graph.setLabel(
        "left",
        '<span style="color: red; font-size: 18px">Temperature (°C)</span>'
        )
        self.plot_graph.setLabel(
        "bottom",
        '<span style="color: red; font-size: 18px">Time (min)</span>'
        )
      
       #
        pen = pg.mkPen(color=(255, 0, 0), width=5)
        # You can use all other Qt's line styles, including Qt.SolidLine, Qt.DotLine, Qt.DashDotLine, and Qt.DashDotDotLine. 
        
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        # self.plot_graph.plot(time, temperature)
        # self.plot_graph.plot(time, temperature, symbol="+") #symbol argument :=> tells PyQtGraph to use that symbol as a marker for the points in your plot
        self.plot_graph.plot(
                time,
                temperature,
                pen=pen,
                symbol="+",
                symbolSize=20,
                symbolBrush="b",
            )
        # also use the symbolSize, symbolBrush, and symbolPen arguments to further customize the marker.

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

