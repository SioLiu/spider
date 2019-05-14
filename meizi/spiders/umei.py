# -*- coding: utf-8 -*-
import scrapy
from meizi.items import UmeiItem
import sys
import pymongo


class UmeiSpider(scrapy.Spider):
    name = 'umei'
    allowed_domains = ['www.umei.cc']
    start_urls = ['http://www.umei.cc/meinvtupian/', 'http://www.umei.cc/bizhitupian/meinvbizhi/']

    def parse(self, response):
        client = pymongo.MongoClient('localhost', 27017)
        # 库名
        db = client['MZIMG']
        # 表名
        # 下载图片去重表名
        title_Duplicates = db.Umei
        # print(response.text)
        titles = response.css('body div.TypeList ul a.TypeBigPics')
        count_pages = response.css(
            'body div.NewPages ul li a:contains("末页")::attr(href)').extract_first().split('.')[0]
        for one_title in titles:
            title_url = one_title.css('a::attr(href)').extract_first()
            title = one_title.css('a div.ListTit::text').extract_first()
            try:
                if title_Duplicates.find_one({'title_url': title_url}) is None:
                    item = UmeiItem()
                    # print(title, title_url)
                    item['title_url'] = title_url
                    item['title'] = title
                    item['img_url'] = []
                    yield scrapy.Request(url=title_url, meta={'item': item}, callback=self.title_parse)
                else:
                    print('{}: {} 已经存在'.format(title, title_url))
            except Exception as erro:
                print('去重出错：{}'.format(erro))
        for next_page in range(1, (eval(count_pages) + 1)):
            page_url = '{}{}.htm'.format(self.start_urls[0], next_page)
            # print(page_url)
            yield scrapy.Request(url=page_url, callback=self.parse)

    def title_parse(self, response):
        item = response.meta['item']
        next_img_url = response.css(
            'body div.wrap div.NewPages ul li a:contains("下一页")::attr(href)').extract_first()
        imgurl_and_title = response.css('#ArticleId22 p img')
        imgurl = imgurl_and_title.css('img::attr(src)').extract_first()
        item['img_url'].append(imgurl)
        if next_img_url == '#':
            # print(next_img_url)
            # print(item)
            yield item
        else:
            # 拼接图片的url
            # print(next_img_url)
            if next_img_url is not None:
                url = response.url
                # print(url, next_img_url)
                url = url.split('/')
                # print(url)
                url[-1] = next_img_url
                next_img = '/'.join(url)
                # print(next_img)
                yield scrapy.Request(url=next_img, meta={'item': item}, callback=self.title_parse)
