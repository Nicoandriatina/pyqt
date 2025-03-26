import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from admin_ui import AdminUI
from client_ui import ClientUI


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Se connecter", self)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

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
                self.open_client_ui(username)  # ✅ Correction : passer `username`
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    auth_window.show()
    sys.exit(app.exec())
