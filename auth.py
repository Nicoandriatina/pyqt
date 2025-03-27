import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QLineEdit, QMessageBox, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from admin_ui import AdminUI
from client_ui import ClientUI


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setGeometry(100, 100, 400, 350)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Supprime la bordure native
        self.setStyleSheet("background-color: #2C3E50; border-radius: 10px;")

        layout = QVBoxLayout()
        
        # === BARRE DE TITRE PERSONNALISÉE ===
        title_bar = QHBoxLayout()
        self.close_btn = QPushButton("")
        self.minimize_btn = QPushButton("")
        self.maximize_btn = QPushButton("")

        for btn in (self.close_btn, self.minimize_btn, self.maximize_btn):
            btn.setFixedSize(16, 16)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #E74C3C;
                    border-radius: 8px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #C0392B;
                }
            """)

        self.minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #F1C40F;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #D4AC0D;
            }
        """)

        self.maximize_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ECC71;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
        """)

        self.close_btn.clicked.connect(self.close)
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize)

        title_bar.addWidget(self.close_btn)
        title_bar.addWidget(self.minimize_btn)
        title_bar.addWidget(self.maximize_btn)
        title_bar.addStretch(1)  # Décaler les boutons à gauche

        layout.addLayout(title_bar)

        # === TITRE ET MESSAGE DE BIENVENUE ===
        title_label = QLabel("AUTHENTIFICATION")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white; margin-top: 10px;")

        welcome_label = QLabel("Bienvenue ! Veuillez vous connecter.")
        welcome_label.setFont(QFont("Arial", 10))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("color: white; margin-bottom: 15px;")

        layout.addWidget(title_label)
        layout.addWidget(welcome_label)

        # === FORMULAIRE DE CONNEXION ===
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setStyleSheet("padding: 5px; border-radius: 5px; background-color: white;")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("padding: 5px; border-radius: 5px; background-color: white;")
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Se connecter", self)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        self.is_maximized = False

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect("vente.db")
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM utilisateurs WHERE nom=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            role = user[0]
            if role == "admin":
                self.open_admin_ui()
            elif role == "client":
                self.open_client_ui(username)
        else:
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect !")

    def open_admin_ui(self):
        self.admin_window = AdminUI()
        self.admin_window.show()
        self.close()

    def open_client_ui(self, nom):
        self.client_window = ClientUI(nom)
        self.client_window.show()
        self.close()

    def toggle_maximize(self):
        if self.is_maximized:
            self.showNormal()
        else:
            self.showMaximized()
        self.is_maximized = not self.is_maximized


if __name__ == "__main__":
    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    auth_window.show()
    sys.exit(app.exec())
