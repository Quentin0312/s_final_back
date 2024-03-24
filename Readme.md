##### Run locally:

`uvicorn main:app --reload`

##### Ordre d'éxection des scripts de scrapping:

- `get_all_refs.py`
- `get_links.py`
- `download_images.py`

##### Ordre de remplissage de la db:

Training v1:

- `initial_import_analytic_database.py` (write on db)
- `data_labelizer` (write in a .txt file)
- `update_labels_analytic.py` (write on db)

Training v2:

- `initial_import_analytic_database_multi-class.py` (write on db)
- `data_labelizer_multi-class.py` (write in a .txt file)
- `update_labels_analytic_multi-class.py` (write on db)

Application db:

- `full_import_initial.py` (write on db)
- `inference_on_db` (write on db)

Prod db:

Création:

- `create_db.py`

Updating:

- `final_scraping.py`
- TODO: nlp_labelizer.py

---

# Prod db full creation process

## Data scrapping

## Create prod db :

create_db_final.py

## Initial import :

initial_import_prod_final.py ??? OU final_scrapping.ipynb

## Insert db page_categories with model inference

4
