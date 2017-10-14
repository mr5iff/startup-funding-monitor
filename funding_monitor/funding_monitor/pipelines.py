# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os.path

class FundingMonitorPipeline(object):
    def process_item(self, item, spider):
        item['spider_name'] = spider.name
        item['id'] = '_'.join([item['spider_name'], item['article_id']])
        return item

### JsonWriterPipeline starts
import json
import time

class JsonWriterPipeline(object):
    def open_spider(self, spider):
        timestamp = str(int(time.time()))
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', '{}_items_{}.json'.format(spider.name, timestamp))
        print (filename)
        self.file = open(filename, 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
### JsonWriterPipeline ends


### MongoPipeline starts
import pymongo


class MongoPipeline(object):
    collection_name = 'funding_news'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item

### MongoPipeline ends


### FundingNewsClassifierPipeline starts
import numpy as np
from keras.models import load_model
from keras.preprocessing import sequence
import spacy
from scrapy.utils.project import get_project_settings
# import logging


class FundingNewsClassifierPipeline(object):
    def process_item(self, item, spider):
        # try:
        #     article_title_embedding = self.nlp(item['article_title'])
        #     article_title_embedding_clean = self._clean_word_vector(article_title_embedding)
        #     # padding zero to the front of the word embedding
        #     article_title_embedding_clean_padded = sequence.pad_sequences(article_title_embedding_clean, maxlen=self.steps_len ,dtype='float32')
        #     item['has_funding_news'] = np.asscalar(self.model.predict(article_title_embedding_clean_padded))
        # except Exception as e:
        #     logging.warn(e)
        # finally:
        #     return item

        article_title_embedding = np.expand_dims([self._clean_word_vector(word.vector) for word in self.nlp(item['article_title'])], axis=0)
        # padding zero to the front of the word embedding
        article_title_embedding_clean_padded = sequence.pad_sequences(article_title_embedding, maxlen=self.steps_len ,dtype='float32')
        item['has_funding_news'] = np.asscalar(self.model.predict(article_title_embedding_clean_padded))
        return item

    def open_spider(self, spider):
        settings = get_project_settings()
        model = load_model(settings.get('CLASSIFIER_MODEL_PATH'))
        self.steps_len = settings.get('STEPS_LEN', 33)
        self.model = model
        self.nlp = spacy.load('en', vectors='en_glove_cc_300_1m')
        # try:
        #     self.model = model
        #     self.nlp = spacy.load('en', vectors='en_glove_cc_300_1m')
        # except Exception as e:
        #     logging.warn(e)

    def _clean_word_vector(self, word_vector, upper_bound=1.0e+3, lower_bound=-1.0e+3):
    #     remove nan
    #     print(word_vector)
        word_vector[np.isnan(word_vector)] = 0.0
        return np.clip(word_vector, a_min=lower_bound, a_max=upper_bound)
### FundingNewsClassifierPipeline ends


### NaiveDropDuplicatesPipeline starts
from scrapy.exceptions import DropItem

class NaiveDropDuplicatesPipeline(object):
    """Naive as in it uses in memory ids_seen for the check. Better should use be independent of memory, e.g. cache etc"""
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item
### NaiveDropDuplicatesPipeline ends
