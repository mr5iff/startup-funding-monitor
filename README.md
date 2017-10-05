# startup-funding-monitor

Perform web scraping on any of the startup funding news sites. Brownie points for scraping Javascript/AJAX based sites that don't load immediately. Just the top few articles is fine. Be careful not to send a whole lot of requests at once. Once you have a few articles, train-test them with some other general articles so that you are able to predict whether a particular article has funding news or not

## Websites to scrape
https://techcrunch.com/2017/09/23/how-to-announce-a-funding-round/

... These include (but aren’t limited to): The Wall Street Journal, The New York Times, Forbes, Fortune, TechCrunch, Recode, VentureBeat, Business Insider, Buzzfeed, CNN, and CNBC. Additionally, newsletters like StrictlyVC, Fortune’s TermSheet, Mattermark and Pitchbook include roundup coverage of new financings.

* TechCrunch
* Recode
* VentureBeat [Done]

## Run
```
scrapy crawl venturebeat
```