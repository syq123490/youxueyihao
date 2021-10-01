import requests
import my_headers
from lxml.html import etree


def R_quests(url):
    '''

    传入网址，向网站发送请求并传回响应的文档

    '''
    r = requests.get(url=url, headers=my_headers.headers)
    r.encoding = 'gbk'
    print(my_headers.headers["User-Agent"] + "\n")
    print(r.status_code)
    return r.text


def O_pendocument(content):
    docname = input("请输入保存的文件名:")
    file = open(docname, 'w', encoding='utf-8')
    file.write(content)
    file.close()
    print("已成功创建")
    return 0


def P_arse(response):
    """

    传入网页文档和解析规则，用lxml解析

    """
    tree = etree.HTML(response)
    pass


def main():
    url = input("请输入请求网址：")
    response = R_quests(url)
    # response是一个网页文档
    O_pendocument(response)
    print("Finish")


if __name__ == '__main__':
    main()
