# coding:utf-8

import requests
import pymongo
import os
import aiohttp
import asyncio
import random
import time
import re
import sys
import signal

# class Downloadimg():
path = r'e:\\图片\\'
# 连接数据库
client = pymongo.MongoClient('localhost', 27017)
# 库名
db = client['MZIMG']
# 表名
# 下载队列表名  用列表形式添加表
collections = [db.MZ, db.Umei, db.A7160, db.Win4000]
# collections = [db.Win4000]

# 下载图片去重表名
img_filter = db.Imgfilter

# 最大连接数
max_connection = 5
# 下载关键词
# keyword = "短裤*酥胸|俏皮*甜美|清纯*可爱|高颜值美女|白色短裤"
keyword = "白皙|嫩白"

count_download_img = 0
title_count = 0
done = False
listdir = []



# 读取文件
def get_url():
    global title_count
    all_data = []
    # 读取数据
    for collection in collections:
        data = collection.find({'title': {"$regex": keyword}})  # 用正则查找
        title_count += data.count()
        all_data.append(data)
        # print(data.count())
    for one_collection_data in all_data:
        for data in one_collection_data:
            # title = da['title']
            # title_url = da['title_url']
            # img_urls = da['img_url']

            yield data
            # time.sleep(4)
            # return get_url()


def get_headers():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Android 2.3.4; Linux; Opera mobi/adr-1107051709; U; zh-cn) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
    ]
    UserAgent = random.choice(user_agent_list)
    return UserAgent


def get_proxy():
    proxy = requests.get('http://127.0.0.1:5010/get').text
    proxies = 'http://{}'.format(proxy)

    return proxies


async def download_img(title, img_url, num, semaphore, session):
    headers = {
        'User-Agent': get_headers(),
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    async with semaphore:
        # 特定条件丢掉所有后续任务
        if done:
            pass
        else:
            try:
                global listdir
                # 格式输出
                # 输出的标题长度
                output_title_len = 15
                len_title = len(title)
                space_count = len(re.findall(r'[a-zA-Z\[\]*\(\)\.?<>\-\+\=/0-9 ]', title[:output_title_len - 2]))
                if len_title > output_title_len:
                    out_put_title = '{}... {}'.format(title[:output_title_len - 2], ' ' * space_count)
                elif len_title <= output_title_len:
                    add_space_count = (output_title_len-len_title) * 2 + space_count
                    out_put_title = '{}{}'.format(title, ' ' * add_space_count)
                if num < 10:
                    num = '{} '.format(num)
                print('正在下载>>>>>  {}  第{}张图片  {}'.format(out_put_title, num, img_url))

                async with session.get(img_url, headers=headers) as response:
                    img_content = await response.read()
                    title = re.sub(r'[:><?*\\/|]', '', title)
                    path_title = path + title
                    if title not in listdir:
                        os.makedirs(path_title)
                        listdir.append(title)
                    with open(path_title + '\\{}.{}'.format(num, img_url.split('.')[-1]), 'wb') as f:
                        f.write(img_content)
                        f.close()
                    # 将下载成功的img_url写入数据库
                    img_filter.update({'img_url': img_url},
                                    {'$set': {'img_url': img_url}}, True)
                    global count_download_img
                    count_download_img += 1

            except Exception as e:
                print('downloading_error:{}'.format(e))
                # return await download_img(title, img_url, num)

# 判断图片是否已经下载 已经下载返回Ture  否则返回False
def pd_imgurl(img_url=None):
    if img_url:
        try:
            dup_data = img_filter.find_one({'img_url': img_url})
            if dup_data is None:
                return False
            else:
                return True
        except:
            pass


async def main():
    global count_download_img
    global title_count
    tasks = []
    total_data = get_url()
    semaphore = asyncio.Semaphore(max_connection)  # 限制并发量
    async with aiohttp.ClientSession() as session:
        for data in total_data:
            title = data['title'].strip()
            title_url = data['title_url']
            img_urls = data['img_url']
            # t = 0
            for num, img_url in enumerate(img_urls):
                if img_url is None:
                    continue
                if 't1.27270.com' in img_url:
                    continue
                if 'jpg' not in img_url:
                    continue

                # 判断图片是否下载过
                if pd_imgurl(img_url=img_url):
                    continue

                tasks.append(download_img(title, img_url,
                                          num+1, semaphore, session))  # 总任务
            # 待下载套图数-1
            title_count -= 1
            if tasks:
                img_count = len(tasks)
                print('{} {}\n总共 {} 张图片待下载\n'.format(title, title_url, img_count))
                try:
                    await asyncio.wait(tasks)
                except Exception as e:
                    print('error:', e)
                else:
                    if not done:
                        print('\n{} 下载完成  还剩{}套图片待下载\n'.format(title, title_count))
                finally:
                    tasks.clear()
            else:
                print('{} 已下载  还剩{}套图片待下载'.format(title, title_count))
            if done:
                print('\nctrl + c  本次下载 {} 张图片'.format(
                    count_download_img))
                break

def Done(signal, frame):
    global done
    done = True

def get_dir_name():
    global listdir
    listdir = os.listdir(path)

if __name__ == '__main__':
    signal.signal(signal.SIGINT,Done)
    try:
        get_dir_name()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
    except KeyboardInterrupt:
        print('\nctrl + c  本次下载 {} 张图片'.format(
                    count_download_img))
    except Exception as e:
        print(e)
    else:
        if not done:
            print('所有图片下载完成，共下载{}张图片'.format(count_download_img))
