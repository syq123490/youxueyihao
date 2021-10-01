import re
import os
import json

import requests

"""
获取详细教程、获取代码帮助、提出意见建议
关注微信公众号「裸睡的猪」与猪哥联系

@Author  :   猪哥,
@Version :   2.0"
"""

s = requests.Session()
# cookies序列化文件
COOKIES_FILE_PATH = 'taobao_login_cookies.txt'


class UsernameLogin:

    def __init__(self, loginId, umidToken, ua, password2):
        """
        账号登录对象
        :param loginId: 用户名
        :param umidToken: 新版登录新增参数
        :param ua: 淘宝的ua参数
        :param password2: 加密后的密码
        """
        # 检测是否需要验证码的URL
        self.user_check_url = 'https://login.taobao.com/newlogin/account/check.do?appName=taobao&fromSite=0'
        # 验证淘宝用户名密码URL
        self.verify_password_url = "https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0"
        # 访问st码URL
        self.vst_url = 'https://login.taobao.com/member/vst.htm?st={}'
        # 淘宝个人 主页
        self.my_taobao_url = 'http://i.taobao.com/my_taobao.htm'

        # 淘宝用户名
        self.loginId = loginId
        # 淘宝用户名
        self.umidToken = umidToken
        # 淘宝关键参数，包含用户浏览器等一些信息，很多地方会使用，从浏览器或抓包工具中复制，可重复使用
        self.ua = ua
        # 加密后的密码，从浏览器或抓包工具中复制，可重复使用
        self.password2 = password2

        # 请求超时时间
        self.timeout = 3

    def _user_check(self):
        """
        检测账号是否需要验证码
        :return:
        """
        data = {
            'loginId': self.loginId,
            'ua': self.ua,
        }
        try:
            response = s.post(self.user_check_url, data=data, timeout=self.timeout)
            response.raise_for_status()
            print(response.content)
        except Exception as e:
            print('检测是否需要验证码请求失败，原因：')
            raise e
        # check_resp_data = response.json()['content']['data']
        needcode = False
        # 判断是否需要滑块验证，一般短时间密码错误多次可能出现
        # if 'isCheckCodeShowed' in check_resp_data:
        #     needcode = True
        print('是否需要滑块验证：{}'.format(needcode))
        return needcode

    def _get_umidToken(self):
        """
        获取umidToken参数
        :return:
        """
        response = s.get('https://login.taobao.com/member/login.jhtml')
        st_match = re.search(r'"umidToken":"(.*?)"', response.text)
        print(st_match.group(1))
        return st_match.group(1)

    @property
    def _verify_password(self):
        """
        验证用户名密码，并获取st码申请URL
        :return: 验证成功返回st码申请地址
        """
        verify_password_headers = {
            'Origin': 'https://login.taobao.com',
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d9HjW9WC&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F',
        }
        # 验证用户名密码参数
        verify_password_data = {
            'ua': self.ua,
            'loginId': self.loginId,
            'password2': self.password2,
            'umidToken': self.umidToken,
            'appEntrance': 'taobao_pc',
            'isMobile': 'false',
            'returnUrl': 'https://www.taobao.com/',
            'navPlatform': 'MacIntel',
        }
        try:
            response = s.post(self.verify_password_url, headers=verify_password_headers, data=verify_password_data,
                              timeout=self.timeout)
            response.raise_for_status()
            # 从返回的页面中提取申请st码地址
        except Exception as e:
            print('验证用户名和密码请求失败，原因：')
            raise e
        # 提取申请st码url
        apply_st_url_match = response.json()['content']['data']['asyncUrls'][0]
        # 存在则返回
        if apply_st_url_match:
            print('验证用户名密码成功，st码申请地址：{}'.format(apply_st_url_match))
            return apply_st_url_match
        else:
            raise RuntimeError('用户名密码验证失败！response：{}'.format(response.text))

    def _apply_st(self):
        """
        申请st码
        :return: st码
        """
        apply_st_url = self._verify_password
        try:
            response = s.get(apply_st_url)
            response.raise_for_status()
        except Exception as e:
            print('申请st码请求失败，原因：')
            raise e
        st_match = re.search(r'"data":{"st":"(.*?)"}', response.text)
        if st_match:
            print('获取st码成功，st码：{}'.format(st_match.group(1)))
            return st_match.group(1)
        else:
            raise RuntimeError('获取st码失败！response：{}'.format(response.text))

    def login(self):
        """
        使用st码登录
        :return:
        """
        # 加载cookies文件
        if self._load_cookies():
            return True
        # 判断是否需要滑块验证
        self._user_check()
        st = self._apply_st()
        headers = {
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = s.get(self.vst_url.format(st), headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('st码登录请求，原因：')
            raise e
        # 登录成功，提取跳转淘宝用户主页url
        my_taobao_match = re.search(r'top.location.href = "(.*?)"', response.text)
        if my_taobao_match:
            print('登录淘宝成功，跳转链接：{}'.format(my_taobao_match.group(1)))
            self.my_taobao_url = my_taobao_match.group(1)
            self._serialization_cookies()
            return True
        else:
            raise RuntimeError('登录失败！response：{}'.format(response.text))

    def _load_cookies(self):
        # 1、判断cookies序列化文件是否存在
        if not os.path.exists(COOKIES_FILE_PATH):
            return False
        # 2、加载cookies
        s.cookies = self._deserialization_cookies()
        # 3、判断cookies是否过期
        try:
            self.get_taobao_nick_name()
        except Exception as e:
            os.remove(COOKIES_FILE_PATH)
            print('cookies过期，删除cookies文件！')
            return False
        print('加载淘宝cookies登录成功!!!')
        return True

    def _serialization_cookies(self):
        """
        序列化cookies
        :return:
        """
        cookies_dict = requests.utils.dict_from_cookiejar(s.cookies)
        with open(COOKIES_FILE_PATH, 'w+', encoding='utf-8') as file:
            json.dump(cookies_dict, file)
            print('保存cookies文件成功！')

    def _deserialization_cookies(self):
        """
        反序列化cookies
        :return:
        """
        with open(COOKIES_FILE_PATH, 'r+', encoding='utf-8') as file:
            cookies_dict = json.load(file)
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            return cookies

    def get_taobao_nick_name(self):
        """
        获取淘宝昵称
        :return: 淘宝昵称
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = s.get(self.my_taobao_url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('获取淘宝主页请求失败！原因：')
            raise e
        # 提取淘宝昵称
        nick_name_match = re.search(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', response.text)
        if nick_name_match:
            print('登录淘宝成功，你的用户名是：{}'.format(nick_name_match.group(1)))
            return nick_name_match.group(1)
        else:
            raise RuntimeError('获取淘宝昵称失败！response：{}'.format(response.text))


if __name__ == '__main__':
    # 说明：loginId、umidToken、ua、password2这4个参数都是从浏览器登录页面复制过来的。
    # 如何复制4个参数：
    # # 1、浏览器打开：https://login.taobao.com/member/login.jhtml
    # # 2、F12打开调试窗口，左边有个Preserve log，勾选上，这样页面跳转请求记录不会丢失
    # # 3、输入用户名密码登录，然后找到请求：newlogin/login.do 这个是登录请求
    # # 4、复制上面的4个参数到下面，基本就可以运行了
    # # 5、如果运行报错可以微信私聊猪哥，没加猪哥微信的可以关注猪哥微信公众号[裸睡的猪]，回复：加群

    # 淘宝用户名：手机 用户名 都可以
    loginId = '13871367581'
    # 改版后增加的参数，后面考虑解密这个参数
    umidToken = '398e868e344dcac7fa1999d8bc019a4a33088112',
    # 淘宝重要参数，从浏览器或抓包工具中复制，可重复使用
    ua = '140#9pOrZH/BzzZdrzo2Li/TAtSogFUBQKGfl+/MPvre4C0MjBGnqOVbPdMlAxpnusIPdj700ecrcvjQ/dAm0xfGSSNi095td44qlbzxgb2nuuv2zzrTiXkvU6OzzPzbVXlqlbrodGK+FzfczFFy2XMvl61zzPNj6/XLDzKv2P+GK3QdzF+f2XG0DFbDVPrIoFEtfzfDY8c4jtEqTbrIQOgozZwb5YLLMZ2aMXLQN4OVQnFtiGoql1QkFu2otNvldiCL2hZzHFXVVJanklePiZgoGXF2XCSonRI5BsVFlzE9A/lLublAo6UbTyPQvCeer1j7jF1mVXGFhkrgP64oHKJMhcUupkuoi5QcX6xBOpfEP2p2NMCA3Cf9hnFpPsDALRKyVwo1xGSbUEezHyNM8tE4sG+a6WmfmztzYxqto4wJRqOT7bMhJfuaMDPyZumpIDI5IQlcw1NYH8ai8y9xWctS2zdtTt44B1SUt6BAMgW3BfXppOp18RfKHkjj3WOdX5iB79jb1WrpMFdPDNUYurLk7bM7yTPCa5hg4Y66TCCnQUKCdcEPkY16r+wGitoXkyOC8Ynzs+QI+eyTGPhkNZwfpcPHEOaN06iov2ave8XIjDUnsgBwtgBrGSqmj+VNxq3hMPDUsZKg08mpr3z2MDLLk6qGEwCOS1a4I3WuZqDhevZRBBtzTngCJN3nLhgzXK90ijO5XcJqUufxKwYTbISFpy7b2lomDr6kuoU8wYoSwZOD/vF3kbBu13FnFTAqUS8ap57ThYsTZr9RKlAbYkUCYT0qkxfjAatdGFJ8mRdqPNAKBHAS7+eKK2e1gsaARN+75UiV/pWEE7pZYlR5Ax6fpr0sZLxgfxn7mlQEjv2IHgzUJFJPGj2RJjhgbsstDz8iMXTIQUxFkpM9DTRTjR4mBo9IQkcFYLxYvHGf3p00r+dBQuXAz9xDCjjLoRxClXLeALY57JWXUYuWANNhNbUfpXH5dUOP/n9CqO+YoiS42LwrWLZr6FcapNTYN7hXm18m51aL7TtioaaTJvfcNE/dRmndHnKnezdyKrqYrRFPC4pD42LFZGboMkKT4cgYLKFvPi0VC8WVvW4Gf1vP20YyGMum5kKlu3b2sG7xgpExwYwlPENL+543WCSTN5CXRqrOWt1R/Yi8LcubZ4X5BwUmUalHlQPvJVpD69LMPqjdCP2RZpNcoccj2/hnflaYUu/I1n6HQzCds/966kfczmpS4yE7d8C79uFTxxQ9seb3PHedcvj7dIfovmO4+pT1k+vAKLYrHbqaZVgycH1mvNNe2y9Ux4mP9pAEY8j7vGaI2IVJlLsnv/KuM/h4FqS0WE1lPuMGxxe/LPRr65MPemr2k7EToNqcHYOFqxakDHbQHBQ6dN+DxwnNd9B0DqGPcbwaVq3LxlpDaPN9eMFuwjnO8LQefYqY46RiwS+2qoe/mktIQ+5iavKhYNV1mB6Gc4Mx'
    # 加密后的密码，从浏览器或抓包工具中复制，可重复使用
    password2 = '20eb79237f48e81721946e75e2fee8c8795f27b3d22f48a9a15cec83404748545413f4c6b63baa26ede43ca222f3a7d679c4f50bf9c12e69099e52829774244384b397306648e76ffdb3ba3073fbb041aada4b3d39055d1ccf3295ab1fbddacd382ee283191e03a315379d4712a90f7c1ed1b03bf0b05186214f0278d4818030'

    ul = UsernameLogin(loginId, umidToken, ua, password2)
    ul.login()
    ul.get_taobao_nick_name()