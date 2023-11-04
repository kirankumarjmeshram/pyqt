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
        my_label = qtw.QLabel('Pick Something From THe List')
        
        #change font size
        my_label.setFont(qtg.QFont('Helvetica',24))

        self.layout().addWidget(my_label)

        #create an combo box
        my_combo = qtw.QComboBox(self,
                                 editable = True,
                                 insertPolicy = qtw.QComboBox.InsertAtTop) #insertPolicy = qtw.QComboBox.InsertAtBottom

        # add items to the combo box
        my_combo.addItem("Pepperoni","Something")
        my_combo.addItem("Cheese", 1)
        my_combo.addItem("Mushroom", qtw.QWidget)
        my_combo.addItem("Peppers")
        my_combo.addItems(["one", "two", "three"]) #addItems => it will disply all the elements of arr in option 
        my_combo.insertItem(2,"Third thing") # "Third thing" will shown on 3rd place of list ie. 2nd index
        my_combo.insertItems(3,["four", "five", "six"])
        # "Something", 1, qtw.QWidget, None are data => my_label.setText(f'You Picked {my_combo.currentData()}!')
        

        # Put combobox on the screen
        self.layout().addWidget(my_combo)


        # Create a button
        my_button = qtw.QPushButton('Press Me!', clicked = lambda: press_it())
        self.layout().addWidget(my_button)


        self.show()

        def press_it():
            #add name to label
            my_label.setText(f'You Picked {my_combo.currentText()}!')
            #my_label.setText(f'You Picked {my_combo.currentData()}!') # return current data / 2nd argument ie "Something" from  my_combo.addItem("Pepperoni","Something")
            #my_label.setText(f'You Picked {my_combo.currentIndex()}!') # return index of the item

app = qtw.QApplication([])
mw = MainWindow()

# Run The App
app.exec_()
