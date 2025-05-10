import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ежедневные привычки")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel("Привычки", self)

        # Поле ввода
        self.input = QLineEdit("", self)

        # Кнопки
        self.add_button = QPushButton("Добавить", self)
        self.done_button = QPushButton("Выполнено", self)

        # Добавляем элементы
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.done_button)

        central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())