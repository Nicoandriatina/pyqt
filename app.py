import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
    QHBoxLayout, QHeaderView, QComboBox
)
from PyQt6.QtCore import Qt

class VenteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Ventes")
        self.setGeometry(100, 100, 1200, 700)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setStyleSheet("""
            QWidget { background-color: #f0f0f0; font-family: Arial, sans-serif; }
            QLabel { font-size: 16px; font-weight: bold; color: #333; }
            QLineEdit, QComboBox { padding: 5px; font-size: 14px; border-radius: 5px; border: 1px solid #ccc; }
            QPushButton { padding: 10px; background-color: #4CAF50; color: white; border-radius: 5px; font-weight: bold; }
            QPushButton:hover { background-color: #45a049; }
            QTableWidget { background-color: white; border-radius: 10px; border: 1px solid #ccc; }
        """)

        # Champs et boutons pour gestion des produits
        self.nom_produit = QLineEdit(self)
        self.nom_produit.setPlaceholderText("Nom du produit")
        layout.addWidget(self.nom_produit)

        self.stock_produit = QLineEdit(self)
        self.stock_produit.setPlaceholderText("Stock initial")
        layout.addWidget(self.stock_produit)

        self.btn_add_produit = QPushButton("Ajouter Produit")
        self.btn_add_produit.clicked.connect(self.ajouter_produit)
        layout.addWidget(self.btn_add_produit)

        self.btn_update_produit = QPushButton("Modifier Produit")
        self.btn_update_produit.clicked.connect(self.modifier_produit)
        layout.addWidget(self.btn_update_produit)

        self.btn_delete_produit = QPushButton("Supprimer Produit")
        self.btn_delete_produit.clicked.connect(self.supprimer_produit)
        layout.addWidget(self.btn_delete_produit)

        # Tableau pour afficher les produits
        self.table_produits = QTableWidget()
        self.table_produits.setColumnCount(3)
        self.table_produits.setHorizontalHeaderLabels(["ID", "Nom", "Stock"])
        layout.addWidget(self.table_produits)
        self.afficher_produits()

        self.setLayout(layout)

    def ajouter_produit(self):
        nom = self.nom_produit.text()
        stock = self.stock_produit.text()
        if not nom or not stock.isdigit():
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des informations valides !")
            return
        conn = sqlite3.connect("vente.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produit (design, stock) VALUES (?, ?)", (nom, int(stock)))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Succès", "Produit ajouté avec succès !")
        self.afficher_produits()

    def modifier_produit(self):
        selected_row = self.table_produits.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un produit à modifier !")
            return
        produit_id = self.table_produits.item(selected_row, 0).text()
        nom = self.nom_produit.text()
        stock = self.stock_produit.text()
        if not nom or not stock.isdigit():
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des informations valides !")
            return
        conn = sqlite3.connect("vente.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE produit SET design=?, stock=? WHERE id=?", (nom, int(stock), produit_id))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Succès", "Produit modifié avec succès !")
        self.afficher_produits()

    def supprimer_produit(self):
        selected_row = self.table_produits.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un produit à supprimer !")
            return
        produit_id = self.table_produits.item(selected_row, 0).text()
        conn = sqlite3.connect("vente.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produit WHERE id=?", (produit_id,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Succès", "Produit supprimé avec succès !")
        self.afficher_produits()

    def afficher_produits(self):
        conn = sqlite3.connect("vente.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produit")
        rows = cursor.fetchall()
        self.table_produits.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                self.table_produits.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VenteApp()
    window.show()
    sys.exit(app.exec())
