import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ежедневные привычки")
        self.setGeometry(100, 100, 400, 400)

        self.habits = []

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel("Введите новую привычку:", self)
        layout.addWidget(self.label)

        #Поле ввода
        self.input = QLineEdit(self)
        layout.addWidget(self.input)

        #Кнопки
        self.add_button = QPushButton("Добавить", self)
        self.add_button.clicked.connect(self.add_habit)
        layout.addWidget(self.add_button)

        self.done_button = QPushButton("Выполнено", self)
        self.done_button.clicked.connect(self.mark_done)
        layout.addWidget(self.done_button)

        #Список привычек
        self.habit_list = QListWidget(self)
        layout.addWidget(self.habit_list)

        central_widget.setLayout(layout)

    def add_habit(self):
        habit_text = self.input.text().strip()
        if habit_text:
            self.habits.append({"name": habit_text, "done": False})
            self.update_list()
            self.input.clear()

    def mark_done(self):
        selected = self.habit_list.currentRow()
        if selected != -1:
            self.habits[selected]["done"] = True
            self.update_list()

    def update_list(self):
        self.habit_list.clear()
        for habit in self.habits:
            text = "✅ " + habit["name"] if habit["done"] else habit["name"]
            self.habit_list.addItem(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
