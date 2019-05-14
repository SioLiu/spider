# -*-coding: utf-8 -*-
import pymongo


MONGO_URL = 'localhost' #数据库地址
MONGO_DB = 'MZIMG' #数据库名称
MONGO_TABLE = 'Duplicates' #表名称

client = pymongo.MongoClient('localhost', 27017)
db = client['MZIMG']
table = db['MZ']
collection = db.TitleItem


def save_to_mongo():
    data = list(table.find())
    for da in data:
        # print(type(da))
        if db[MONGO_TABLE].insert({'title_url':da['title_url']}):
            print('存储到mongodb成功',da['title_url'])
    print('#'*40)

save_to_mongo()