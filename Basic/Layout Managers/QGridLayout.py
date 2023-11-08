# g_layout.py

"""Grid layout example."""

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
)

app = QApplication([])
window = QWidget()
window.setWindowTitle("QGridLayout")

layout = QGridLayout()
layout.addWidget(QPushButton("Button (0, 0)"), 0, 0)
layout.addWidget(QPushButton("Button (0, 1)"), 0, 1)
layout.addWidget(QPushButton("Button (0, 2)"), 0, 2)
layout.addWidget(QPushButton("Button (1, 0)"), 1, 0)
layout.addWidget(QPushButton("Button (1, 1)"), 1, 1)
layout.addWidget(QPushButton("Button (1, 2)"), 1, 2)
layout.addWidget(QPushButton("Button (2, 0)"), 2, 0)
layout.addWidget(QPushButton("Button (2, 1) + 2 Columns Span"), 2, 1, 1, 2) # here we pass two more arguments (ie, 1 and 2) to .addWidget(). These arguments are rowSpan(1) and columnSpan(2), and they’re the fourth and fifth arguments passed to the function. You can use them to make a widget occupy more than one row or column
window.setLayout(layout)

window.show()
sys.exit(app.exec())