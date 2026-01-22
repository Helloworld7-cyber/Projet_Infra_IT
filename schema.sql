-- On retire les "DROP TABLE" pour ne pas effacer les données existantes

CREATE TABLE IF NOT EXISTS livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    disponible BOOLEAN DEFAULT 1,
    stock INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS taches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT,
    echeance DATE,
    terminee BOOLEAN DEFAULT 0
);
