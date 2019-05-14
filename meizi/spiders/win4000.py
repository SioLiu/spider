# -*- coding: utf-8 -*-
import scrapy
from meizi.items import Win4000Item
import pymongo
import re
import sys


class Win4000Spider(scrapy.Spider):
    name = 'win4000'
    allowed_domains = ['www.win4000.com']
    start_urls = ['http://www.win4000.com/meitu.html']
    # 设置熔断值
    max_count = 20

 
    def parse(self, response):
        strat_request_title_url = response.css('div.tab_box div ul.clearfix li a::attr(href)').extract_first()
        yield scrapy.Request(url=strat_request_title_url, callback=self.titleParse)

    def titleParse(self, response):
        client = pymongo.MongoClient('localhost', 27017)
        # 库名
        db = client['MZIMG']
        # 表名
        # 下载图片去重表名
        FilterDB = db.Win4000
        # 获取下一组图片链接
        title = response.css('div.ptitle h1::text').extract_first()
        next_title = response.css('div.scroll-img-cont span.group-next a::attr(href)').extract_first()
        if FilterDB.find_one({'title_url':response.url}) is None:
            item = Win4000Item()
            # print(title)
            img_urls = response.css('#scroll li a img::attr(data-original)').extract()
            # print('*' * 30, next_title)
            item['title'] = title.strip()
            item['title_url'] = response.url
            item['img_url'] = []
            for img_url in img_urls:
                if 'jpg' not in img_url:
                    continue
                img_url = re.sub('_130_170', '', img_url)
                # print(img_url)
                item['img_url'].append(img_url)
            yield item
        else:
            print(title, response.url, '已经下载过')
            if self.max_count:
                self.max_count -= 1
                if self.max_count < 1:
                    sys.exit('已达到熔断值，系统退出')

        yield scrapy.Request(url=next_title, callback=self.titleParse)
