# -*- coding: utf-8 -*-

# Scrapy settings for funding_monitor project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import os
from botocore import configloader

BOT_NAME = 'funding_monitor'

SPIDER_MODULES = ['funding_monitor.spiders']
NEWSPIDER_MODULE = 'funding_monitor.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'funding_monitor (+http://www.yourdomain.com)'
USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)'
              ' AppleWebKit/537.36 (KHTML, like Gecko)'
              ' Chrome/60.0.3112.113 Safari/537.36')

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'funding_monitor.middlewares.FundingMonitorSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'funding_monitor.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'funding_monitor.pipelines.FundingMonitorPipeline': 100,
    # 'funding_monitor.pipelines.NaiveDropDuplicatesPipeline': 150,
    # 'funding_monitor.pipelines.FundingNewsClassifierPipeline': 200,
    # 'funding_monitor.pipelines.JsonWriterPipeline': 300,
    'funding_monitor.pipelines.S3WriterPipeline': 350,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Model path for Keras model
STEPS_LEN = 33  # max number of tokens to be used
CLASSIFIER_MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../classifier/model/fundingNewsClassifier.h5')

# AWS
# aws_config = configloader.multi_file_load_config('~/.aws/credentials')['profiles'].get('default', {})

# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', aws_config.get('aws_access_key_id'))
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', aws_config.get('aws_secret_access_key'))
# AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME', aws_config.get('aws_region_name'))
# AWS_ENDPOINT_URL = os.environ('AWS_ENDPOINT_URL')  # only needed for S3-like storage, for example Minio or s3.scality
AWS_VERIFY = os.environ.get('AWS_VERIFY', True)

# FEED_URI = 's3://startup-monitor/scraping/feeds/%(name)s/%(name)s_%(time)s.json'
# FEED_FORMAT = 'jsonlines'
# FEED_EXPORTERS = {
#     'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
# }
