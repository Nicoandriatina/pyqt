import sqlite3
from PyQt6.QtWidgets import QMessageBox


def reset_database():
    """Supprime et recrée toutes les tables de la base de données."""
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()

    try:
        # Suppression des anciennes tables
        cursor.executescript("""
        DROP TABLE IF EXISTS ventes;
        DROP TABLE IF EXISTS produits;
        DROP TABLE IF EXISTS utilisateur;
        DROP TABLE IF EXISTS audit_vente;
        """)

        # Recréation des tables
        cursor.executescript("""
        CREATE TABLE utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE NOT NULL,
            role TEXT CHECK(role IN ('admin', 'client')) NOT NULL
        );

        CREATE TABLE produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE NOT NULL,
            stock INTEGER NOT NULL
        );

        CREATE TABLE ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            produit_id INTEGER NOT NULL,
            quantite INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES utilisateur(id),
            FOREIGN KEY (produit_id) REFERENCES produits(id)
        );

        CREATE TABLE audit_vente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vente_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vente_id) REFERENCES ventes(id)
        );
        """)

        conn.commit()
        print("Base de données réinitialisée avec succès.")

    except sqlite3.Error as e:
        print(f"Erreur lors de la réinitialisation : {e}")

    finally:
        conn.close()

### === FONCTIONS POUR LES PRODUITS === ###
def ajouter_produit(nom, prix, stock):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produits (nom, prix, stock) VALUES (?, ?, ?)", (nom, prix, stock))
    conn.commit()
    conn.close()


def modifier_produit(id_produit, nom, stock, prix):
    # Connexion à la base de données
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    
    # Exécution de la requête de mise à jour du produit
    cursor.execute("""
        UPDATE produits
        SET nom = ?, stock = ?, prix = ?
        WHERE id = ?
    """, (nom,stock,prix, id_produit))
    
    # Validation de la modification et fermeture de la connexion
    conn.commit()

def supprimer_produit(id_produit):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produits WHERE id=?", (id_produit,))
    conn.commit()
    conn.close()

def obtenir_produits():
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()
    conn.close()
     # Débogage : Vérifiez ce qui est récupéré
    print(f"DEBUG: Produits récupérés - {produits}")
    return produits

### === FONCTIONS POUR LES CLIENTS === ###
def ajouter_client(nom):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO utilisateurs (nom) VALUES (?)", (nom,))
    conn.commit()
    conn.close()

def modifier_client(id_client, nom):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE utilisateurs SET nom=? WHERE id=?", (nom, id_client))
    conn.commit()
    conn.close()

def supprimer_client(id_client):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM utilisateurs WHERE id=?", (id_client,))
    conn.commit()
    conn.close()

def obtenir_clients():
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs")
    clients = cursor.fetchall()
    conn.close()
    return clients

# FONCTIONS POUR LES VENTES
def obtenir_ventes():
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, client_id, produit_id, quantite, date FROM ventes")
    ventes = cursor.fetchall()
    conn.close()
    return ventes


def ajouter_vente(client_id, produit_id, quantite):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()

    try:
        # Vérifier le stock disponible
        cursor.execute("PRAGMA table_info(produits);")  # Vérifie la structure de la table
        print("DEBUG - Structure de produits :", cursor.fetchall())

        cursor.execute("SELECT stock FROM produits WHERE id = ?", (produit_id,))
        # cursor.execute("SELECT stock FROM produits WHERE id = ?", (produit_id,))
        produit = cursor.fetchone()

        if produit is None:
            print("DEBUG - Produit introuvable")
            return False  # Produit introuvable

        stock_disponible = produit[0]

        if stock_disponible < quantite:
            print("DEBUG - Stock insuffisant")
            return False  # Stock insuffisant

        # Insérer la vente
        print(f"DEBUG - Ajout vente | client_id: {client_id}, produit_id: {produit_id}, quantite: {quantite}")
        cursor.execute("INSERT INTO ventes (client_id, produit_id, quantite, date) VALUES (?, ?, ?, datetime('now'))",
                       (client_id, produit_id, quantite))

        # Mettre à jour le stock du produit
        nouveau_stock = stock_disponible - quantite
        cursor.execute("UPDATE produits SET stock = ? WHERE id = ?", (nouveau_stock, produit_id))

        conn.commit()
        print("DEBUG - Vente ajoutée avec succès")
        return True  # Vente réussie

    except sqlite3.Error as e:
        print(f"DEBUG - Erreur SQLite : {e}")
        return False

    finally:
        conn.close()


# def ajouter_vente(username, id_produit, quantite):
#     print(f"DEBUG - ajouter_vente appelé avec: {username}, {id_produit}, {quantite}")
#     return True  # Simule un achat réussi


def modifier_vente(id_vente, nouvelle_quantite):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE ventes SET quantite = ? WHERE id = ?", (nouvelle_quantite, id_vente))
    conn.commit()
    conn.close()

def supprimer_vente(id_vente):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ventes WHERE id = ?", (id_vente,))
    conn.commit()
    conn.close()

### === FONCTIONS POUR LES UTILISATEURS === ###

def ajouter_utilisateur(nom, password, role):
    """Ajoute un nouvel utilisateur."""
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO utilisateurs (nom, password, role) VALUES (?, ?, ?)",
                       (nom, password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        print(" Nom d'utilisateur déjà pris !")
    conn.close()

def modifier_utilisateur(id_utilisateur, nom, mdp, role):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()

    # Exécuter la requête pour mettre à jour l'utilisateur dans la base de données
    cursor.execute("""
        UPDATE utilisateurs
        SET nom = ?, password = ?, role = ?
        WHERE id = ?
    """, (nom, mdp, role, id_utilisateur))

    conn.commit()
    conn.close()



def supprimer_utilisateur(id_utilisateur):
    """Supprime un utilisateur de la base de données."""
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM utilisateurs WHERE id=?", (id_utilisateur,))
    conn.commit()
    conn.close()

def obtenir_utilisateurs():
    """Récupère la liste des utilisateurs."""
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs")
    utilisateurs = cursor.fetchall()
    conn.close()
    return utilisateurs

def obtenir_ventes_client():
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ventes")  # Sélectionne toutes les ventes
    ventes = cursor.fetchall()

    conn.close()
    return ventes  # Retourne toutes les ventes


#resaka audit
def obtenir_audit_ventes():
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()

    # Récupérer tous les logs d'audit
    cursor.execute("SELECT action, date, vente_id FROM audit_vente")
    logs = cursor.fetchall()

    # Compter les insertions, modifications et suppressions
    insertions = sum(1 for log in logs if log[0] == "INSERT")
    modifications = sum(1 for log in logs if log[0] == "UPDATE")
    suppressions = sum(1 for log in logs if log[0] == "DELETE")

    conn.close()
    return logs, insertions, modifications, suppressions


    

if __name__ == "__main__":
    reset_database()
