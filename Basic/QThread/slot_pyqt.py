from PyQt5.QtCore import QObject, pyqtSlot

class MyObject(QObject):
    @pyqtSlot(int)
    def my_slot(self, value):
        print(f"Received value: {value}")

# Usage
obj = MyObject()
obj.my_slot(42)  # This will print "Received value: 42"
