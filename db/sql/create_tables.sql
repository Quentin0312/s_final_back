-- TODO: Rename page_image to image_path
CREATE TABLE
    Pages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        page_image TEXT,
        content TEXT
    )