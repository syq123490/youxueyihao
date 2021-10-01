import requests
from bs4 import BeautifulSoup
import re
import time


# keyword = input("请输入关键字：")

for i in range(5):
    url = 'https://www.baidu.com/s'
    ua = UserAgent()
    data = {'wd': '{python}', 'pn': 'i*10'}
    headers = {'User-Agent': '{}'.format(ua.random())}
    # proxies = {'https':'http://124.94.252.146:9999'}
    pattern1 = re.compile('http://www\.baidu\.com/baidu\.php')
    pattern2 = re.compile('<div class="c-abstract">(.*?)</div>', re.S)
    # emptylist = []
    # number = 0
    response = requests.get(url=url, headers=headers, params=data)
    # describe = re.findall(pattern2,response.text)
    # for i in describe:
    #     if '<span class=' in i:
    #         first=re.sub('<span class=" newTimeFactor_before_abs c-color-gray2 m">','',i)
    #         second = re.sub('&nbsp;</span>', '', first)
    #         thrid = re.sub('<em>.*?</em>','python',second)
    #         # forth = re.sub('')
    #         emptylist.append(thrid)
    #     else:
    #         pass
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.select('h3 a')
    # print(soup.prettify())
    for title in title:
        if re.findall(pattern1, title['href']) != []:
            pass
        else:
            print(title.text)
            # print(emptylist[number])
            print(title['href'])
            print("\n")
    print(i)
    time.sleep(2)
