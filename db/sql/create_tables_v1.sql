CREATE TABLE Catalog(
    id_catalog INTEGER PRIMARY KEY AUTOINCREMENT,
    start_date TEXT,
    end_date TEXT
);

CREATE TABLE Category(
    id_category INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE Page(
    id_page INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT,
    type TEXT,
    text TEXT,
   id_category INT,
   id_catalog INT,
   FOREIGN KEY(id_category) REFERENCES Category(id_category),
   FOREIGN KEY(id_catalog) REFERENCES Catalog(id_catalog)
);