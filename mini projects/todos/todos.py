import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QListWidget, QListWidgetItem, QLineEdit
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('mydb:')
        self.db.open()

        self.query = QSqlQuery()
        self.query.exec_("CREATE TABLE todos (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)")

        self.layout = QVBoxLayout()

        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText("Enter task...")
        self.layout.addWidget(self.taskInput)

        self.addButton = QPushButton("Add Task")
        self.addButton.clicked.connect(self.addTask)
        self.layout.addWidget(self.addButton)

        self.todoList = QListWidget()
        self.layout.addWidget(self.todoList)

        self.setLayout(self.layout)
        self.updateList()

    def addTask(self):
        task = self.taskInput.text()
        if task:
            self.query.exec_(f"INSERT INTO todos (task) VALUES ('{task}')")
            self.taskInput.clear()
            self.updateList()

    def updateList(self):
        self.todoList.clear()
        self.query.exec_("SELECT * FROM todos")
        while self.query.next():
            id = self.query.value(0)
            task = self.query.value(1)
            item = QListWidgetItem(task)
            item.setData(256, id)
            self.todoList.addItem(item)

app = QApplication(sys.argv)
window = ToDoApp()
window.show()
sys.exit(app.exec_())
