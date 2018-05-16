# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from jind.items import JindItem
import urllib.request
import re

class HpSpider(scrapy.Spider):
    name = 'hp'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']

    def parse(self, response):
        key = '惠普'
        for i in range(1,2):#len()
            url = 'https://search.jd.com/Search?keyword='+key+'&enc=utf-8&page='+str(i*2)
            yield Request(url=url,callback=self.page_url)
            #stuff_url
            
    def page_url(self,response):
        #body = response.body.decode('utf-8','ignore')
        goodsid = response.xpath(
            '//ul[@class="gl-warp clearfix"]//li/@data-sku'
            ).extract()
        #print(goodsid)#testwork
        for j in range(0,len(goodsid)):
            thisid = goodsid[j]
            thisurl = 'https://item.jd.com/'+str(thisid)+'.html'
            yield Request(url=thisurl,callback=self.stuff_url)

    def stuff_url(self,response):
        item = JindItem()
        item['title'] = response.xpath(
            '//title/text()'
            ).extract()
        item['link'] = response.url
        
        patid = '(\d*).html'
        goodsid = re.compile(patid).findall(response.url)[0]
        priceurl = 'https://p.3.cn/prices/mgets?&skuIds=J_'+str(goodsid)+'%2CJ'
        #print(priceurl)#testwork
        pricedata = urllib.request.urlopen(priceurl).read().decode('utf-8','ignore')
        pat = '"p":"([\d\.]*)"'
        
        item['price_now'] = re.compile(pat).findall(pricedata)[0]
        #print(item['price_now'])#testwork
        yield item
