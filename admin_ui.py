from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, 
    QTabWidget, QHBoxLayout
)
from database import (
    obtenir_produits, ajouter_produit, modifier_produit, supprimer_produit, 
    obtenir_clients, ajouter_client, modifier_client, supprimer_client,
    obtenir_ventes, ajouter_vente, modifier_vente, supprimer_vente,obtenir_utilisateurs, ajouter_utilisateur, modifier_utilisateur, supprimer_utilisateur

)

class AdminUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Espace Administrateur")
        self.setGeometry(100, 100, 700, 500)

        self.layout = QVBoxLayout()
        
        # Onglets (Produits / Clients)
        self.tabs = QTabWidget()
        self.tab_produits = QWidget()
        self.tab_clients = QWidget()
        self.tab_ventes = QWidget()
        self.tab_utilisateurs = QWidget()

        self.tabs.addTab(self.tab_produits, "Gestion des Produits")
        self.tabs.addTab(self.tab_clients, "Gestion des Clients")
        self.tabs.addTab(self.tab_ventes, "Gestion des Ventes")
        self.tabs.addTab(self.tab_utilisateurs, "Gestion des Utilisateurs")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Ajouter les interfaces pour chaque onglet
        self.setup_produit_ui()
        self.setup_client_ui()
        self.setup_ventes_ui()
        self.setup_utilisateur_ui()

    # === Onglet Gestion des Produits ===
    def setup_produit_ui(self):
        layout = QVBoxLayout()

        self.nom_produit_input = QLineEdit()
        self.nom_produit_input.setPlaceholderText("Nom du produit")

        self.prix_produit_input = QLineEdit()
        self.prix_produit_input.setPlaceholderText("Prix")

        self.stock_produit_input = QLineEdit()
        self.stock_produit_input.setPlaceholderText("Stock")

        self.btn_ajouter_produit = QPushButton("Ajouter Produit")
        self.btn_ajouter_produit.clicked.connect(self.ajouter_produit)

        self.btn_modifier_produit = QPushButton("Modifier Produit")
        self.btn_modifier_produit.clicked.connect(self.modifier_produit)

        self.btn_supprimer_produit = QPushButton("Supprimer Produit")
        self.btn_supprimer_produit.clicked.connect(self.supprimer_produit)

        self.table_produits = QTableWidget()
        self.table_produits.setColumnCount(4)
        self.table_produits.setHorizontalHeaderLabels(["ID", "Nom", "Prix", "Stock"])
        
        layout.addWidget(QLabel("Nom:"))
        layout.addWidget(self.nom_produit_input)
        layout.addWidget(QLabel("Prix:"))
        layout.addWidget(self.prix_produit_input)
        layout.addWidget(QLabel("Stock:"))
        layout.addWidget(self.stock_produit_input)
        layout.addWidget(self.btn_ajouter_produit)
        layout.addWidget(self.btn_modifier_produit)
        layout.addWidget(self.btn_supprimer_produit)
        layout.addWidget(self.table_produits)

        self.tab_produits.setLayout(layout)
        self.refresh_produit_table()

    def refresh_produit_table(self):
        produits = obtenir_produits()
        self.table_produits.setRowCount(len(produits))

        for row_idx, produit in enumerate(produits):
            for col_idx, data in enumerate(produit):
                self.table_produits.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def ajouter_produit(self):
        nom = self.nom_produit_input.text()
        prix = self.prix_produit_input.text()
        stock = self.stock_produit_input.text()

        if nom and prix and stock:
            ajouter_produit(nom, float(prix), int(stock))
            self.refresh_produit_table()
            QMessageBox.information(self, "Succès", "Produit ajouté avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def modifier_produit(self):
        selected_row = self.table_produits.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un produit.")
            return

        id_produit = int(self.table_produits.item(selected_row, 0).text())
        nom = self.nom_produit_input.text()
        prix = self.prix_produit_input.text()
        stock = self.stock_produit_input.text()

        if nom and prix and stock:
            modifier_produit(id_produit, nom, float(prix), int(stock))
            self.refresh_produit_table()
            QMessageBox.information(self, "Succès", "Produit modifié avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def supprimer_produit(self):
        selected_row = self.table_produits.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un produit.")
            return

        id_produit = int(self.table_produits.item(selected_row, 0).text())
        supprimer_produit(id_produit)
        self.refresh_produit_table()
        QMessageBox.information(self, "Succès", "Produit supprimé avec succès !")

    # === Onglet Gestion des Clients ===
    def setup_client_ui(self):
        layout = QVBoxLayout()

        self.nom_client_input = QLineEdit()
        self.nom_client_input.setPlaceholderText("Nom du client")

        self.btn_ajouter_client = QPushButton("Ajouter Client")
        self.btn_ajouter_client.clicked.connect(self.ajouter_client)

        self.btn_modifier_client = QPushButton("Modifier Client")
        self.btn_modifier_client.clicked.connect(self.modifier_client)

        self.btn_supprimer_client = QPushButton("Supprimer Client")
        self.btn_supprimer_client.clicked.connect(self.supprimer_client)

        self.table_clients = QTableWidget()
        self.table_clients.setColumnCount(2)
        self.table_clients.setHorizontalHeaderLabels(["ID", "Nom"])
        
        layout.addWidget(QLabel("Nom:"))
        layout.addWidget(self.nom_client_input)
        layout.addWidget(self.btn_ajouter_client)
        layout.addWidget(self.btn_modifier_client)
        layout.addWidget(self.btn_supprimer_client)
        layout.addWidget(self.table_clients)

        self.tab_clients.setLayout(layout)
        self.refresh_client_table()

    def refresh_client_table(self):
        clients = obtenir_clients()
        self.table_clients.setRowCount(len(clients))

        for row_idx, client in enumerate(clients):
            for col_idx, data in enumerate(client):
                self.table_clients.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def ajouter_client(self):
        nom = self.nom_client_input.text()

        if nom:
            ajouter_client(nom)
            self.refresh_client_table()
            QMessageBox.information(self, "Succès", "Client ajouté avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom.")

    def modifier_client(self):
        selected_row = self.table_clients.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un client.")
            return

        id_client = int(self.table_clients.item(selected_row, 0).text())
        nom = self.nom_client_input.text()

        if nom:
            modifier_client(id_client, nom)
            self.refresh_client_table()
            QMessageBox.information(self, "Succès", "Client modifié avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom.")

    def supprimer_client(self):
        selected_row = self.table_clients.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un client.")
            return

        id_client = int(self.table_clients.item(selected_row, 0).text())
        supprimer_client(id_client)
        self.refresh_client_table()
        QMessageBox.information(self, "Succès", "Client supprimé avec succès !")

    # === Onglet Gestion des Ventes ===
    def setup_ventes_ui(self):
        layout = QVBoxLayout()

        self.table_ventes = QTableWidget()
        self.table_ventes.setColumnCount(5)
        self.table_ventes.setHorizontalHeaderLabels(["ID", "Client", "Produit", "Quantité", "Date"])
        self.refresh_vente_table()

        # Champs pour ajouter une vente
        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("ID Client")

        self.produit_id_input = QLineEdit()
        self.produit_id_input.setPlaceholderText("ID Produit")

        self.quantite_input = QLineEdit()
        self.quantite_input.setPlaceholderText("Quantité")

        self.btn_ajouter_vente = QPushButton("Ajouter Vente")
        self.btn_ajouter_vente.clicked.connect(self.ajouter_vente)

        # Champs pour modifier/supprimer une vente
        self.id_vente_input = QLineEdit()
        self.id_vente_input.setPlaceholderText("ID Vente")

        self.nouvelle_quantite_input = QLineEdit()
        self.nouvelle_quantite_input.setPlaceholderText("Nouvelle Quantité")

        self.btn_modifier_vente = QPushButton("Modifier Vente")
        self.btn_modifier_vente.clicked.connect(self.modifier_vente)

        self.btn_supprimer_vente = QPushButton("Supprimer Vente")
        self.btn_supprimer_vente.clicked.connect(self.supprimer_vente)

        # Ajout des widgets au layout
        layout.addWidget(self.table_ventes)
        layout.addWidget(QLabel("Nouvelle Vente:"))
        layout.addWidget(self.client_id_input)
        layout.addWidget(self.produit_id_input)
        layout.addWidget(self.quantite_input)
        layout.addWidget(self.btn_ajouter_vente)

        layout.addWidget(QLabel("Modifier/Supprimer Vente:"))
        layout.addWidget(self.id_vente_input)
        layout.addWidget(self.nouvelle_quantite_input)
        layout.addWidget(self.btn_modifier_vente)
        layout.addWidget(self.btn_supprimer_vente)

        self.tab_ventes.setLayout(layout)

    def refresh_vente_table(self):
        ventes = obtenir_ventes()
        self.table_ventes.setRowCount(len(ventes))
        for i, vente in enumerate(ventes):
            for j, valeur in enumerate(vente):
                self.table_ventes.setItem(i, j, QTableWidgetItem(str(valeur)))

    def ajouter_vente(self):
        client_id = self.client_id_input.text()
        produit_id = self.produit_id_input.text()
        quantite = self.quantite_input.text()

        if client_id and produit_id and quantite:
            ajouter_vente(int(client_id), int(produit_id), int(quantite))
            self.refresh_vente_table()
            QMessageBox.information(self, "Succès", "Vente ajoutée avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def modifier_vente(self):
        id_vente = self.id_vente_input.text()
        nouvelle_quantite = self.nouvelle_quantite_input.text()

        if id_vente and nouvelle_quantite:
            modifier_vente(int(id_vente), int(nouvelle_quantite))
            self.refresh_vente_table()
            QMessageBox.information(self, "Succès", "Vente modifiée avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def supprimer_vente(self):
        id_vente = self.id_vente_input.text()
        if id_vente:
            supprimer_vente(int(id_vente))
            self.refresh_vente_table()
            QMessageBox.information(self, "Succès", "Vente supprimée avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un ID de vente.")

#interface pour gestion uilisateur
    def setup_utilisateur_ui(self):
        layout = QVBoxLayout()

        self.nom_utilisateur_input = QLineEdit()
        self.nom_utilisateur_input.setPlaceholderText("Nom d'utilisateur")

        self.mdp_utilisateur_input = QLineEdit()
        self.mdp_utilisateur_input.setPlaceholderText("Mot de passe")
        self.mdp_utilisateur_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_ajouter_utilisateur = QPushButton("Ajouter Utilisateur")
        self.btn_ajouter_utilisateur.clicked.connect(self.ajouter_utilisateur)

        self.btn_modifier_utilisateur = QPushButton("Modifier Utilisateur")
        self.btn_modifier_utilisateur.clicked.connect(self.modifier_utilisateur)

        self.btn_supprimer_utilisateur = QPushButton("Supprimer Utilisateur")
        self.btn_supprimer_utilisateur.clicked.connect(self.supprimer_utilisateur)

        self.table_utilisateurs = QTableWidget()
        self.table_utilisateurs.setColumnCount(2)
        self.table_utilisateurs.setHorizontalHeaderLabels(["ID", "Nom d'utilisateur"])

        layout.addWidget(QLabel("Nom d'utilisateur:"))
        layout.addWidget(self.nom_utilisateur_input)
        layout.addWidget(QLabel("Mot de passe:"))
        layout.addWidget(self.mdp_utilisateur_input)
        layout.addWidget(self.btn_ajouter_utilisateur)
        layout.addWidget(self.btn_modifier_utilisateur)
        layout.addWidget(self.btn_supprimer_utilisateur)
        layout.addWidget(self.table_utilisateurs)

        self.tab_utilisateurs.setLayout(layout)
        self.refresh_utilisateur_table()

    def refresh_utilisateur_table(self):
        utilisateurs = obtenir_utilisateurs()
        self.table_utilisateurs.setRowCount(len(utilisateurs))
        for row_idx, utilisateur in enumerate(utilisateurs):
            for col_idx, data in enumerate(utilisateur):
                self.table_utilisateurs.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def ajouter_utilisateur(self):
        nom = self.nom_utilisateur_input.text()
        mdp = self.mdp_utilisateur_input.text()

        if nom and mdp:
            ajouter_utilisateur(nom, mdp)
            self.refresh_utilisateur_table()
            QMessageBox.information(self, "Succès", "Utilisateur ajouté avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def modifier_utilisateur(self):
        selected_row = self.table_utilisateurs.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un utilisateur.")
            return

        id_utilisateur = int(self.table_utilisateurs.item(selected_row, 0).text())
        nom = self.nom_utilisateur_input.text()
        mdp = self.mdp_utilisateur_input.text()

        if nom and mdp:
            modifier_utilisateur(id_utilisateur, nom, mdp)
            self.refresh_utilisateur_table()
            QMessageBox.information(self, "Succès", "Utilisateur modifié avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def supprimer_utilisateur(self):
        selected_row = self.table_utilisateurs.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un utilisateur.")
            return

        id_utilisateur = int(self.table_utilisateurs.item(selected_row, 0).text())
        supprimer_utilisateur(id_utilisateur)
        self.refresh_utilisateur_table()
        QMessageBox.information(self, "Succès", "Utilisateur supprimé avec succès !")


if __name__ == "__main__":
    app = QApplication([])
    window = AdminUI()
    window.show()
    app.exec()
