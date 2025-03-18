import sqlite3

def creer_triggers():
    conn = sqlite3.connect("vente.db")
    cursor = conn.cursor()

    # Trigger pour l'insertion dans audit_vente après une vente
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS after_insert_vente
        AFTER INSERT ON vente
        BEGIN
            INSERT INTO audit_vente (type_operation, nom_client, design_produit, qtesortie_ancien, qtesortie_nouv, utilisateur)
            SELECT 'INSERT', client.nom, produit.design, 0, NEW.qte_vendue, 'système'
            FROM client, produit
            WHERE client.id = NEW.id_client AND produit.id = NEW.id_produit;
        END;
    ''')

    # Trigger pour mettre à jour le stock après une vente
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_stock
        AFTER INSERT ON vente
        BEGIN
            UPDATE produit
            SET stock = stock - NEW.qte_vendue
            WHERE id = NEW.id_produit;
        END;
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    creer_triggers()
    print("Triggers créés avec succès.")
