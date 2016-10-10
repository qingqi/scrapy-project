# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
import time
import datetime

from scrapy.exceptions import DropItem
import MySQLdb


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class SaveToDBPipeline(object):
    def __init__(self):
        self.db = MySQLdb.connect(host='10.95.118.125', user='test', passwd='ceshi', port=8733, db='scrapy', charset='utf8')
        self.cursor = self.db.cursor()
        self.cursor.execute('select house_sell_id from scrapy.lj_house where crawl_date >= curdate() and crawl_date <adddate(curdate(), 1)')
        data = self.cursor.fetchall()
        data = list(data)  
        data = [x[0] for x in data]  # list of unicode string
        self.saved_set = set(data)

    def process_item(self, item, spider):
        if item['houseSellId'] in self.saved_set:
            return
        self.saved_set.add(item['houseSellId'])

        sql = "insert into lj_house(house_sell_id, acreage, ave_price, total_price, district_name, \
            plate_name, property_name, property_no, crawl_date) values('%(houseSellId)s',\
             %(acreage)f, %(unitPrice)f, %(showPrice)f, '%(districtName)s', '%(plateName)s', \
             '%(propertyName)s', '%(propertyNo)s', curdate())"
        sql = sql % item
        self.cursor.execute(sql)

