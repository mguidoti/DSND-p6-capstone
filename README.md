# README
> This is my work for the fifth project of the Data Scientist Nanodegree Program from Udacity.

## Files
```
|--p6-capstone
  |--data
    |--wos
      |--*.txt (156x)
    |--tb_response.p                      # Pickle file containing the full response from TreatmentBank API's, to test .db data consistency later
    |--tb.db                      # Snapshot for TB data used in the project
    |--wos.p                      # Not added due to the file size
    |--zb.db                      # Snapshot for Zoobank data used in the project
  |--etl
    |--extract
      |--zb
        |--logs
          |--zb-scraper.txt                      # Log from scraper
        |--spiders
          |--__init__.py
          |--zoobank.py                      # Spider used to scrape Zoobank
        |--__init__.py
        |--items.py                      # Item and custom ItemLoader and in- and out-processors used in this scraper
        |--middlewares.py
        |--models.py                      # Model created to save scraped data into a SQLite database
        |--pipelines.py                      # Custom ItemPipeline used in this project
        |--settings.py                      # There are some settings added by me here
      |--scrapy.cfg
      |--tb_model.py                      # Model used to save the data from TreatmentBank into a SQLite database
      |--tb.py                      # TreatmentBank processing script
      |--wos.py                      # Zoological Records parser
    |--transform
      |--sherpa_romeo.py (maybe I'll delete it)
      |--transform.py                      # Transform routine
    |--load.py                      # Load routine
  |--.gitignore
  |--p6-capstone.code-workspace
  |--Pipfile
  |--Pipfile.lock
  |--README.md
  |--sp_nov.ipynb                      # Notebook with the entire rationale behind this project
```