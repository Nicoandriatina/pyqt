from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, 
    QTabWidget, QHBoxLayout, QFrame
)

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from database import (
    obtenir_produits, ajouter_produit, modifier_produit, supprimer_produit, 
    obtenir_clients, ajouter_client, modifier_client, supprimer_client,
    obtenir_ventes, ajouter_vente, modifier_vente, supprimer_vente,obtenir_utilisateurs, ajouter_utilisateur, modifier_utilisateur, supprimer_utilisateur, obtenir_audit_ventes

)

class AdminUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Espace Administrateur")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #f4f4f4; border-radius: 10px;")

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
# contenu principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        #titre 
          # === Barre de titre personnalisée ===
        self.title_bar = QHBoxLayout()
        self.title_bar.setContentsMargins(10, 5, 10, 5)

        self.title_label = QLabel("Espace Administrateur")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.close_btn = QPushButton("")
        self.minimize_btn = QPushButton("")
        self.maximize_btn = QPushButton("")

        for btn in (self.close_btn, self.minimize_btn, self.maximize_btn):
            btn.setFixedSize(QSize(16, 16))
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

        self.title_bar.addWidget(self.title_label)
        self.title_bar.addStretch()
        self.title_bar.addWidget(self.minimize_btn)
        self.title_bar.addWidget(self.maximize_btn)
        self.title_bar.addWidget(self.close_btn)

        title_container = QWidget()
        title_container.setLayout(self.title_bar)
        title_container.setStyleSheet("background-color: #2c3e50; padding: 5px;")

        self.main_layout.addWidget(title_container)
        # Onglets (Produits / Clients)
        self.tabs = QTabWidget()
        self.tab_produits = QWidget()
        self.tab_clients = QWidget()
        self.tab_ventes = QWidget()
        self.tab_utilisateurs = QWidget()
        self.tab_audit = QWidget()

        self.tabs.addTab(self.tab_produits, "Gestion des Produits")
        # self.tabs.addTab(self.tab_clients, "Gestion des Clients")
        self.tabs.addTab(self.tab_ventes, "Gestion des Ventes")
        self.tabs.addTab(self.tab_utilisateurs, "Gestion des Utilisateurs")
        self.tabs.addTab(self.tab_audit,"Audit des Ventes")

        self.main_layout.addWidget(self.tabs)
        self.setLayout(self.main_layout)

        # Ajouter les interfaces pour chaque onglet
        self.setup_produit_ui()
        # self.setup_client_ui()
        self.setup_ventes_ui()
        self.setup_utilisateur_ui()
        self.setup_audit_ui()


        # Bouton de déconnexion
        self.btn_deconnexion = QPushButton("Déconnexion")
        self.btn_deconnexion.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        self.btn_deconnexion.clicked.connect(self.deconnexion)
        self.main_layout.addWidget(self.btn_deconnexion)

    def toggle_maximize(self):
        """Bascule entre le mode maximisé et restauré."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def deconnexion(self):
        """Ferme l'interface admin et revient à l'authentification."""
        from auth import AuthWindow  # Importation tardive pour éviter l'importation circulaire
        self.close()
        self.auth_window = AuthWindow()
        self.auth_window.show()


    # === Onglet Audit des Ventes ===
    def setup_audit_ui(self):
        layout = QVBoxLayout()

        self.table_audit = QTableWidget()
        self.table_audit.setColumnCount(7)
        self.table_audit.setHorizontalHeaderLabels([
            "Type Opération", "Date MAJ", "Nom Client", "Désignation Produit",
            "Quantité Ancienne", "Quantité Nouvelle", "Utilisateur"
        ])
        self.table_audit.setStyleSheet("background-color: white; border: 1px solid #ccc;")

        self.btn_refresh_audit = QPushButton("Actualiser")
        self.btn_refresh_audit.clicked.connect(self.refresh_audit_table)

        layout.addWidget(self.table_audit)
        layout.addWidget(self.btn_refresh_audit)

        self.tab_audit.setLayout(layout)

    def refresh_audit_table(self):
        audit_logs = obtenir_audit_ventes()
        self.table_audit.setRowCount(len(audit_logs))

        for row_idx, log in enumerate(audit_logs):
            for col_idx, data in enumerate(log):
                self.table_audit.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))


    # === Onglet Gestion des Produits ===
    def setup_produit_ui(self):
        layout = QVBoxLayout()

    #formulaire
        form_layout = QHBoxLayout()

        self.nom_produit_input = QLineEdit()
        self.nom_produit_input.setPlaceholderText("Nom du produit")

        self.prix_produit_input = QLineEdit()
        self.prix_produit_input.setPlaceholderText("Prix")

        self.stock_produit_input = QLineEdit()
        self.stock_produit_input.setPlaceholderText("Stock")

        form_layout.addWidget(self.nom_produit_input)
        form_layout.addWidget(self.prix_produit_input)
        form_layout.addWidget(self.stock_produit_input)

        layout.addLayout(form_layout)

        #bouton
        btn_layout = QHBoxLayout()
        self.btn_ajouter_produit = QPushButton("Ajouter")
        self.btn_modifier_produit = QPushButton("Modifier")
        self.btn_supprimer_produit = QPushButton("Supprimer")

        for btn in [self.btn_ajouter_produit, self.btn_modifier_produit, self.btn_supprimer_produit]:
            btn.setStyleSheet("background-color: #3498db; color: white; padding: 6px; font-size: 14px; border-radius: 5px;")
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

    #tableau
        self.table_produits = QTableWidget()
        self.table_produits.setColumnCount(4)
        self.table_produits.setHorizontalHeaderLabels(["ID", "Nom", "Prix", "stock"])
        self.table_produits.setStyleSheet("background-color: white; border: 1px solid #ccc;")

        layout.addWidget(self.table_produits)
        self.tab_produits.setLayout(layout)
        self.refresh_produit_table()
        
        #connection de event
        self.btn_ajouter_produit.clicked.connect(self.ajouter_produit)
        self.btn_modifier_produit.clicked.connect(self.modifier_produit)
        self.btn_supprimer_produit.clicked.connect(self.supprimer_produit)
        self.table_produits.itemSelectionChanged.connect(self.remplir_champs_produit)

        
    def remplir_champs_produit(self):
        selected_row = self.table_produits.currentRow()
        if selected_row == -1:
            return  # Aucun produit sélectionné

        # Débogage : Vérifiez les valeurs récupérées de la table
        print(f"DEBUG: Ligne sélectionnée {selected_row}")
        print(f"DEBUG: Nom: {self.table_produits.item(selected_row, 1).text()}")
        print(f"DEBUG: Prix: {self.table_produits.item(selected_row, 2).text()}")
        print(f"DEBUG: Stock: {self.table_produits.item(selected_row, 3).text()}")

        # Remplir les champs avec les données sélectionnées
        if self.table_produits.item(selected_row, 1) and self.table_produits.item(selected_row, 2) and self.table_produits.item(selected_row, 3):
            self.nom_produit_input.setText(self.table_produits.item(selected_row, 1).text())
            self.prix_produit_input.setText(self.table_produits.item(selected_row, 2).text())
            self.stock_produit_input.setText(self.table_produits.item(selected_row, 3).text())


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
            modifier_produit(id_produit, nom, float(prix), int(float(stock)))
            self.refresh_produit_table()
            QMessageBox.information(self, "Succès", "Produit modifié avec succès !")

    def supprimer_produit(self):
        selected_row = self.table_produits.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un produit.")
            return

        id_produit = int(self.table_produits.item(selected_row, 0).text())

        reply = QMessageBox.question(
            self, "Confirmation", "Voulez-vous vraiment supprimer ce produit ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            supprimer_produit(id_produit)
            self.refresh_produit_table()
            QMessageBox.information(self, "Succès", "Produit supprimé avec succès !")

    # === Onglet Gestion des Ventes ===
    def setup_ventes_ui(self):
        layout = QVBoxLayout()

        # === Tableau des ventes ===
        self.table_ventes = QTableWidget()
        self.table_ventes.setColumnCount(5)
        self.table_ventes.setHorizontalHeaderLabels(["ID", "Client", "Produit", "Quantité", "Date"])
        self.table_ventes.setStyleSheet("background-color: white; border: 1px solid #ccc;")

        layout.addWidget(self.table_ventes)

        # === Formulaire pour ajouter une vente ===
        form_layout = QHBoxLayout()

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("ID Client")

        self.produit_id_input = QLineEdit()
        self.produit_id_input.setPlaceholderText("ID Produit")

        self.quantite_input = QLineEdit()
        self.quantite_input.setPlaceholderText("Quantité")

        form_layout.addWidget(self.client_id_input)
        form_layout.addWidget(self.produit_id_input)
        form_layout.addWidget(self.quantite_input)

        layout.addLayout(form_layout)

        # === Boutons pour gérer les ventes ===
        btn_layout = QHBoxLayout()
        self.btn_ajouter_vente = QPushButton("Ajouter")
        self.btn_modifier_vente = QPushButton("Modifier")
        self.btn_supprimer_vente = QPushButton("Supprimer")

        for btn in [self.btn_ajouter_vente, self.btn_modifier_vente, self.btn_supprimer_vente]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 6px;
                    font-size: 14px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        # === Formulaire pour modifier/supprimer une vente ===
        edit_form_layout = QHBoxLayout()

        self.id_vente_input = QLineEdit()
        self.id_vente_input.setPlaceholderText("ID Vente")

        self.nouvelle_quantite_input = QLineEdit()
        self.nouvelle_quantite_input.setPlaceholderText("Nouvelle Quantité")

        edit_form_layout.addWidget(self.id_vente_input)
        edit_form_layout.addWidget(self.nouvelle_quantite_input)

        layout.addLayout(edit_form_layout)

        self.tab_ventes.setLayout(layout)

        # === Connexion des boutons ===
        self.btn_ajouter_vente.clicked.connect(self.ajouter_vente)
        self.btn_modifier_vente.clicked.connect(self.modifier_vente)
        self.btn_supprimer_vente.clicked.connect(self.supprimer_vente)

        self.refresh_vente_table()

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

        # === Formulaire ===
        form_layout = QHBoxLayout()

        self.nom_utilisateur_input = QLineEdit()
        self.nom_utilisateur_input.setPlaceholderText("Nom d'utilisateur")

        self.role_utilisateur_input = QLineEdit()
        self.role_utilisateur_input.setPlaceholderText("Rôle")

        self.mdp_utilisateur_input = QLineEdit()
        self.mdp_utilisateur_input.setPlaceholderText("Mot de passe")
        self.mdp_utilisateur_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addWidget(self.nom_utilisateur_input)
        form_layout.addWidget(self.role_utilisateur_input)
        form_layout.addWidget(self.mdp_utilisateur_input)

        layout.addLayout(form_layout)

        # === Boutons ===
        btn_layout = QHBoxLayout()
        self.btn_ajouter_utilisateur = QPushButton("Ajouter")
        self.btn_modifier_utilisateur = QPushButton("Modifier")
        self.btn_supprimer_utilisateur = QPushButton("Supprimer")

        for btn in [self.btn_ajouter_utilisateur, self.btn_modifier_utilisateur, self.btn_supprimer_utilisateur]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 6px;
                    font-size: 14px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        # === Tableau des utilisateurs ===
        self.table_utilisateurs = QTableWidget()
        self.table_utilisateurs.setColumnCount(3)
        self.table_utilisateurs.setHorizontalHeaderLabels(["ID", "Nom d'utilisateur", "Rôle"])
        self.table_utilisateurs.setStyleSheet("background-color: white; border: 1px solid #ccc;")

        layout.addWidget(self.table_utilisateurs)
        self.tab_utilisateurs.setLayout(layout)

        # === Connexion des boutons ===
        self.btn_ajouter_utilisateur.clicked.connect(self.ajouter_utilisateur)
        self.btn_modifier_utilisateur.clicked.connect(self.modifier_utilisateur)
        self.btn_supprimer_utilisateur.clicked.connect(self.supprimer_utilisateur)
        self.table_utilisateurs.itemSelectionChanged.connect(self.remplir_champs_utilisateur)

        self.refresh_utilisateur_table()


    def refresh_utilisateur_table(self):
        utilisateurs = obtenir_utilisateurs()
        self.table_utilisateurs.setRowCount(len(utilisateurs))
        for row_idx, utilisateur in enumerate(utilisateurs):
            for col_idx, data in enumerate(utilisateur):
                self.table_utilisateurs.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def ajouter_utilisateur(self):
        nom = self.nom_utilisateur_input.text()
        role = self.role_utilisateur_input.text()
        mdp = self.mdp_utilisateur_input.text()

        if nom and mdp:
            ajouter_utilisateur(nom, mdp, role)
            self.refresh_utilisateur_table()
            QMessageBox.information(self, "Succès", "Utilisateur ajouté avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def remplir_champs_utilisateur(self):
        selected_row = self.table_utilisateurs.currentRow()
        if selected_row == -1:
            return  # Aucun utilisateur sélectionné

        # Récupérer les informations de l'utilisateur sélectionné
        id_utilisateur = self.table_utilisateurs.item(selected_row, 0).text()
        nom_utilisateur = self.table_utilisateurs.item(selected_row, 1).text()
        mdp_utilisateur = self.table_utilisateurs.item(selected_row, 2).text()

        # Vérifier si la cellule du rôle existe avant d'essayer d'y accéder
        role_utilisateur_item = self.table_utilisateurs.item(selected_row, 3)
        if role_utilisateur_item:
            role_utilisateur = role_utilisateur_item.text()
        else:
            role_utilisateur = ''  # ou définir une valeur par défaut comme ''

        # Afficher les informations dans les champs d'édition
        self.nom_utilisateur_input.setText(nom_utilisateur)
        self.mdp_utilisateur_input.setText(mdp_utilisateur)
        self.role_utilisateur_input.setText(role_utilisateur)

    def modifier_utilisateur(self):
        selected_row = self.table_utilisateurs.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un utilisateur.")
            return

        id_utilisateur = self.table_utilisateurs.item(selected_row, 0).text()
        nom = self.nom_utilisateur_input.text()
        mdp = self.mdp_utilisateur_input.text()

        # Récupérer le rôle de l'utilisateur (Assurez-vous que cette ligne récupère correctement le rôle)
        role = self.role_utilisateur_input.text()  # Supposons que vous avez un champ pour le rôle

        print(f"DEBUG: Modification de l'utilisateur {id_utilisateur} - {nom}, {mdp}, {role}")

        # Assurez-vous que tous les champs sont remplis
        if nom and mdp and role:
            # Passer tous les arguments nécessaires à la fonction modifier_utilisateur
            modifier_utilisateur(id_utilisateur, nom, mdp, role)
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
