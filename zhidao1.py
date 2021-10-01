# //b[@class='pl5  hour']       每节课的序号
# //b[contains(text(), "1.1")]/../following-sibling::div[1]/span        利用序号锁定节
# //b[contains(text(), "1.1")]/../following-sibling::div[1]/div//b[@class='fl time_icofinish']      利用序号判断是否完结
# document.getElementsByClassName("example color")
# //div[@class='video-topic']/ul/li     疑似弹窗题
# //div[@class='speedList']         播放速度
# 3.25:寻找并测试lxml使用方法，使用html.etree代替etree。使用lxml解析获得课程列表
# 循环对每节课进行完结播放判断
# 3.26:判断后对完结播放的视频，跳转至下一集
# 封装关闭弹窗代码，优化代码
# 使用JavaScript定位播放速度并点击至1.5倍速
# 使用JavaScript修改rate元素将播放速度提至12.5倍速
from selenium import webdriver
import time
from lxml.html import etree
from selenium.common.exceptions import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def close():
    '''
    close函数用于关闭弹题测试，智慧树警告，温馨提示，习惯分
    '''
    try:
        tanchuang = wd.find_element_by_xpath(
            "//div[@class='el-dialog__wrapper dialog-test']")
        answer = wd.find_element_by_xpath("//li[@class='topic-item']")
        answer.click()
        tanchuangc = wd.find_element_by_xpath(
            "//div[@aria-label='弹题测验']//button/i")
        tanchuangc.click()
        time.sleep(2)
        js = 'document.getElementById("playButton").click()'
        wd.execute_script(js)
        print("已关闭弹窗，继续播放")
    except BaseException:
        pass
    # 关闭弹窗
    try:
        warning = wd.find_element_by_xpath(
            "//div[@aria-label='智慧树警告']//span/button")
        warning.click()
        print("已关闭智慧树警告")
    except BaseException:
        pass
    # 关闭智慧树警告
    try:
        bidu = wd.find_element_by_xpath("//div[@class='dialog-read']//i")
        bidu.click()
    except BaseException:
        pass
    # 关闭必读
    try:
        tip = wd.find_element_by_xpath(
            "//div[@class='el-dialog__wrapper dialog-look-habit']//button")
        tip.click()
    except BaseException:
        pass
    # 关闭温馨提示
    try:
        xiguanfen = wd.find_element_by_xpath(
            "//div[@class='el-dialog__wrapper dialog-look-habit']/div/div/button")
        xiguanfen.click()
    except BaseException:
        pass
    # 关闭习惯分


name_ = input("请输入账号：")
key_ = str(input("请输入密码："))
number = 0
wd = webdriver.Chrome()
wd.implicitly_wait(10)
wd.get("https://www.zhihuishu.com/")
# 隐式等待10秒

not_login = wd.find_element_by_xpath("//li[@id='notLogin']/a")
not_login.click()
# 点击登录
xuehao = wd.find_element_by_xpath("//a[@id='qStudentID']")
xuehao.click()
# 点击学号登录

school = wd.find_element_by_xpath("//div/input[@placeholder='输入你的学校']")
school.send_keys("太原理工大学")
schoolchoose = wd.find_element_by_xpath("//div[@class='content']/ul/li/b")
schoolchoose.click()

xuehao = wd.find_element_by_xpath("//li/input[@placeholder='大学学号']")
xuehao.send_keys(name_)

keys = wd.find_element_by_xpath("//li/input[@placeholder='密码']")
keys.send_keys(key_)
# 输入账号密码
time.sleep(2)
# rlogin = wd.find_element_by_xpath("//span[@class='wall-sub-btn']")
# rlogin.click()
# class1 = wd.find_element_by_xpath(
#     "//div[@class='hoverList interestingHoverList']//div[@class='item-left-course']/div")
# class1.click()
# time.sleep(5)
# source = wd.page_source
# print(source)
# tree = etree.HTML(source)
# class_list = tree.xpath("//b[@class='pl5  hour']//text()")
# # print(class_list)
# nclass_list = [
#     "1.2",
#     "2.1",
#     "2.3",
#     "2.4",
#     "2.5",
#     "2.6",
#     "3.1",
#     "3.2",
#     "3.3",
#     "4.1",
#     "4.3",
#     "4.4",
#     "4.5",
#     "5.1",
#     "5.4",
#     "6.2",
#     "6.3",
#     "6.4",
#     "6.5",
#     "6.6",
#     "6.7",
#     "7.2",
#     "7.3",
#     "7.4",
#     "7.5",
#     "8.1",
#     "8.2",
#     "8.4",
#     "8.5"]
# # 用以排除无视频的课题号
# rclass_list = []
# for i in class_list:
#     if i in nclass_list:
#         pass
#     else:
#         rclass_list.append(i)
#
# print(rclass_list)
# # NoSuchElementException
# for i in rclass_list:
#     try:
#         finish = wd.find_element_by_xpath(
#             "//b[text()='%s']/../following-sibling::div[1]//b[@class='fl time_icofinish']" %
#             i)
#         print("%s已完成" % i)
#         continue
#     except BaseException:
#         for j in range(2):
#             close()
#         time.sleep(1)
#         js = 'document.evaluate("//b[text()=\'%s\']/../following-sibling::div[1]", document).iterateNext().click()' % i
#         print("js={}".format(js))
#         wd.execute_script(js)
#         print("已执行js")
#         # start = wd.find_element_by_xpath("//b[text()='%s']/../following-sibling::div[1]" % i)
#         # start.click()
#         time.sleep(2)
#         js1 = 'document.getElementsByClassName("speedTab speedTab10")[0].setAttribute("rate","12.5")'
#         wd.execute_script(js1)
#         print("已执行js1")
#         time.sleep(3)
#         js2 = 'document.getElementsByClassName("speedTab speedTab10")[0].click()'
#         wd.execute_script(js2)
#         print("已执行javascript")
#         while True:
#             try:
#                 time.sleep(1)
#                 wd.find_element_by_xpath(
#                     "//b[text()='%s']/../following-sibling::div[1]//b[@class='fl time_icofinish']" %
#                     i)
#                 print("进度已达100！")
#                 break
#             except BaseException:
#                 close()
#     print("i=%s" % i)
#     number += 1
#     print("已播放{}集".format(number))
