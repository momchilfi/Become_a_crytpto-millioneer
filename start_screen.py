from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
from quiz_window import QuizWindow
import os


class StartScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Стани криптобогат!")
        
        self.background_pixmap = self.load_background_image()
        
        if self.background_pixmap:
            width = self.background_pixmap.width()
            height = self.background_pixmap.height()
            self.setFixedSize(width, height)
        else:
            self.setGeometry(100, 100, 600, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        if self.background_pixmap:
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(self.background_pixmap))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
        else:
            self.setStyleSheet("background-color: #2C3E50;")
        
        layout = QVBoxLayout()
        layout.setSpacing(40)
        layout.setAlignment(Qt.AlignCenter)
        
        start_btn = QPushButton("СТАРТ")
        start_btn.setFont(QFont("Arial", 20, QFont.Bold))
        start_btn.setMinimumHeight(80)
        start_btn.setMinimumWidth(250)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                color: white;
                border-radius: 15px;
                border: 3px solid #FFD700;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #45a049, stop:1 #3d8b40);
                border: 3px solid #FFA500;
            }
            QPushButton:pressed {
                background-color: #2e7d32;
            }
        """)
        start_btn.clicked.connect(self.on_start_clicked)
        
        layout.addStretch()
        layout.addWidget(start_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        central_widget.setLayout(layout)
    
    def load_background_image(self):
        """Зарежда фоново изображение"""
        paths = ["start_screen.png", "images/start_screen.png"]
        
        for path in paths:
            if os.path.exists(path):
                print(f"Зареждам изображение от: {path}")
                return QPixmap(path)
        
        print("ВНИМАНИЕ: Не намерих start_screen.png!")
        return None
    
    def on_start_clicked(self):

        self.quiz_window = QuizWindow()
        self.quiz_window.show()
        self.close()