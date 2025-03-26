import sqlite3

def creer_triggers():
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()

    # Trigger pour INSERT sur vente
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS after_insert_vente
        AFTER INSERT ON ventes
        BEGIN
            -- Mise à jour du stock
            UPDATE produit
            SET stock = stock - NEW.qte_sortie
            WHERE n_produit = NEW.n_produit;

            -- Enregistrement de l'opération dans audit_vente
            INSERT INTO audit_vente (type_operation, date_maj, nom, design, qte_sortie_ancien, qte_sortie_nouv, utilisateur)
            SELECT 'INSERT', datetime('now'), client.nom, produit.design, 0, NEW.qte_sortie, 'système'
            FROM client, produit
            WHERE client.n_client = NEW.n_client AND produit.n_produit = NEW.n_produit;
        END;
    ''')

    # Trigger pour UPDATE sur vente
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS after_update_vente
        AFTER UPDATE ON ventes
        BEGIN
            -- Mise à jour du stock en fonction de la nouvelle quantité vendue
            UPDATE produit
            SET stock = stock + OLD.qte_sortie - NEW.qte_sortie
            WHERE n_produit = NEW.n_produit;

            -- Enregistrement de l'opération dans audit_vente
            INSERT INTO audit_vente (type_operation, date_maj, nom, design, qte_sortie_ancien, qte_sortie_nouv, utilisateur)
            SELECT 'UPDATE', datetime('now'), client.nom, produit.design, OLD.qte_sortie, NEW.qte_sortie, 'système'
            FROM client, produit
            WHERE client.n_client = NEW.n_client AND produit.n_produit = NEW.n_produit;
        END;
    ''')

    # Trigger pour DELETE sur vente
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS after_delete_vente
        AFTER DELETE ON ventes
        BEGIN
            -- Restauration du stock après suppression de la vente
            UPDATE produit
            SET stock = stock + OLD.qte_sortie
            WHERE n_produit = OLD.n_produit;

            -- Enregistrement de l'opération dans audit_vente
            INSERT INTO audit_vente (type_operation, date_maj, nom, design, qte_sortie_ancien, qte_sortie_nouv, utilisateur)
            SELECT 'DELETE', datetime('now'), client.nom, produit.design, OLD.qte_sortie, 0, 'système'
            FROM client, produit
            WHERE client.n_client = OLD.n_client AND produit.n_produit = OLD.n_produit;
        END;
    ''')

    conn.commit()
    conn.close()
    print("Triggers créés avec succès.")

if __name__ == "__main__":
    creer_triggers()
