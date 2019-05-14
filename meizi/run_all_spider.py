from scrapy.cmdline import execute
import threading
spiders = ['mz', 'win4000', 'umei', '7160mz']
tasks = []
for spider in spiders:
    tasks.append(threading.Thread(target=(execute('scrapy crawl {}'.format(spider).split()))))
for task in tasks:
    task.start()
for task in tasks:
    task.join()