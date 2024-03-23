CREATE TABLE
    Catalog (
        id_catalog TEXT,
        start_date TEXT,
        end_date TEXT,
        PRIMARY KEY (id_catalog)
    );

CREATE TABLE
    Category (
        id_category INTEGER,
        name TEXT,
        PRIMARY KEY (id_category)
    );

CREATE TABLE
    Page (
        id_page INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT UNIQUE,
        text TEXT,
        id_catalog INT,
        FOREIGN KEY (id_catalog) REFERENCES Catalog (id_catalog)
    );

CREATE TABLE
    Page_categories (
        id_page INT,
        id_category INT,
        PRIMARY KEY (id_page, id_category),
        FOREIGN KEY (id_page) REFERENCES Page (id_page),
        FOREIGN KEY (id_category) REFERENCES Category (id_category)
    );