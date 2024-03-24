SELECT
    image_path,
    "Catalog".start_date,
    "Catalog".end_date,
    Page_categories.id_category,
    Page.id_catalog
FROM
    Page
    JOIN "Catalog" ON Page.id_catalog = "Catalog".id_catalog
    JOIN Page_categories ON Page_categories.id_page = Page.id_page
WHERE
    text LIKE ?