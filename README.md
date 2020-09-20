# README
> This is my work for the sixth project, the capstone project, of the Data Scientist Nanodegree Program from Udacity.


## Motivation
It happens that I'm a PhD in the Biological Sciences, with main focus on zoological taxonomy (actually, a specific family of insects), the science that describes and classifies biodiversity. One of the things that always annoyed me is how the FAIR principles are fairly unknown among my community. Alongside with this, I always wanted to know which journals are the major contributors to the discovery of new species.

Allied to what I just said, this project forced me to work a lot on the ETL part of the Data Scientist's life, which I think is a major skill to acquire. Often we work with ready-to-go datasets, but in this project, I had to work hard to get the data, connecting five different service providers. The analyses might be simplistic, but it does answer the three main questions of this project:

- How much of the newly discovered data end up behind paywalls?
- Who are the biggest journals in the science of discovering and describing things?
- How does the sources related to the Zoological Sciences compare to each other in this context?


## Disclaimer
I applied the [Udacity Git Commit Message Style Guide](https://udacity.github.io/git-styleguide/) in this repository, with one addition to the type list: `file`, used when I uploaded or changed non-coding files, like the pickle file.

I also used [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/), hence the [Pipfile](https://github.com/mguidoti/DSND-p1-blog/blob/master/Pipfile) and [Pipfile.lock](https://github.com/mguidoti/DSND-p1-blog/blob/master/Pipfile.lock) in this repository.


## Files
```
|--p6-capstone
  |--data
    |--wos
      |--*.txt (156x)
    |--df_final.p                      # Pickle file with the transformed, final df
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
      |--config.py                      # Uncommited. Contains API keys to SHERPA/RoMEO
      |--doaj.py                      # Connects to DOAJ
      |--sherpa_romeo.py                      # Connects to SHERPA/RoMEO
      |--transform.py                      # Transform routine
    |--load.py                      # Load routine
  |--tests
    |--test_extract.py
    |--test_transform.py
  |--.gitignore
  |--p6-capstone.code-workspace
  |--LICENSE
  |--Pipfile
  |--Pipfile.lock
  |--README.md
  |--sp_nov.ipynb                      # Notebook with the entire rationale behind this project

```


## Libraries
From the available Pipfile:
- pandas
- numpy
- matplotlib
- ipykernel
- scrapy
- requests
- sqlalchemy


## Installing & Running
First, install [Pipenv], then run close this repository. On the command line, navigate to the cloned repo folder and type `pipenv install`. This should take care of installing all libraries and their dependecies.

To run this project, you can simply open `sp_np.ipynb`. This is the jupyter notebook that will guide you through the entire process. Please, note that this notebook calls a lot of modularized functions that I wrote, and you can find them on /etl/extract, /etl/transform and /test_units.

In order to run the web scraper I wrote to gather data from [Zoobank](http://www.zoobank.org), navigate to `/etl/extract` and run `scrapy crawl zoobank`. This is due the fact that I used a [Scrapy]() project, with custom ItemLoaders, in- and out-processors, ItemPipelines, and I can't run a CrawlerProcess with all these custom functionalities from Jupyter Notebook, apparently. However, this is not needed. On `sp_np.ipynb` I simply load the resulting SQLite database from this scraper.


## Summary of Results
### How much of the newly discovered data end up behind paywalls?
Turns out that the two sources of information where one can grab this data are extremely incomplete. Up to **60.27%** of the journals present on the final dataframe couldn't be retrieved, and **8.04%** were ambiguous (either GOLD or DIAMOND models).
However, when looking at the data that we actually got, only **4.46%** of the journals are DIAMOND open-access, which means, the articles are made freely available without any Authors' Processing Charges (APCs).

### Who are the biggest journals in the science of discovering and describing things?
It depends on the source. For Web of Science/Zoological Records, the top three were: Zootaxa, ZooKeys and Cretaceous Research, with 21.05%, 4.29% and 0.99% of the articles that describing zoological species.

For TreatmentBank, the top three is composed by Zootaxa (69.29%), ZooKeys (16.79%) and European Journal of Taxonomy (2.98%).

In Zoobank Zootaxa (39.80%), ZooKeys (9.77%) and Journal of Threatened Taxa (2.30%).

Clearly, Zootaxa and ZooKeys are the top 2 across the board, and Zootaxa is by far the biggest contributor. These differences were briefly discussed on the [blog post](https://hackmd.io/@mguidoti/S1veVwNHv), which is the actual deliverable of this project.

### How does the sources related to the Zoological Sciences compare to each other in this context?
Despite the differences on the journal rankings, the size of the sources were remarkably different as well: WoS/Zoological Records, TreatmentBank and Zoobank presented, respectivelly, 80,194, 39,209 and 18,955 recors, filtered down to 46,531, 31,272 and 18,859. The top 25 journals represented, for each one of these sources, 39.14%, 98.15% and 66.15% of the data on their datasets. The significance of these results were also addressed on the [project deliverable](https://hackmd.io/@mguidoti/S1veVwNHv).


## Acknowledgements
There are two particular tutorials that I would like to thank:

- [A minimalist end-to-end Scrapy tutorial - Part III](https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-iii-bcd94a2e8bf3)
- [SQLite in Python?](https://www.datacamp.com/community/tutorials/sqlite-in-python?utm_source=adwords_ppc&utm_campaignid=1455363063&utm_adgroupid=65083631748&utm_device=c&utm_keyword=&utm_matchtype=b&utm_network=g&utm_adpostion=&utm_creative=278443377092&utm_targetid=aud-438999696719:dsa-429603003980&utm_loc_interest_ms=&utm_loc_physical_ms=1001686&gclid=Cj0KCQjwtZH7BRDzARIsAGjbK2aeMsVsC9GdjzbWJffg-LtBVHHW10y6XVdl78zuzZ7DPWU4S6gOiacaAql6EALw_wcB)

That and many, many questions and answers on [Stack Overflow](). Too many to count.


## License
MIT