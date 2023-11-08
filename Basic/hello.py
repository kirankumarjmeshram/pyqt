# hello.py

"""Simple Hello, World example with PyQt6."""

import sys

# 1. Import QApplication and all the required widgets
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

# 2. Create an instance of QApplication
app = QApplication([])

# 3. Create your application's GUI
window = QWidget()
window.setWindowTitle("PyQt App")
window.setGeometry(100, 100, 280, 80)   # to define the window’s size and screen position. The first two arguments are the x and y screen coordinates where the window will be placed. The third and fourth arguments are the window’s width and height.
helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
helloMsg.move(60, 15) #  .move() to place helloMsg at the coordinates (60, 15) on the application’s window.

# 4. Show your application's GUI
window.show()  # .show() schedules a paint event, which is a request to paint the widgets that compose a GUI

# 5. Run your application's event loop
sys.exit(app.exec()) # you start the application’s event loop by calling .exec(). The call to .exec() is wrapped in a call to sys.exit(), which allows you to cleanly exit Python and release memory resources when the application terminates