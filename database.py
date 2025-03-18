import sqlite3

def creer_base_de_donnees():
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()

    # Table utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('admin', 'client')) NOT NULL
        )
    ''')

    # Table produits
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prix REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # Table clients
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL
        )
    ''')

    # Table vente (correction des références des clés étrangères)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            produit_id INTEGER NOT NULL,
            quantite INTEGER NOT NULL,
            date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (produit_id) REFERENCES produits(id)
        )
    """)

    conn.commit()

    # Vérification si la table vente est bien créée
    cursor.execute("PRAGMA table_info(ventes)")
    columns = cursor.fetchall()
    if not columns:
        print(" Erreur : la table 'vente' n'a pas été créée correctement.")
    else:
        print(" Base de données initialisée avec succès !")

    conn.close()

### === FONCTIONS POUR LES PRODUITS === ###
def ajouter_produit(nom, prix, stock):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produits (nom, prix, stock) VALUES (?, ?, ?)", (nom, prix, stock))
    conn.commit()
    conn.close()

def modifier_produit(id_produit, nom, prix, stock):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE produits SET nom=?, prix=?, stock=? WHERE id=?", (nom, prix, stock, id_produit))
    conn.commit()
    conn.close()

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
    return produits

### === FONCTIONS POUR LES CLIENTS === ###
def ajouter_client(nom):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (nom) VALUES (?)", (nom,))
    conn.commit()
    conn.close()

def modifier_client(id_client, nom):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE clients SET nom=? WHERE id=?", (nom, id_client))
    conn.commit()
    conn.close()

def supprimer_client(id_client):
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id=?", (id_client,))
    conn.commit()
    conn.close()

def obtenir_clients():
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
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
    cursor.execute("INSERT INTO ventes (client_id, produit_id, quantite, date) VALUES (?, ?, ?, datetime('now'))",
                   (client_id, produit_id, quantite))
    conn.commit()
    conn.close()

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

def ajouter_utilisateur(username, password, role):
    """Ajoute un nouvel utilisateur."""
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)",
                       (username, password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        print("❌ Nom d'utilisateur déjà pris !")
    conn.close()

def modifier_utilisateur(id_utilisateur, username, password, role):
    """Modifie les informations d'un utilisateur."""
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE utilisateurs SET username=?, password=?, role=? WHERE id=?",
                   (username, password, role, id_utilisateur))
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

def obtenir_ventes_client(client_nom):
    """Récupère l'historique des achats d'un client."""
    conn = sqlite3.connect("vente.db")  
    cursor = conn.cursor()

    query = """
    SELECT v.id, p.nom AS produit, v.quantite, v.date
    FROM ventes v
    JOIN produits p ON v.produit_id = p.id
    JOIN clients c ON v.client_id = c.id
    WHERE c.nom = ?
    ORDER BY v.date DESC
    """
    
    cursor.execute(query, (client_nom,))
    ventes = cursor.fetchall()

    conn.close()
    return ventes

if __name__ == "__main__":
    creer_base_de_donnees()
