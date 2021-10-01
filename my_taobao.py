# 暂停,淘宝可能存在较强的反爬机制,无法直接访问捕获的ajax接口.9.10猜想可能需要cookie之类的东西.等待进一步探索
# 确实需要cookie,构建session.不过淘宝的登录难度超出我想象,目前发现_csrf_token非常重要
# 9.16发现,现淘宝网页登录需手机验证
import requests
from lxml.html import etree


def R_quests():
    ID_check_url = 'https://login.taobao.com/newlogin/account/check.do?appName=taobao&fromSite=0&_bx-v=2.0.31'
    ID_check_dataform = {}
    header = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }
    se = requests.Session()
    Password_dataform = {
        'loginId':
        '13871367581',
        'password2':
        '391020978b26b5c11f8a4719db3b3c17c3eab40b55715a407d0c32004e7165342cd6adce1906e4bcfa7b20d9aac5f3c4a95c2e8c0c289d1c995bc804f0ebadf9457c600e7432b008bb07b69a93222b4996d16f0cac2b2f829679571801d86edd06306fe1fee5b49231fe112b2e136310e6993659329f8e17e5ffc46589180de5',
        'keepLogin':
        'false',
        'umidGetStatusVal':
        '255',
        'screenPixel':
        '1536x864',
        'navlanguage':
        'zh-CN',
        'navUserAgent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'navPlatform':
        'Win32',
        'appName':
        'taobao',
        'appEntrance':
        'taobao_pc',
        '_csrf_token':
        '7cLfUGI4nQB2WYh7GiWdmB',
        'umidToken':
        'a469a38d8fa5791e92507bdbc5f89618ab5b8dbf',
        'hsiz':
        '15647f3db9f9dea9ea22cc057146af39',
        'bizParams':
        '',
        'style':
        'default',
        'appkey':
        '00000000',
        'from':
        'tbTop',
        'isMobile':
        'false',
        'lang':
        'zh_CN',
        'returnUrl':
        'https://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&keyword=%E5%A5%B3%E8%A3%85&clk1=0881b2cc36ae20b1f66294d39e8be03f&upsId=0881b2cc36ae20b1f66294d39e8be03f',
        'fromSite':
        '0',
        'bx-ua':
        '215!y2BRGZ/vMNfrERRB1T30m2bwfDQKVmVBCf/c5V1m23erX6pGwdiXPM7HrXpvVmlXCyjor7 r20mmXMFEwGFC225rrJrAl3CBo EM6srM MHN9IKHYC/Ha5Y7NbhNYkVYlN9BrRM1gm2AX6Hbwd7C2jR/fbsllwDS4f2XrpdH2M9rX6rbwGFC22qerbrAzWUXuMpor8PQpuhYN6rowG7NGXewfXHAV3OjLyj6rq0xnv1fXtQ4CZ/exV5mB7BwrAa4LC9VHehz00G0EprWyZcZK7QpVX93rAk4rfmtOeBgamTcNBKqRctW5ChOCcTrDD/Sw5YBmTqh01ec6TfZTC7M7N3stoRyDQ7hTb LBsqX0Y1oyeKue77hFFmef6p69rObLyj6P2 00hG1RTrMXIcGGtf9Rb9ODgZtY5 H8RYj1msZ6yfgRJOq7VjNXb0H8kFEYphwrRKjaY9xRUsv6bOvK6KrNZBsDgZPE2rRrG xxHKlCGINyfuxFULSFfBAEVdDz079AVSzkeRM9P gVg1ja4CmLDC3b8EMkmQwYDdX3A784hh3tnaC1p9N4R0hbRom ahqKxVhPdZiGyfH/2iGVYRlM81Blxiy7voyRBuy9ap1ad8NEM4abYf7hg6L0wOkue0beRUsnVLFKfM87mcgtuXse5CgbrWFLwUFgP6PlsNJj9tHgxfO3AbnnhTz5TBcCIzr6iILJYNSvv9lvDM3S4ZpsNNEivDHbSPi PzL ZBbwAVuvTtGE hNlkvCqVEY6qFp0BD6bw3e3xs/9Kthd6wDQbkChr3Ff3vF8Nb9RN2vOmrn3lE8Qk68Fq8zzWgZ0RBICdKi77P bpV6nuQIK PZ36a/zcNpYN4Pvv1b/v/4APk9wrO7J2iTlDfwAcOgLnrUKVTx2FiOn6VAujevKHfW227cdX4WkoNIh87UnHR4/LVZcsf1I2YtbCgC48hJaInBgJdx0cmxHlFKmyP9mqb F4j5XnDYdubpXui66 VrcEB6LSrZxlDTShPYBqeYxd9MAI/oEZdSls/mEqFrFkyQoxzDvLA5ZvxyUszE7N/RhpMXSVYklMs91 ORDfb6BN1KaEX2YsvZkZm0S9hMDVSYVeePE/G4r/2B2bvpgJnEWu4p4/8YDRrzaIA6Vp4Jme/oUhZYL7s9LlRAH 3pkQWBrDTkLu 810NuyCzDQ8dklmR8HdpsW26PX8pbaROUY40o2rcTH39/9d9udPwp0FBNqauFhzMC bjGlwzAYH1AH 7z1COtPtdROAg9g68oeH2T9LP2HB/gpccata1taSYnKdVWaZN3AyEQbC2ORQakzoLNRgJ93uiiRHHWVtHLqqeBzZie8hhZS7ygkqmq3B3TBXsQmccyRyRTk0p/YIN2BRygkoYj3RRTRX gy/RKRyRRkgDEYDKSBRNqRqZzEQtRLOVPqGM8DGkDFFD8e5T mTyR3N2z7G2J4ZmAhCDY/KuL7KsATOv81aUsyRe2rYX03a/HIDk5op39PSUMOz3Lwu8/suQ6X0iQL3BuTSjx7Hwu0AGDEU1gSOcE7Dvsi/aO7uBwEHhcZ5 Jb9Pu7ExlXStbrskzFbwLhRjjHRrab6Fc8M6FNTJvvO9bpCTJucxngyouXPLheUOdpYiEc8UfKVWfWgQnGuJDyatGIFETeT9wsZWJ/zRIblRGMY 01 D7QLA2okK5MXkALbeLRTA/VoW9BqGJBitH9Rm9/CbF1BCqdRRQAiaw5e4keA1 qDOyRWioJLSe1QkMj4jxvrdg71D96vgfCDxXDLRMUY35RVOhSd7RFqevFzzgLmj9FiYdRruP8MQ 25cpeSMHwKIwkqtHH5ObOCAOSA4XBFT4qhcw8ZOeHUSGXBKWFV2SdBmF0A4nNTRMHcjh2ac Z8Mco8SDN7uoNsHduVR5FFYZCP9G RA9vI2CAtCzCmrvfBmEs/CdMuNHhGCam/S/q8wy/pG/zNK6sE/bRbxnJNzRJ941uijNT6zg7 4c0zH 04kNLTfOTMckrOsRPFfmk7XBGptZV7vVDcckqueAqj3jzjQyANMxl8KYRzbG5jknI/sv85IeroAsooF68wB=',
        'bx-umidtoken':
        'T2gAy40IPkViij1hB20E6ZDebvdAWK3CcwXnIX7o5tv4uEods5PnAIFCpm37UCS39ds=',
    }
    response = se.post(url=ID_check_url,
                       headers=header,
                       data=ID_check_dataform)
    print(response.content)
    # print(response.content)
    return 0


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
    # url = 'http://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0&_bx-v=2.0.31 '
    R_quests()
    # response是一个网页文档
    # O_pendocument(response)
    # print(response)


if __name__ == '__main__':
    main()
