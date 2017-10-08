# -*- coding: utf-8 -*-
import scrapy
from funding_monitor.items import FundingMonitorItem
import json


class TechinasiaSpider(scrapy.Spider):
    name = 'techinasia'
    allowed_domains = ['techinasia.com']
    start_urls = ['https://www.techinasia.com/wp-json/techinasia/2.0/categories/startups/posts?page=1&per_page=30']

    def parse(self, response):
      jsonresponse = json.loads(response.body_as_unicode())

      # metadata from response
      current_page = int(jsonresponse['current_page'])
      total_pages = int(jsonresponse['total_pages'])
      articles = jsonresponse['posts']

      for article in articles:
        item = FundingMonitorItem()
        item['article_id'] = article["id"]
        item['article_title'] = article["title"]
        item['story_url'] = article["link"]
        item['author'] = article['author']['display_name']
        item['time'] = article['date_gmt']
        item['content'] = article['content']

        yield item

      # check end of list
      next_page_no = current_page + 1
      if next_page_no <= total_pages:
        yield response.follow(self.query_url(page=current_page + 1), self.parse)

    def query_url(self, page, per_page=30):
      return 'https://www.techinasia.com/wp-json/techinasia/2.0/categories/startups/posts?page={page}&per_page={per_page}'.format(page=page, per_page=per_page)
