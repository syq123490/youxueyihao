import requests
import my_headers
from lxml.html import etree
from cyberbrain import trace


def R_quests(url):
    '''

    传入网址，向网站发送请求并传回响应的文档

    '''
    r = requests.get(url=url, headers=my_headers.headers)
    r.encoding = 'utf-8'
    print('{}\n'.format(r.status_code))
    return r.text


def O_pendocument(docname, content):
    '''

    写入文件中

    '''
    file = open(docname, 'w', encoding='utf-8')
    file.write(content)
    file.close()
    print("已成功创建")
    return 0


def P_arse(content, xpath):
    """

    传入网页文档和解析规则，用lxml解析

    """
    tree = etree.HTML(content)
    rets = tree.xpath(xpath)
    string = rets[0].xpath("string(.)").replace('\n', '').replace('\t', '').replace('\r', '')
    return string


def main():
    url = input("请输入请求网址：")
    content = R_quests(url)
    # content是一个网页文档
    xpath = '//div[@class="xj_contextinfo"]/h6'
    answer = P_arse(content, xpath)
    print(answer)
    return 0


if __name__ == '__main__':
    main()
