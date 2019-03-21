# -*- coding: utf-8 -*-
import scrapy
from funding_monitor.items import FundingMonitorItem
import json
from scrapy.selector import Selector

query='funding'
# per_page=1

class E27Spider(scrapy.Spider):
    name = 'e27'
    allowed_domains = ['e27.co']
    per_page = 1
    # start_urls = [self.query_url()]

    def start_requests(self):
        urls = [
            self.query_url(),
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_article_header)

    def parse_article_header(self, response):
        content = json.loads(response.body_as_unicode())['content']
        articles = Selector(text=content).css('div.row.mbt-m')
        for article in articles:
            story_url = article.css('.pos-rel a::attr(href)').extract_first()

            meta = {
                'article_id': article.css('.list-article-title::text').extract_first(),
                'article_title': article.css('.list-article-title::text').extract_first(),
                'story_url': story_url,
                # 'time': article.css('time::text').extract_first().strip(),
                'author': article.css('.auth-date a::text').extract_first(),
            }
            item = FundingMonitorItem(meta)

            yield response.follow(story_url + '?json', self.parse_article_body, meta={'item': item})

        # follow next page
        self.per_page += 1
        url_next_page = self.query_url(per_page=self.per_page)
        yield scrapy.Request(url=response.urljoin(url_next_page), callback=self.parse_article_header)

    def parse_article_body(self, response):
        article_content = response.css('div.post-content p')
        item = response.meta['item']
        item['content'] = article_content.css('::text').extract()

        yield item

    def query_url(self, query=query, per_page=per_page):
        return 'https://e27.co/search/ajax_search_articles/?all&s={query}&per_page={per_page}'.format(query=query, per_page=per_page)
