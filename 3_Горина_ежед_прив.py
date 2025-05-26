import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QLineEdit, QTabWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QDate


class PlaceholderLineEdit(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.placeholder = placeholder
        self.setText(placeholder)
        self.setStyleSheet("color: gray;")
        self.default_text = placeholder

        self.textEdited.connect(self.on_text_edited)

    def on_text_edited(self, text):
        if text == "":
            self.setText(self.placeholder)
            self.setStyleSheet("color: gray;")
        else:
            self.setStyleSheet("color: black;")


class MainWindow(QMainWindow):
    FILE_NAME = "habits.json"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ежедневные привычки")
        self.setGeometry(100, 100, 600, 400)

        # Данные
        self.habits = self.load_from_file()
        self.current_month = QDate.currentDate().month()
        self.current_year = QDate.currentDate().year()

        # Вкладки
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Вкладка "Привычки"
        self.tab_habits = QWidget()
        self.init_tab_habits()
        self.tabs.addTab(self.tab_habits, "Привычки")

        # Вкладка "Статистика"
        self.tab_stats = QWidget()
        self.init_tab_stats()
        self.tabs.addTab(self.tab_stats, "Статистика")

        # Вкладка "Настройки"
        self.tab_settings = QWidget()
        self.init_tab_settings()
        self.tabs.addTab(self.tab_settings, "Настройки")

    def init_tab_habits(self):
        layout = QVBoxLayout()

        # Месяц и стрелки
        month_layout = QHBoxLayout()
        self.btn_prev = QPushButton("←")
        self.btn_next = QPushButton("→")
        self.lbl_month = QLabel()
        self.lbl_month.setAlignment(Qt.AlignCenter)
        self.update_month_label()

        self.btn_prev.clicked.connect(self.prev_month)
        self.btn_next.clicked.connect(self.next_month)

        month_layout.addWidget(self.btn_prev)
        month_layout.addWidget(self.lbl_month)
        month_layout.addWidget(self.btn_next)

        # Список привычек
        self.list_habits = QListWidget()

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.btn_done = QPushButton("Выполнено")
        self.btn_delete = QPushButton("Удалить")

        self.btn_done.clicked.connect(self.mark_done)
        self.btn_delete.clicked.connect(self.delete_habit)

        btn_layout.addWidget(self.btn_done)
        btn_layout.addWidget(self.btn_delete)

        # Поле ввода и кнопка добавления
        add_layout = QHBoxLayout()
        self.input_new = PlaceholderLineEdit("Новая привычка...")
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_habit)

        add_layout.addWidget(self.input_new)
        add_layout.addWidget(self.btn_add)

        # Макет
        layout.addLayout(month_layout)
        layout.addWidget(self.list_habits)
        layout.addLayout(btn_layout)
        layout.addLayout(add_layout)

        self.tab_habits.setLayout(layout)
        self.load_habits()

    def update_month_label(self):
        month_name = QDate.longMonthName(self.current_month)
        year = self.current_year
        self.lbl_month.setText(f"{month_name} {year}")

    def get_month_key(self):
        return f"{self.current_year}-{self.current_month}"

    def load_habits(self):
        key = self.get_month_key()
        if key not in self.habits:
            self.habits[key] = []

        self.list_habits.clear()
        for habit in self.habits[key]:
            text = "✅ " + habit["name"] if habit.get("done", False) else habit["name"]
            self.list_habits.addItem(text)

    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_month_label()
        self.load_habits()

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.update_month_label()
        self.load_habits()

    def mark_done(self):
        selected = self.list_habits.currentRow()
        if selected == -1:
            return

        key = self.get_month_key()
        habit = self.habits[key][selected]
        habit["done"] = True
        self.save_to_file()
        self.load_habits()

    def delete_habit(self):
        selected = self.list_habits.currentRow()
        if selected == -1:
            return

        reply = QMessageBox.question(
            self, 'Удаление', 'Вы уверены, что хотите удалить эту привычку?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            key = self.get_month_key()
            del self.habits[key][selected]
            self.save_to_file()
            self.load_habits()

    def add_habit(self):
        name = self.input_new.text().strip()
        if name == "" or name == "Новая привычка...":
            return

        key = self.get_month_key()
        self.habits[key].append({"name": name})
        self.save_to_file()
        self.input_new.setText("")
        self.load_habits()

    def init_tab_stats(self):
        layout = QVBoxLayout()
        label = QLabel("Здесь будет статистика...", alignment=Qt.AlignCenter)
        layout.addWidget(label)
        self.tab_stats.setLayout(layout)

    def init_tab_settings(self):
        layout = QVBoxLayout()
        label = QLabel("Настройки приложения", alignment=Qt.AlignCenter)
        layout.addWidget(label)
        self.tab_settings.setLayout(layout)

    def save_to_file(self):
        with open(self.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.habits, f, ensure_ascii=False, indent=4)

    def load_from_file(self):
        try:
            with open(self.FILE_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())