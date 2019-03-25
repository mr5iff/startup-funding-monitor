from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from notify import send_telegram_msg

setting = get_project_settings()
process = CrawlerProcess(setting)

for spider_name in process.spider_loader.list():
    print("Running spider %s" % (spider_name))
    process.crawl(spider_name)

send_telegram_msg(f'startup-funding-monitor: start - {datetime.now()}')
process.start()  # the script will block here until all crawling jobs are finished
send_telegram_msg(f'startup-funding-monitor: end - {datetime.now()}')
