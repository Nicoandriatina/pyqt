from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, 
    QTabWidget, QInputDialog
)
from database import obtenir_produits, obtenir_ventes_client, ajouter_vente

class ClientUI(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
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

    # === Onglet Produits Disponibles ===
    def setup_produits_ui(self):
        layout = QVBoxLayout()
        self.table_produits = QTableWidget()
        self.table_produits.setColumnCount(4)
        self.table_produits.setHorizontalHeaderLabels(["ID", "Nom", "Prix", "Stock"])

        self.id_produit_input = QLineEdit()
        self.id_produit_input.setPlaceholderText("ID du produit")

        self.quantite_input = QLineEdit()
        self.quantite_input.setPlaceholderText("Quantité")

        self.btn_acheter = QPushButton("Acheter")
        self.btn_acheter.clicked.connect(self.acheter_produit)

        layout.addWidget(self.table_produits)
        layout.addWidget(QLabel("ID du produit :"))
        layout.addWidget(self.id_produit_input)
        layout.addWidget(QLabel("Quantité :"))
        layout.addWidget(self.quantite_input)
        layout.addWidget(self.btn_acheter)

        self.tab_produits.setLayout(layout)
        self.refresh_produits_table()

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
        self.table_historique.setColumnCount(4)
        self.table_historique.setHorizontalHeaderLabels(["ID Vente", "Produit", "Quantité", "Date"])

        layout.addWidget(self.table_historique)
        self.tab_historique.setLayout(layout)
        self.refresh_historique_table()

    def refresh_historique_table(self):
        ventes = obtenir_ventes_client(self.username)
        self.table_historique.setRowCount(len(ventes))

        for row_idx, vente in enumerate(ventes):
            for col_idx, data in enumerate(vente):
                self.table_historique.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
    
    def acheter_produit(self):
        """Gère l'achat d'un produit par le client."""
        produit_selectionne = self.table_produits.currentItem()
    
        if produit_selectionne:
            nom_produit = produit_selectionne.text()
            quantite, ok = QInputDialog.getInt(self, "Achat", f"Quantité de {nom_produit} à acheter:", 1, 1, 100)
        
            if ok:
                reussi = ajouter_vente(self.username, nom_produit, quantite)
                if reussi:
                    QMessageBox.information(self, "Succès", f"Achat de {quantite} {nom_produit} réussi!")
                else:
                    QMessageBox.warning(self, "Erreur", "Achat échoué. Vérifiez le stock ou réessayez plus tard.")
        else:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un produit avant d'acheter.")

if __name__ == "__main__":
    app = QApplication([])
    window = ClientUI("client1")
    window.show()
    app.exec()
