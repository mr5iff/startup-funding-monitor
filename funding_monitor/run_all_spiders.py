from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

setting = get_project_settings()
process = CrawlerProcess(setting)

for spider_name in process.spider_loader.list():
    print ("Running spider %s" % (spider_name))
    process.crawl(spider_name)

process.start()  # the script will block here until all crawling jobs are finished
