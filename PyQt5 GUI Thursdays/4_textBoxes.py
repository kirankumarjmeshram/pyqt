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
        my_label = qtw.QLabel('Pick Something')
        
        #change font size
        my_label.setFont(qtg.QFont('Helvetica',18))

        self.layout().addWidget(my_label)

        #create an spin box
        # my_spin = qtw.QSpinBox(self,
        #                        value=10,
        #                        maximum=100,
        #                        minimum=0,
        #                        singleStep=5,
        #                        prefix='# ',
        #                        suffix=" Order") 
        
        # for non whole number
        my_spin = qtw.QDoubleSpinBox(self,
                               value=10,
                               maximum=100,
                               minimum=0,
                               singleStep=5.33,
                               prefix='# ',
                               suffix=" Order") 
        
        my_spin.setFont(qtg.QFont('Helvetica',34))

        

        # Put spinbox on the screen
        self.layout().addWidget(my_spin)


        # Create a button
        my_button = qtw.QPushButton('Press Me!', 
                                    clicked = lambda: press_it())
        self.layout().addWidget(my_button)


        self.show()

        def press_it():
            #add name to label
            my_label.setText(f'You Picked {my_spin.value()} Orderd!') #my_spincurrentText()
            #my_label.setText(f'You Picked {my_spin.currentData()}!') # return current data / 2nd argument ie "Something" from  my_spin.addItem("Pepperoni","Something")
            #my_label.setText(f'You Picked {my_spin.currentIndex()}!') # return index of the item

app = qtw.QApplication([])
mw = MainWindow()

# Run The App
app.exec_()
