# -*- coding: utf-8 -*-
import scrapy
from funding_monitor.items import FundingMonitorItem


class RecodeSpider(scrapy.Spider):
    name = 'recode'
    allowed_domains = ['recode.net']
    # start_urls = ['http://recode.com/']

    def start_requests(self):
        urls = [
            'https://www.recode.net/search?q=raise&type=Article',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_article_header)

    def parse_article_header(self, response):
        articles = response.css('div.c-entry-box--compact__body')
        for article in articles:
            story_url = (article.css('.c-entry-box--compact__title a[data-analytics-link="article"]::attr(href)')
                         .extract_first())

            meta = {
                'article_id': article.css('a[data-entry-admin]::attr(data-entry-admin)').extract_first(),
                'article_title': (article.css('.c-entry-box--compact__title a[data-analytics-link="article"]::text')
                                  .extract_first()),
                'story_url': story_url,
                'time': article.css('time::text').extract_first().strip(),
                'author': article.css('a[href^="https://www.recode.net/authors/"]::text').extract_first(),
            }
            item = FundingMonitorItem(meta)

            yield response.follow(story_url, self.parse_article_body, meta={'item': item})

        # follow next page
        url_next_page = response.css('a.c-pagination__next.c-pagination__link::attr(href)').extract_first()
        if url_next_page:
            yield scrapy.Request(url=response.urljoin(url_next_page), callback=self.parse_article_header)

    def parse_article_body(self, response):
        article_content = response.css('div.c-entry-content p')
        item = response.meta['item']
        item['content'] = article_content.css('::text').extract()

        yield item
