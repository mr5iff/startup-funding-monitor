# -*- coding: utf-8 -*-
import scrapy
from funding_monitor.items import FundingMonitorItem
import json

queryly_key='80afd98519704a1b'
query='funding'
endindex=0
batchsize=100
showfaceted='false'

def create_url(queryly_key=queryly_key,
    query=query,
    endindex=endindex,
    batchsize=batchsize,
    showfaceted=showfaceted
    ):
    return 'https://api.queryly.com/json.aspx?queryly_key={queryly_key}&query={query}&endindex={endindex}&batchsize={batchsize}&showfaceted={showfaceted}&extendeddatafields=brand&timezoneoffset=-480'.format(
        queryly_key=queryly_key,
        query=query,
        endindex=endindex,
        batchsize=batchsize,
        showfaceted=showfaceted
        )

# {
#   "metadata": {
#     "query": "funding",
#     "total": 13899,
#     "endindex": 100,
#     "correction": "",
#     "suggest": "funding",
#     "filters": [],
#     "functions": []
#   },
#   "related": [
#     "funding round",
#     "venture capital",
#     "new fund",
#     "female entrepreneur",
#     "get fund"
#   ],
#   "items": [
#     {
#       "_id": 173393,
#       "index": 0,
#       "title": "Is It Time to Raise VC Funding? Ask Yourself These 4 Questions to Find Out",
#       "name": "Is It Time to Raise VC Funding? Ask Yourself These 4 Questions to Find Out",
#       "link": "http://www.inc.com/debbie-madden/4-reasons-you-dont-need-vc-money-for-your-startup.html",
#       "description": "Global venture capital funding reached a decade-high of $155 billion in 2017, according to auditing firm KPMG. That's a whole lot of funding. Yet, it might surprise you to learn that only 0.62 percent of startups raise VC funding. It's tempting to try and raise VC money as soon as possible. But, raising VC money isn't always a good idea. It's often a huge distraction, and ultimately unnecessary. Before you go out and try to raise a VC round, take a minute to ask yourself if you really need it. T",
#       "pubdate": "Jul 26, 2018",
#       "pubdateunix": 1532603940,
#       "image": "https://www.incimages.com/uploaded_files/image/970x450/getty_505872010_361904.jpg",
#       "isad": 0,
#       "_type": 0,
#       "feedname": "",
#       "brand": "",
#       "timestamp": "7/26/2018 11:19:00 AM"
#     },

class IncSpider(scrapy.Spider):
    name = 'inc'
    allowed_domains = ['inc.com', 'queryly.com']
    start_urls = [create_url()]
    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        # metadata from response
        endindex = int(jsonresponse['metadata']['endindex'])
        total = int(jsonresponse['metadata']['total'])
        articles = jsonresponse['items']

        for article in articles:
            item = FundingMonitorItem()
            item['article_id'] = str(article["_id"])
            item['article_title'] = article["title"]
            item['story_url'] = article["link"]
            # item['author'] = article['author']['display_name']
            item['time'] = article['timestamp']
            item['content'] = article['description']

            yield item

        if endindex <= total:
            yield response.follow(self.query_url(index=endindex), self.parse)

    def query_url(self, index):
        return create_url(endindex=index)
