from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from quiz_game import QuizGame
from question import easy_questions


class QuizWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.game = QuizGame(easy_questions)
        # звук при верен отговор
        self.correct_sound = QSoundEffect()
        self.correct_sound.setSource(QUrl.fromLocalFile(os.path.abspath("audio/correct.mp3")))

        # звук при грешен отговор
        self.wrong_sound = QSoundEffect()
        self.wrong_sound.setSource(QUrl.fromLocalFile(os.path.abspath("audio/wrong.mp3")))


        self.setWindowTitle("Въпроси")
        self.setGeometry(200, 200, 800, 500)

        # тъмен фон
        self.setStyleSheet("""
        QMainWindow{
            background-color:#0b0f2a;
        }
        """)

        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        self.layout = QVBoxLayout()
        # показване на биткойните
        self.score_label = QLabel("Биткойни: 0")
        self.score_label.setAlignment(Qt.AlignRight)

        self.score_label.setStyleSheet("""
        QLabel{
        color: gold;
        font-size:20px;
        font-weight:bold;
        padding:10px;
        }
        """)

        self.layout.addWidget(self.score_label)


        # ВЪПРОС
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)

        self.question_label.setStyleSheet("""
        QLabel{
        background-color:#142a6e;
        color:white;
        border-radius:25px;
        border:4px solid gold;
        padding:20px;
        font-size:24px;
        font-weight:bold;
        }
        """)


        self.layout.addWidget(self.question_label)

        # layout за отговорите
        answers_layout = QGridLayout()

        self.buttons = []

        for i in range(4):

            btn = QPushButton()

            btn.setMinimumHeight(70)

            btn.setStyleSheet("""
            QPushButton{
                background-color:#1c3faa;
                color:white;
                border-radius:20px;
                border:3px solid #6fd3ff;
                font-size:18px;
                padding:10px;
            }

            QPushButton:hover{
                background-color:#2a5de0;
            }

            QPushButton:pressed{
                background-color:#162d73;
            }
            """)

            btn.clicked.connect(lambda checked, x=i: self.answer_clicked(x))

            self.buttons.append(btn)

        # 2x2 подредба
        answers_layout.addWidget(self.buttons[0],0,0)
        answers_layout.addWidget(self.buttons[1],0,1)
        answers_layout.addWidget(self.buttons[2],1,0)
        answers_layout.addWidget(self.buttons[3],1,1)

        self.layout.addLayout(answers_layout)

        self.widget.setLayout(self.layout)

        self.load_question()

    def load_question(self):
# връщане на нормалния цвят на бутоните
        for btn in self.buttons:
            btn.setStyleSheet("""
            QPushButton{
                background-color:#1c3faa;
                color:white;
                border-radius:20px;
                border:3px solid #6fd3ff;
                font-size:18px;
                padding:10px;
            }
            """)

        if self.game.is_finished():
            self.question_label.setText(f"Играта свърши!\nТочки: {self.game.score}")

            for btn in self.buttons:
                btn.hide()

            return

        q = self.game.get_current_question()

        self.question_label.setText(q["text"])

        letters = ["A", "B", "C", "D"]

        for i, answer in enumerate(q["answers"]):
            self.buttons[i].setText(f"{letters[i]}: {answer}")

    def answer_clicked(self, index):

        correct = self.game.answer(index)

        btn = self.buttons[index]

        if correct:

            btn.setStyleSheet("""
            QPushButton{
                background-color:green;
                color:white;
                border-radius:20px;
                font-size:18px;
            }
            """)

            self.correct_sound.play()

        else:

            btn.setStyleSheet("""
            QPushButton{
                background-color:red;
                color:white;
                border-radius:20px;
                font-size:18px;
            }
            """)

            self.wrong_sound.play()

            # обновяване на биткойните
            self.score_label.setText(f"Биткойни: {self.game.score}")

            # изчакване 1 секунда
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(1000, self.load_question)
