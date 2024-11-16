CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
);

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    categorie INTEGER,
    quantite_disponible REAL NOT NULL DEFAULT 0,
    unite TEXT NOT NULL,
    FOREIGN KEY(categorie) REFERENCES categories(id)
);

CREATE TABLE mouvements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id INTEGER NOT NULL,
    type_mouvement TEXT NOT NULL,
    quantite REAL NOT NULL,
    date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(ingredient_id) REFERENCES ingredients(id)
);
