SELECT
    Page.id_page,
    Page.text,
    Page_categories.id_page
FROM
    Page
    LEFT JOIN Page_categories ON Page.id_page = Page_categories.id_page
WHERE
    Page_categories.id_page IS NULL