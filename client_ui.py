import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, 
    QInputDialog, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from database import obtenir_produits, obtenir_ventes_client, ajouter_vente

class ClientUI(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.client_id = self.get_client_id(username)

        self.setWindowTitle(f"Espace Client - {self.username}")
        self.setGeometry(100, 100, 700, 500)
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
        title_bar.addStretch(1)

        layout.addLayout(title_bar)

        # === TITRE ===
        title_label = QLabel("ESPACE CLIENT")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white; margin-top: 10px;")

        welcome_label = QLabel(f"Bienvenue, {self.username} !")
        welcome_label.setFont(QFont("Arial", 10))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("color: white; margin-bottom: 15px;")

        layout.addWidget(title_label)
        layout.addWidget(welcome_label)

        # === Onglets (Produits disponibles / Historique des achats) ===
        self.tabs = QTabWidget()
        self.tab_produits = QWidget()
        self.tab_historique = QWidget()

        self.tabs.addTab(self.tab_produits, "Produits disponibles")
        self.tabs.addTab(self.tab_historique, "Historique des achats")
        layout.addWidget(self.tabs)

        # Ajouter les interfaces pour chaque onglet
        self.setup_produits_ui()
        self.setup_historique_ui()

        # Bouton de déconnexion stylisé
        self.btn_deconnexion = QPushButton("Déconnexion")
        self.btn_deconnexion.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        self.btn_deconnexion.clicked.connect(self.deconnexion)
        layout.addWidget(self.btn_deconnexion)

        self.setLayout(layout)
        self.is_maximized = False

    def deconnexion(self):
        """Ferme l'interface client et revient à l'authentification."""
        from auth import AuthWindow  # Importation retardée pour éviter l'importation circulaire
        self.close()  # Ferme l'interface client
        self.auth_window = AuthWindow()  # Ouvre la fenêtre d'authentification
        self.auth_window.show()

    # === Onglet Produits Disponibles ===
    def setup_produits_ui(self):
        layout = QVBoxLayout()
        self.table_produits = QTableWidget()
        self.table_produits.setColumnCount(4)
        self.table_produits.setHorizontalHeaderLabels(["ID", "Nom", "Prix", "Stock"])
        self.table_produits.setStyleSheet("background-color: white; border-radius: 5px;")
        self.table_produits.verticalHeader().setVisible(False)

        self.btn_acheter = QPushButton("Acheter")
        self.btn_acheter.setStyleSheet("""
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
        self.btn_acheter.clicked.connect(self.acheter_produit)

        layout.addWidget(self.table_produits)
        layout.addWidget(self.btn_acheter)

        self.tab_produits.setLayout(layout)
        self.refresh_produits_table()
    def acheter_produit(self):
        produit_selectionne = self.table_produits.currentRow()  # Récupérer l'index sélectionné

        if produit_selectionne == -1:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un produit avant d'acheter.")
            return

        produit_id = int(self.table_produits.item(produit_selectionne, 0).text())  # ID du produit
        nom_produit = self.table_produits.item(produit_selectionne, 1).text()  # Nom du produit

        quantite, ok = QInputDialog.getInt(self, "Achat", f"Quantité de {nom_produit} à acheter:", 1, 1, 100)

        if ok:
            reussi = ajouter_vente(self.username, produit_id, quantite)
            if reussi:
                QMessageBox.information(self, "Succès", f"Achat de {quantite} {nom_produit} réussi!")
                self.refresh_produits_table()  # Rafraîchir la liste des produits
                self.refresh_historique_table()  # Rafraîchir l'historique des achats
            else:
                QMessageBox.warning(self, "Erreur", "Achat échoué. Stock insuffisant ou erreur.")


    def get_client_id(self, username):
        """Récupère l'ID de l'utilisateur ayant le rôle client."""
        conn = sqlite3.connect("vente.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM utilisateurs WHERE nom = ? AND role = 'client'", (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def refresh_produits_table(self):
        produits = obtenir_produits()
        self.table_produits.setRowCount(len(produits))
        for row_idx, produit in enumerate(produits):
            for col_idx, data in enumerate(produit):
                self.table_produits.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    # === Onglet Historique des Achats ===
    def setup_historique_ui(self):
        layout = QVBoxLayout()
        self.table_historique = QTableWidget()
        self.table_historique.setColumnCount(5)
        self.table_historique.setHorizontalHeaderLabels(["ID Vente", "Nom client", "ID Produit", "Quantité", "Date"])
        self.table_historique.setStyleSheet("background-color: white; border-radius: 5px;")
        self.table_historique.verticalHeader().setVisible(False)

        layout.addWidget(self.table_historique)
        self.tab_historique.setLayout(layout)
        self.refresh_historique_table()

    def refresh_historique_table(self):
        if self.client_id is None:
            return
        ventes = obtenir_ventes_client()
        self.table_historique.setRowCount(len(ventes))
        for row_idx, vente in enumerate(ventes):
            for col_idx, data in enumerate(vente):
                self.table_historique.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def toggle_maximize(self):
        if self.is_maximized:
            self.showNormal()
        else:
            self.showMaximized()
        self.is_maximized = not self.is_maximized


if __name__ == "__main__":
    app = QApplication([])
    window = ClientUI("client1")
    window.show()
    app.exec()
