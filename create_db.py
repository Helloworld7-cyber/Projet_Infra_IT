import sqlite3

connection = sqlite3.connect('database.db')

# 1. On lance le schema.sql (assure-toi qu'il utilise "CREATE TABLE IF NOT EXISTS")
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# 2. On vérifie si la table livres est vide avant d'insérer (pour éviter les doublons)
cur.execute("SELECT count(*) FROM livres")
if cur.fetchone()[0] == 0:
    print("Insertion des livres de test...")
    cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", 
                ('Le Petit Prince', 'Antoine de Saint-Exupéry', 1))
    cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", 
                ('1984', 'George Orwell', 1))

# 3. Insertion d'une tâche de test (Optionnel - Mini-Projet) [cite: 1, 8]
cur.execute("SELECT count(*) FROM taches")
if cur.fetchone()[0] == 0:
    print("Insertion d'une tâche de test...")
    cur.execute("INSERT INTO taches (titre, description, echeance) VALUES (?, ?, ?)",
                ('Finir le projet IT', 'Coder les routes de la bibliothèque', '2024-06-01'))

connection.commit()
connection.close()
print("Base de données (Livres + Tâches) prête !")
