# startup-funding-monitor

## What have been done
1. Built a scalable scraper for scraping funding news, using scrapy
2. Trained a LSTM model (with GloVe word embedding) to classify if there is funding information in the news, using keras with tensorflow backend

---

### Install
```
pip install -r requirement.txt
```

---

## Scrapy: Websites to scrape
https://techcrunch.com/2017/09/23/how-to-announce-a-funding-round/

> ... These include (but aren’t limited to): The Wall Street Journal, The New York Times, Forbes, Fortune, TechCrunch, Recode, VentureBeat, Business Insider, Buzzfeed, CNN, and CNBC. Additionally, newsletters like StrictlyVC, Fortune’s TermSheet, Mattermark and Pitchbook include roundup coverage of new financings.

* Recode [Done]
* VentureBeat [Done]
* Techinasia [Done, AJAX]
* TechCrunch [Later]

### Run
Single spider
```
scrapy crawl venturebeat
scrapy crawl techinasia
scrapy crawl recode
```

All spiders
```
python run_all_spiders.py
```

---

## Keras: LSTM model
The model was trained in /classifier/notebooks/news-classifier.ipynb - with 5000+ examples scraped from the scrapy crawlers. The data was first hand labeled with a regex pattern (could be replaced with human annotation), and then the title of the news is being used as the input of the model.


### Accuracy
```
on Epoch 10, loss: 0.4105 - acc: 0.7911 - val_loss: 0.4347 - val_acc: 0.7749
```

### Model Integration
The trained model has been integrated into the scrapy pipeline, and the model will be used to populate the "has_funding_news" field, where 1.0 indicates a high chance of having funding_news, and 0.0 for low chances. (See /funding_monitor/funding_monitor/output/techinasia_items_1507446655.json for example)