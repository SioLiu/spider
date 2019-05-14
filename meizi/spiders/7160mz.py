# -*- coding: utf-8 -*-
import scrapy
from meizi.items import A7160Item
import pymongo


class A7160mzSpider(scrapy.Spider):
    name = '7160mz'
    allowed_domains = ['www.7160.com']
    start_urls = ['https://www.7160.com/xiaohua/', 'https://www.7160.com/qingchunmeinv/']

    def parse(self, response):
        client = pymongo.MongoClient('localhost', 27017)
        # 库名
        db = client['MZIMG']
        # 表名
        # 下载图片去重表名
        title_filter = db.A7160
        request_url = response.url.split('/')
        index_url = 'https://www.7160.com'
        title_bom = response.css('div.news_bom div.news_bom-left ul.new-img ul li')
        next_page = response.css('div.page a:contains("下一页")::attr(href)').extract_first()
        for title_data in title_bom:
            title_url = title_data.css('a::attr(href)').extract_first()
            title = title_data.css('a::attr(title)').extract_first()
            title_url = ''.join([index_url, title_url])
            if title_filter.find_one({'title_url':title_url}) is None:
                item = A7160Item()
                item['title_url'] = title_url
                item['title'] = title
                item['img_url'] = []
                # print(title, title_url)
                yield scrapy.Request(url=title_url, meta={'item':item}, callback=self.title_parse)
            else:
                print(title, title_url, '已经存在')
        if next_page is not None:
            request_url[-1] = next_page
            next_page_url = '/'.join(request_url)
            # print('下一页   *******', next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        


    def title_parse(self, response):
        item = response.meta['item']
        # print(item)
        # print(response.url)
        # 获取单一标题的图片数量
        count_img = response.css('div.itempage a:contains("共")::text').extract_first()[1:-3]
        one_title_imgs = response.css('div.itempage a::attr(href)').extract()
        img_url = response.css('div.picsbox p a img::attr(src)').extract_first()
        # print(img_url)
        item['img_url'].append(img_url)
        # print(count_img)
        url_list = response.url.split('/')
        # print(url_list)
        for one_img in one_title_imgs[2:-1]:
            if 'html' in one_img:
                url_list[-1] = one_img
                next_img_url = '/'.join(url_list)
                yield scrapy.Request(url=next_img_url, meta={'item':item}, callback=self.title_parse)
        # print(len(item['img_url']))
        # print(int(count_img))
        if len(item['img_url']) >= int(count_img):
            yield item
        