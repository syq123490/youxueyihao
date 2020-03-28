import requests
import json

if __name__ == '__main__':
    url=r'https://wenku.baidu.com/browse/getbcsurl?doc_id=378f7303f01dc281e53af0ac&pn=1&rn=99999&type=ppt&callback=jQuery110108441270703745489_1585356567452&_=1585356567453'
    #需先找到json数据的真实url
    header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    response=requests.get(url=url,headers=header)
    req=response.text
    # print(req)
    req1=req.strip('()jQuery110108441270703745489_1585356567452')        #去掉小括号
    # print(req1)
    result1=json.loads(req1)
    # print(result)
    result2=result1['list']
    # print(result2)
    for i in result2:
        final=i['zoom']
        # print(final)
        final1=requests.get(url=final,headers=header)
        pickture=final1.content
        number=final.rsplit('=',1)[1]   #将图片名切片
        with open(r'C:\Users\User\Desktop\百度文库\{}.jpg'.format(number),'ab+') as fp:
            fp.write(pickture)
            print('爬取成功')
