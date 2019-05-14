# -*- coding: utf-8 -*-
import scrapy
import re
from meizi.items import MzItem
import pymongo


class MzSpider(scrapy.Spider):
    name = 'mz'
    allowed_domains = ['www.2717.com']
    start_urls = ['https://www.2717.com/ent/meinvtupian/']
    index_url = 'https://www.2717.com'
    # 设置更新页数
    updata_page = 5

    def parse(self, response):
        client = pymongo.MongoClient('localhost', 27017)
        # 库名
        db = client['MZIMG']
        # 表名
        # 下载图片去重表名
        title_Duplicates = db.MZ
        title_urls = response.css(
            'div.MeinvTuPianBox > ul > li > a[class*=tit]').extract()
        if title_urls:
            for title_url in title_urls:
                item = MzItem()
                pattern = re.compile(
                    r'<a.*?href="(.*?)".*?title="(.*?)".*?a>', re.S)
                title_url = re.match(pattern, title_url)
                url = self.index_url + title_url.group(1)
                # print(url,title_url.group(2))
                title = title_url.group(2).strip()
                item['title'] = title
                item['title_url'] = url
                item['img_url'] = []
                try:

                    if title_Duplicates.find_one({'title_url': url}) is None:
                        yield scrapy.Request(url=url, meta={'item': item}, callback=self.get_picture_urls)

                except:
                    print('{}已存在'.format(title))

        next_page_url = response.css(
            'div.NewPages > ul > li > a:contains("下一页")::attr(href)').extract_first()
        if next_page_url and self.updata_page >=0:
            self.updata_page -= 1
            url = response.url.split('/')
            url[-1] = next_page_url
            # time.sleep(1)
            # print(nextpage)
            yield scrapy.Request(url='/'.join(url), callback=self.parse)
        '''else:
            return self.get_picture_urls(response)'''

    # 获取图片链接
    def get_picture_urls(self, response):
        # item = TitleItem()
        item = response.meta['item']
        # print(response.url)
        url = response.url
        image_url = response.css(
            '#picBody > p > a:nth-child(1) > img::attr(src)').extract_first()  # 提取图片链接
        if image_url:
            item['img_url'].append(image_url)
        pattern = re.compile(r'(\d+_.*?html)|(\d+.html)')
        next_image = response.css('#nl a::attr(href)').extract_first()  # 下一张图片
        try:
            next_image_url = re.sub(pattern, next_image, url)  # 拼接图片链接
        except:
            pass
        if next_image == '##':
            yield item
            print(item, '<<<<<<<<<<<<<<<')
        else:
            yield scrapy.Request(url=next_image_url, meta={'item': item}, callback=self.get_picture_urls)
