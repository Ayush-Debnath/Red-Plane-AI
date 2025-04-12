import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from game import Game
from game_AI import run
import os

class StartMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Red Plane - Modern Menu")
        self.setGeometry(100, 100, 400, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-image: url('graphics/environment/bg.png'); background-size: cover;")

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("Red Plane")
        self.title_label.setFont(QFont("Arial", 40, QFont.Bold))
        self.title_label.setStyleSheet("color: black;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.play_button = QPushButton("Normal Play")
        self.ai_button = QPushButton("AI Play")
        self.quit_button = QPushButton("Quit")

        for button in [self.play_button, self.ai_button, self.quit_button]:
            button.setFont(QFont("Arial", 18))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #fff;
                    color: black;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #fff;
                }
            """)
            button.setFixedSize(200, 50)
            self.layout.addWidget(button)

        self.play_button.clicked.connect(self.start_normal_game)
        self.ai_button.clicked.connect(self.start_ai_game)
        self.quit_button.clicked.connect(self.quit_game)

    def start_normal_game(self):
        self.close()
        game = Game()
        game.run()

    def start_ai_game(self):
        self.close()
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config-feedforward.txt')
        run(config_path)

    def quit_game(self):
        sys.exit()
