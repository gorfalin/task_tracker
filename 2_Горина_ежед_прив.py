import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import QDate

class PlaceholderLineEdit(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.placeholder = placeholder
        self.setText(placeholder)
        self.default_font = self.font()
        self.placeholder_font = self.font()
        self.placeholder_font.setItalic(True)
        self.setFont(self.placeholder_font)
        self.setStyleSheet("color: gray;")
        self.is_placeholder = True

        self.textEdited.connect(self.on_text_edited)

    def on_text_edited(self, text):
        if self.is_placeholder and text != "":
            self.clear()
            self.setFont(self.default_font)
            self.setStyleSheet("color: black;")
            self.is_placeholder = False
        elif not self.is_placeholder and text == "":
            self.setText(self.placeholder)
            self.setFont(self.placeholder_font)
            self.setStyleSheet("color: gray;")
            self.is_placeholder = True

    def focusInEvent(self, event):
        if self.is_placeholder:
            self.clear()
            self.setFont(self.default_font)
            self.setStyleSheet("color: black;")
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        if self.text() == "":
            self.setText(self.placeholder)
            self.setFont(self.placeholder_font)
            self.setStyleSheet("color: gray;")
            self.is_placeholder = True
        super().focusOutEvent(event)


class DataApp(QMainWindow):
    FILE_NAME = "habits.json"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Работа с данными")
        self.setGeometry(100, 100, 400, 300)

        self.habits = self.load_from_file()

        self.input = PlaceholderLineEdit("Введите привычку")
        self.label = QLabel("Сохранённые привычки:")
        self.list_label = QLabel()
        self.add_button = QPushButton("Добавить")
        self.save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.label)
        layout.addWidget(self.list_label)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.add_button.clicked.connect(self.add_habit)
        self.save_button.clicked.connect(self.save_to_file)

        self.update_list_display()

    def add_habit(self):
        name = self.input.text().strip()
        if name and name != "Введите привычку":
            key = f"{QDate.currentDate().year()}-{QDate.currentDate().month()}"
            if key not in self.habits:
                self.habits[key] = []
            self.habits[key].append({"name": name})
            self.input.clear()
            self.update_list_display()

    def update_list_display(self):
        key = f"{QDate.currentDate().year()}-{QDate.currentDate().month()}"
        habits = self.habits.get(key, [])
        text = "\n".join([h["name"] for h in habits])
        self.list_label.setText(text if text else "Нет добавленных привычек")

    def save_to_file(self):
        with open(self.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.habits, f, ensure_ascii=False, indent=4)
        self.statusBar().showMessage("Данные сохранены в файл")

    def load_from_file(self):
        try:
            with open(self.FILE_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataApp()
    window.show()
    sys.exit(app.exec_())
