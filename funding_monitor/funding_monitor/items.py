# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FundingMonitorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_id = scrapy.Field()
    artile_title = scrapy.Field()
    story_url = scrapy.Field()
    time = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
