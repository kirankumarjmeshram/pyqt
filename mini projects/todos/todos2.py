import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QListWidget, QListWidgetItem, QLineEdit, QCheckBox, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(':memory:')
        self.db.open()

        self.query = QSqlQuery()
        self.query.exec_("CREATE TABLE todos (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, completed INTEGER)")

        self.layout = QVBoxLayout()

        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText("Enter task...")
        self.layout.addWidget(self.taskInput)

        self.addButton = QPushButton("Add Task")
        self.addButton.clicked.connect(self.addTask)
        self.layout.addWidget(self.addButton)

        self.todoTable = QTableWidget(0, 3)
        self.todoTable.setHorizontalHeaderLabels(["Task", "Completed", "Actions"])
        self.layout.addWidget(self.todoTable)

        self.setLayout(self.layout)
        self.updateList()

    def addTask(self):
        task = self.taskInput.text()
        if task:
            self.query.exec_(f"INSERT INTO todos (task, completed) VALUES ('{task}', 0)")
            self.taskInput.clear()
            self.updateList()

    def updateList(self):
        self.todoTable.setRowCount(0)
        self.query.exec_("SELECT * FROM todos")
        while self.query.next():
            id = self.query.value(0)
            task = self.query.value(1)
            completed = self.query.value(2)

            checkbox = QCheckBox()
            checkbox.setChecked(bool(completed))
            checkbox.stateChanged.connect(lambda state, id=id: self.markCompleted(id, state))

            deleteButton = QPushButton("Delete")
            deleteButton.clicked.connect(lambda _, id=id: self.deleteTask(id))

            self.todoTable.insertRow(self.todoTable.rowCount())
            self.todoTable.setItem(self.todoTable.rowCount()-1, 0, QTableWidgetItem(task))
            self.todoTable.setCellWidget(self.todoTable.rowCount()-1, 1, checkbox)
            self.todoTable.setCellWidget(self.todoTable.rowCount()-1, 2, deleteButton)

    def markCompleted(self, id, state):
        self.query.exec_(f"UPDATE todos SET completed = {state} WHERE id = {id}")
        self.updateList()

    def deleteTask(self, id):
        self.query.exec_(f"DELETE FROM todos WHERE id = {id}")
        self.updateList()

app = QApplication(sys.argv)
window = ToDoApp()
window.show()
sys.exit(app.exec_())
