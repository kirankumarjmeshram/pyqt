import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        button = QPushButton('Click me!', self)
        layout.addWidget(button)

        self.setLayout(layout)

        # Set initial styles
        self.setStyleSheet("""
            QPushButton {
                font-size: 16px;
            }
        """)

        # Check the screen width and apply styles accordingly
        screen_width = self.geometry().width()
        if screen_width < 800:
            self.setStyleSheet("""
                QPushButton {
                    font-size: 12px;
                }
            """)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Media Queries Example')
        self.show()

    # def resizeEvent(self, event):
    #     # Reapply styles when the window is resized
    #     screen_width = self.geometry().width()
    #     if screen_width < 800:
    #         self.setStyleSheet("""
    #             QPushButton {
    #                 font-size: 12px;
    #             }
    #         """)
    #     elif screen_width < 1000:
    #         self.setStyleSheet("""
    #             QPushButton {
    #                 font-size: 32px;
    #             }
    #         """)
    #     elif screen_width < 1200:
    #         self.setStyleSheet("""
    #             QPushButton {
    #                 font-size: 62px;
    #             }
    #         """)
    #     else:
    #         self.setStyleSheet("""
    #             QPushButton {
    #                 font-size: 86px;
    #             }
    #         """)

        # button.setStyleSheet("""
        #     QPushButton {
        #         font-size: 16px;
        #         background-color: #3498db;
        #         color: #ffffff;
        #         border: 2px solid #3498db;
        #         border-radius: 5px;
        #         padding: 5px;
        #     }

        #     QPushButton:hover {
        #         background-color: #2980b9;
        #         border: 2px solid #2980b9;
        #     }
        # """)

        # def updateButtonStyle(self):
        # # Adjust styles based on window width
        #     if self.width() < 400:
        #         style = """
        #             QPushButton {
        #                 font-size: 12px;
        #                 background-color: #3498db;
        #                 color: #ffffff;
        #                 border: 2px solid #3498db;
        #                 border-radius: 5px;
        #                 padding: 5px;
        #             }

        #             QPushButton:hover {
        #                 background-color: #2980b9;
        #                 border: 2px solid #2980b9;
        #             }
        #         """
        #     else:
        #         style = """
        #             QPushButton {
        #                 font-size: 56px;
        #                 background-color: #3498db;
        #                 color: #ffffff;
        #                 border: 2px solid #3498db;
        #                 border-radius: 5px;
        #                 padding: 5px;
        #             }

        #             QPushButton:hover {
        #                 background-color: #2980b9;
        #                 border: 2px solid #2980b9;
        #             }
        #         """

        #     self.button.setStyleSheet(style)

def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
