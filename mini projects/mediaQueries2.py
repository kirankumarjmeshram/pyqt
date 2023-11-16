import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.button = QPushButton('Click me!', self)
        layout.addWidget(self.button)

        self.setLayout(layout)

        # Set initial styles for the button
        self.updateButtonStyle()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Styled Button Example')
        self.show()

    def updateButtonStyle(self):
        # Adjust styles based on window width
        width = self.width()

        if width < 400:
            style = """
                QPushButton {
                    font-size: 12px;
                    background-color: #3498db;
                    color: #ffffff;
                    border: 2px solid #3498db;
                    border-radius: 5px;
                    padding: 10px;
                    width: 100px;
                }

                QPushButton:hover {
                    background-color: #2980b9;
                    border: 2px solid #2980b9;
                }
            """
        elif 400 <= width < 600:
            style = """
                QPushButton {
                    font-size: 14px;
                    background-color: #2ecc71;
                    color: #ffffff;
                    border: 2px solid #2ecc71;
                    border-radius: 5px;
                    padding: 10px;
                    width: 150px;
                }

                QPushButton:hover {
                    background-color: #27ae60;
                    border: 2px solid #27ae60;
                }
            """
        else:
            style = """
                QPushButton {
                    font-size: 16px;
                    background-color: #e74c3c;
                    color: #ffffff;
                    border: 2px solid #e74c3c;
                    border-radius: 5px;
                    padding: 10px;
                    width: 200px;
                }

                QPushButton:hover {
                    background-color: #c0392b;
                    border: 2px solid #c0392b;
                }
            """

        self.button.setStyleSheet(style)

    def resizeEvent(self, event):
        # Reapply styles when the window is resized
        self.updateButtonStyle()

def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
