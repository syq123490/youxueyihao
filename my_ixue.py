import requests
import my_headers
from lxml.html import etree
import time


def R_quests(url):
    '''

    传入网址，向网站发送请求并传回响应的文档

    '''
    r = requests.get(url=url, headers=my_headers.headers)
    r.encoding = 'utf-8'
    print(r.status_code)
    return r.text


def O_pendocument(name, content):
    # name = input("请输入保存的文件名:")
    file = open(name, 'a', encoding='utf-8')
    file.write(content)
    file.close()
    # print("已成功创建热卖网站")
    return 0


def P_arse(docname, dict, response):
    """

    传入网页文档和解析规则，用lxml解析并写入文件

    """
    tree = etree.HTML(response)
    rets = tree.xpath('//article[@class="excerpt"]')
    for ret in rets:
        title = ret.xpath(".//h2/a/@title")[0].replace('- i学–爱学习，爱成长，爱生命，爱自由',
                                                       '')
        theurl = ret.xpath(".//h2/a/@href")[0]
        # 这里从当前节点开始非常重要，xpath如果用title的绝对路径将会选择所有的title而非ret的
        O_pendocument(docname, title + '\n')
        O_pendocument(docname, theurl + '\n' * 3)

    return 0


def main():
    start = time.perf_counter()
    start_page = 1
    end_page = 20
    classdict = {}
    docname = 'ixuexi2.txt'
    for page in range(start_page, end_page + 1):
        url = "https://ixue.me/page/%d" % page
        # print(url)
        response = R_quests(url)
        # response是一个网页文档
        P_arse(docname, classdict, response)
        time.sleep(1)
    print("Finish")
    end = time.perf_counter()
    print(end - start, 's')


if __name__ == '__main__':
    main()