import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        #Add a title
        self.setWindowTitle("Hello World")

        #Set layout
        #vertical box layout QVBoxLayout 
        # horizontal QHBoxLayout
        self.setLayout(qtw.QVBoxLayout())

        #  label
        my_label = qtw.QLabel('Hello World')
        
        #change font size
        my_label.setFont(qtg.QFont('Helvetica',24))

        self.layout().addWidget(my_label)


        self.show()

app = qtw.QApplication([])
mw = MainWindow()

# Run The App
app.exec_()
