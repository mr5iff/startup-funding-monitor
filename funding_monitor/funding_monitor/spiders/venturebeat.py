# -*- coding: utf-8 -*-
import scrapy
from funding_monitor.items import FundingMonitorItem


class VenturebeatSpider(scrapy.Spider):
    name = "venturebeat"
    allowed_domains = ["venturebeat.com"]
    # start_urls = ['http://venturebeat.com/']

    def start_requests(self):
        urls = [
            'https://venturebeat.com/page/1/?s=raise',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_article_header)

    def parse_article_header(self, response):
      articles = response.css('article')
      for article in articles:
        story_url = article.css('header.article-header a::attr(href)').extract_first()

        meta = {
            'article_id': article.css('::attr(id)').extract_first(),
            'artile_title': article.css('header.article-header a::attr(title)').extract_first(),
            'story_url': story_url,
            'time': article.css('time::attr(datetime)').extract_first(),
            'author': article.css('a[rel="author"]::text').extract_first(),
        }
        item = FundingMonitorItem(meta)

        yield response.follow(story_url, self.parse_article_body, meta={'item': item})

      # follow next page
      url_next_page = response.css('a.next.page-numbers::attr(href)').extract_first()
      if url_next_page:
        yield scrapy.Request(url=url_next_page, callback=self.parse_article_header)

    def parse_article_body(self, response):
      article_content = response.css('div.article-content p')
      item = response.meta['item']
      item['content'] = article_content.css('::text').extract()

      yield item
