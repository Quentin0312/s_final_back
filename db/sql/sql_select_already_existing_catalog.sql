SELECT
    id_catalog
FROM
    Catalog
WHERE
    Catalog.start_date NOTNULL
    AND Catalog.end_date NOTNULL