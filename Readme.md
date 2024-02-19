##### Run locally:

`uvicorn main:app --reload`

##### Ordre d'éxection des scripts de scrapping:

- `get_all_refs.py`
- `get_links.py`
- `download_images.py`

##### Ordre de remplissage de la db:

Training:

- `initial_import_analytic_database.py` (write on db)
- `data_labelizer` (write in a .txt file)
- `update_labels_analytic.py` (write on db)

Application db:

- `full_import_initial.py` (write on db)
- `inference_on_db` (write on db)

Prod db:

Création:

- `create_db.py`

Updating:

- `final_scraping.py`
- TODO: nlp_labelizer.py
