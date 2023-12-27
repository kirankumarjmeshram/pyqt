import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyQt Database App')
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.inputprocess_input = QLineEdit()
        self.outputprocess_input = QLineEdit()

        self.add_button = QPushButton('Add Data')
        self.add_button.clicked.connect(self.add_data)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Input Process', 'Output Process'])

        input_label = QLabel('Input Process :')
        output_label = QLabel('Output Process :')
        # main_layout.addWidget(url_label)
        self.layout.addWidget(input_label)
        self.layout.addWidget(self.inputprocess_input)
        self.layout.addWidget(output_label)
        self.layout.addWidget(self.outputprocess_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.table)

        self.central_widget.setLayout(self.layout)

        self.update_data_table()

    def add_data(self):
        inputprocess = self.inputprocess_input.text()
        outputprocess = self.outputprocess_input.text()
        if inputprocess and outputprocess:
            data = {'inputprocess': inputprocess, 'outputprocess': outputprocess}
            try:
                headers = {'Content-Type': 'application/json'}
                response = requests.post('http://127.0.0.1:5005/add', json=data, headers=headers)
                if response.status_code == 201:  # Check for 201 Created status code
                    self.inputprocess_input.clear()
                    self.outputprocess_input.clear()
                    self.update_data_table()
                else:
                    print(f'Error: {response.status_code} - {response.text}')
            except requests.RequestException as e:
                print(f'Error: {e}')

    def update_data_table(self):
        try:
            response = requests.get('http://127.0.0.1:5005/getall')
            if response.status_code == 200:
                data = response.json()
                self.table.setRowCount(len(data))
                for row, entry in enumerate(data):
                    item1 = QTableWidgetItem(entry['inputprocess'])
                    item2 = QTableWidgetItem(entry['outputprocess'])
                    self.table.setItem(row, 0, item1)
                    self.table.setItem(row, 1, item2)
                self.table.resizeColumnsToContents()
            else:
                print(f'Error: {response.status_code} - {response.text}')
        except requests.RequestException as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
