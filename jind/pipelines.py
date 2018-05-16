# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JindPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host='localhost',user='root',passwd='142857',port=3306,db='jdlaptop')
        self.cursor = self.db.cursor()
        #self.cursor.execute('USE jdlaptop')
    def process_item(self, item, spider):
        try:
            title = item['title'][0]
            link = item['link']
            price = item['price_now']
            
            print(title)
            print(link)
            print(price)
            
            sql = "insert into laptop(title,link,price) values(%s,%s,%s)"
            self.cursor.execute(sql,tuple(title,link,price))
            self.db.commit()
            return item
        except Exception as err:
            pass
    
    def close_spider(self):
        self.db.close()