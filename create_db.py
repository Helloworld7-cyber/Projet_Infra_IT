import sqlite3

# Connexion à la base (le fichier sera créé s'il n'existe pas)
connection = sqlite3.connect('database.db')

# Lecture du fichier schema.sql pour créer la table 'livres'
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# --- INSERTION DES LIVRES (Séquence 6) ---
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", 
            ('Le Petit Prince', 'Antoine de Saint-Exupéry', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", 
            ('1984', 'George Orwell', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", 
            ('Le Seigneur des Anneaux', 'J.R.R. Tolkien', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", 
            ('Germinal', 'Émile Zola', 1))

# On enregistre les changements et on ferme
connection.commit()
connection.close()
print("Base de données de la bibliothèque initialisée avec succès !")
