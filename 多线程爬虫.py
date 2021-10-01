# 两类线程:下载(3)/解析(3)
# 内容队列:下载线程往队列中put数据,解析线程往队列中get数据
# URL队列:下载线程从URL队列中get数据并且拼接成URL
from queue import Queue
import threading
import requests
from lxml import etree
import time


class CrawlThreading(threading.Thread):
    def __init__(self, urlqueue, dataqueue):
        super().__init__()
        self.urlqueue = urlqueue
        self.dataqueue = dataqueue

    def run(self):
        '''
        将URL队列里的数取出来拼出完整URL,逐一请求后将响应数据放入data队列中
        '''
        while 1:
            if self.urlqueue.empty():
                print('采集线程结束')
                break
            else:
                number = self.urlqueue.get()
                url = "https://ixue.me/page/%d" % number
                header = {
                    'User-Agent':
                    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
                }
                response = requests.get(url=url, headers=header)
                self.dataqueue.put(response)
                print('第%s面已采集' % number)
                time.sleep(1)


class CreateParseThreading(threading.Thread):
    def __init__(self, dataqueue, fp, lock, urlqueue):
        super().__init__()
        self.dataqueue = dataqueue
        self.fp = fp
        self.lock = lock
        self.urlqueue = urlqueue

    def run(self):
        while 1:
            if self.urlqueue.empty() and self.dataqueue.empty():
                print("解析线程结束")
                break
            else:
                content = self.dataqueue.get(True, 10)
                # print(content.text)
                # exit()
                self.parse(content.text)
                print('第页已解析')

    def parse(self, content):
        tree = etree.HTML(content)
        rets = tree.xpath('//article[@class="excerpt"]')
        for ret in rets:
            title = ret.xpath(".//h2/a/@title")[0].replace(
                '- i学–爱学习，爱成长，爱生命，爱自由', '')
            theurl = ret.xpath(".//h2/a/@href")[0]
            self.lock.acquire()
            self.fp.write(title + '\n')
            self.fp.write(theurl + '\n' * 3)
            self.lock.release()


def CreateUrlQueue():
    # 创造URL队列
    q = Queue(50)
    for item in range(1, 21):
        q.put(item)
    return q


def CreateDataQueue():
    # 创造data队列
    q = Queue(50)
    return q


def main():
    start = time.perf_counter()
    urlqueue = CreateUrlQueue()
    # 创建URL队列
    dataqueue = CreateDataQueue()
    # 创造data队列存放爬下来的数据
    fp = open(file='aikecheng.txt', mode='a', encoding='utf8')
    # 打开文件
    lock = threading.Lock()
    # 创建锁,必须放在主线程.子线程之间不共享局部变量
    crawl1 = CrawlThreading(urlqueue=urlqueue, dataqueue=dataqueue)
    crawl2 = CrawlThreading(urlqueue=urlqueue, dataqueue=dataqueue)
    crawl3 = CrawlThreading(urlqueue=urlqueue, dataqueue=dataqueue)
    crawl1.start()
    crawl2.start()
    crawl3.start()
    parse1 = CreateParseThreading(dataqueue=dataqueue,
                                  lock=lock,
                                  fp=fp,
                                  urlqueue=urlqueue)
    parse2 = CreateParseThreading(dataqueue=dataqueue,
                                  lock=lock,
                                  fp=fp,
                                  urlqueue=urlqueue)
    parse3 = CreateParseThreading(dataqueue=dataqueue,
                                  lock=lock,
                                  fp=fp,
                                  urlqueue=urlqueue)

    parse1.start()
    parse2.start()
    parse3.start()
    crawl1.join()
    crawl2.join()
    crawl3.join()
    parse1.join()
    parse2.join()
    parse3.join()
    fp.close()
    print('主线程结束,爬取完成')
    end = time.perf_counter()
    print(end - start, 's')


if __name__ == '__main__':
    main()
