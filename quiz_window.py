import pygame 
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QHBoxLayout
from question import get_random_questions
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from quiz_game import QuizGame
from question import easy_questions
import random
import json

class QuizWindow(QMainWindow):

    def load_highscore(self):
        try:
            with open('notes_data.json') as f:
                return json.load(f).get('highscore', 0)
        except:
            return 0

    def save_highscore(self, score):
        hs = max(score, self.load_highscore())
        with open('notes_data.json', 'w') as f:
            json.dump({'highscore': hs}, f)

    def use_call_friend(self):
        if self.joker_friend_used:
            return
        self.joker_friend_used = True

        q = self.game.get_current_question()
        letters = ['A', 'B', 'C', 'D']
        letter  = letters[q['correct']]
        answer  = q['answers'][q['correct']]

        messages = [
            f'Хмм... не съм 100% сигурен, но мисля е {letter}.',
            f'Чакай... вероятно е {letter} - {answer}!',
            f'Доста съм уверен, че е {letter}!'
        ]

        QMessageBox.information(
            self,
            'Приятелят ти казва:',
            f'... (звъни телефона) ...\n\n{random.choice(messages)}'
        )
        self.btn_friend.setEnabled(False)

    def use_fifty_fifty(self):
        if self.joker_fifty_used:
            return
        self.joker_fifty_used = True

        q = self.game.get_current_question()
        wrong = [i for i in range(4) if i != q['correct']]
        to_hide = random.sample(wrong, 2)

        for i in to_hide:
            self.buttons[i].hide()

        self.btn_fifty.setEnabled(False)

    def use_audience(self):
        if self.joker_audience_used:
            return
        self.joker_audience_used = True

        q = self.game.get_current_question()
        correct = q['correct']

        correct_pct = random.randint(45, 70)
        rest = 100 - correct_pct

        cuts = sorted([random.randint(0, rest) for _ in range(2)])
        parts = [cuts[0], cuts[1] - cuts[0], rest - cuts[1]]
        random.shuffle(parts)

        pi = 0
        for i in range(4):
            if i == correct:
                pct = correct_pct
            else:
                pct = parts[pi]
                pi += 1
            current = self.buttons[i].text()
            self.buttons[i].setText(current + f'  ({pct}%)')

        self.btn_audience.setEnabled(False)

        # Метод:
    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f'Време: {self.time_left}s')
        if self.time_left <= 0:
            self.timer.stop()
            self.load_question()
    ANSWER_STYLE = "background:#1a3a6e; color:white; border-radius:8px; font-size:15px;"
    
    def flash_button(self, btn, color):     
        btn.setStyleSheet(f"background:{color}; border-radius:8px; font-size:15px;")     
        QTimer.singleShot(600, lambda: btn.setStyleSheet(ANSWER_STYLE))
    
    def __init__(self):
        self.time_left = 30
        self.timer_label = QLabel('Време: 30s')
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.layout.addWidget(self.timer_label)

        self.game = QuizGame(get_random_questions())
        # Флагове
        self.joker_fifty_used    = False
        self.joker_audience_used = False
        self.joker_friend_used   = False

        # Бутони
        self.btn_fifty   = QPushButton('50:50')
        self.btn_audience = QPushButton('Публика')
        self.btn_friend  = QPushButton('Приятел')

        joker_style = '''
            QPushButton { background:#DAA520; color:#0b0f2a;
                border-radius:10px; font-weight:bold; font-size:14px;
                min-height:45px; }
            QPushButton:disabled { background:#555; color:#888; }
        '''
        for btn in [self.btn_fifty, self.btn_audience, self.btn_friend]:
            btn.setStyleSheet(joker_style)

        self.btn_fifty.clicked.connect(self.use_fifty_fifty)
        self.btn_audience.clicked.connect(self.use_audience)
        self.btn_friend.clicked.connect(self.use_call_friend)
        
        joker_layout = QHBoxLayout()
        joker_layout.addWidget(self.btn_fifty)
        joker_layout.addWidget(self.btn_audience)
        joker_layout.addWidget(self.btn_friend)
        self.layout.addLayout(joker_layout)

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
        self.time_left = 30
        self.timer.start(1000)


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

    def reset_jokers(self):
        self.joker_fifty_used    = False
        self.joker_audience_used = False
        self.joker_friend_used   = False
        self.btn_fifty.setEnabled(True)
        self.btn_audience.setEnabled(True)
        self.btn_friend.setEnabled(True)
        for btn in self.buttons:
            btn.show()

    def restart_game(self):
        self.reset_jokers()
        self.game = QuizGame(get_random_questions())
        self.score_label.setText('Биткойни: 0')
        self.load_question()

    def answer_clicked(self, index):
        if is_correct:
            self.flash_button(self.buttons[idx], color) 
            QTimer.singleShot(700, self.load_question)
        self.timer.stop()
        pygame.mixer.init() 
        self.sound_correct = pygame.mixer.Sound("assets/sounds/correct.wav") 
        self.sound_wrong   = pygame.mixer.Sound("assets/sounds/wrong.wav")  
        if is_correct: 	
            self.sound_correct.play() 
        else: 	
            self.sound_wrong.play()
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

            def __init__(self, mode='easy'):
    
                if mode == 'easy':
                    questions = random.sample(easy_questions, 5)
                else:
                    questions = random.sample(hard_questions, 10)
                    self.game = QuizGame(questions)

            self.save_highscore(self.game.score)
            self.setWindowTitle(f'Рекорд: {self.load_highscore()} BTC')

            self.wrong_sound.play()

            # обновяване на биткойните
            self.score_label.setText(f"Биткойни: {self.game.score}")

            # изчакване 1 секунда
            QTimer.singleShot(1000, self.load_question)
