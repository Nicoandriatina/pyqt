import sqlite3

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, 
    QTabWidget, QInputDialog
)
from database import obtenir_produits, obtenir_ventes_client, ajouter_vente, reset_database

class ClientUI(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.client_id = self.get_client_id(username)
        self.setWindowTitle(f"Espace Client - {self.username}")
        self.setGeometry(100, 100, 700, 500)

        self.layout = QVBoxLayout()

        # Onglets (Produits disponibles / Historique des achats)
        self.tabs = QTabWidget()
        self.tab_produits = QWidget()
        self.tab_historique = QWidget()

        self.tabs.addTab(self.tab_produits, "Produits disponibles")
        self.tabs.addTab(self.tab_historique, "Historique des achats")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Ajouter les interfaces pour chaque onglet
        self.setup_produits_ui()
        self.setup_historique_ui()

     # Bouton de déconnexion
        self.btn_deconnexion = QPushButton("Déconnexion")
        self.btn_deconnexion.clicked.connect(self.deconnexion)
        self.layout.addWidget(self.btn_deconnexion)

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

        # self.id_produit_input = QLineEdit()
        # self.id_produit_input.setPlaceholderText("ID du produit")

        # self.quantite_input = QLineEdit()
        # self.quantite_input.setPlaceholderText("Quantité")

        self.btn_acheter = QPushButton("Acheter")
        self.btn_acheter.clicked.connect(self.acheter_produit)

        layout.addWidget(self.table_produits)
        # layout.addWidget(QLabel("ID du produit :"))
        # layout.addWidget(self.id_produit_input)
        # layout.addWidget(QLabel("Quantité :"))
        # layout.addWidget(self.quantite_input)
        layout.addWidget(self.btn_acheter)

        self.tab_produits.setLayout(layout)
        self.refresh_produits_table()


    def get_client_id(self, username):
        """Récupère l'ID de l'utilisateur ayant le rôle client."""
        conn = sqlite3.connect("vente.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM utilisateurs WHERE nom = ? AND role = 'client'", (username,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            print(f"DEBUG - Aucun ID trouvé pour {username}")
            return None


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
        self.table_historique.setHorizontalHeaderLabels(["ID Vente","Nom client" ," ID Produit", "Quantité", "Date"])

        layout.addWidget(self.table_historique)
        self.tab_historique.setLayout(layout)
        self.refresh_historique_table()

    def refresh_historique_table(self):
        if self.client_id is None:
            print(f"DEBUG - Aucun ID trouvé pour {self.username}")
            return

        ventes = obtenir_ventes_client()
        self.table_historique.setRowCount(len(ventes))
        print(f"DEBUG - Ventes récupérées : {ventes}")

        for row_idx, vente in enumerate(ventes):
            for col_idx, data in enumerate(vente):
                self.table_historique.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    
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
                self.refresh_historique_table(self.client_id)  # Rafraîchir l'historique des achats
        else:
            QMessageBox.warning(self, "Erreur", "Achat échoué. Stock insuffisant ou erreur.")


if __name__ == "__main__":
    app = QApplication([])
    window = ClientUI("client1")
    window.show()
    app.exec()
