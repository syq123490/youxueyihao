# //li[@class='clearfix video current_play']        当前播放视频
# //div/b[@class='fl time_icofinish']           已完成观看的视频独有的class属性
#


from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

wd = webdriver.Chrome()
wd.implicitly_wait(10)
wd.get("https://www.zhihuishu.com/")
# 隐式等待10秒

notlogin = wd.find_element_by_xpath("//li[@id='notLogin']/a")
notlogin.click()
# 点击登录
xuehao = wd.find_element_by_xpath("//a[@id='qStudentID']")
xuehao.click()
# 点击学号登录

school = wd.find_element_by_xpath("//div/input[@placeholder='输入你的学校']")
school.send_keys("太原理工大学")
schoolchoose = wd.find_element_by_xpath("//div[@class='content']/ul/li/b")
schoolchoose.click()

xuehao = wd.find_element_by_xpath("//li/input[@placeholder='大学学号']")
xuehao.send_keys("2020003808")

keys = wd.find_element_by_xpath("//li/input[@placeholder='密码']")
keys.send_keys("54YXZruomi")
# 输入账号密码
time.sleep(2)
rlogin = wd.find_element_by_xpath("//span[@class='wall-sub-btn']")
rlogin.click()
# 点击登录

while True:
    try:
        class1 = wd.find_element_by_xpath(
            "//div[@class='hoverList interestingHoverList']//div[@class='item-left-course']/div")
        class1.click()
        break
    except BaseException:
        pass

# 选择第一门课

while True:
    while True:
        try:
            wd.find_element_by_xpath(
                "//li[@class='clearfix video current_play']//div/b[@class='fl time_icofinish']")
            # print("进度已达100！")
            break
        except BaseException:
            pass
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
        except BaseException:
            pass
        try:
            warning = wd.find_element_by_xpath(
                "//div[@aria-label='智慧树警告']//span/button")
            warning.click()
        except BaseException:
            pass
        try:
            bidu = wd.find_element_by_xpath("//div[@class='dialog-read']//i")
            bidu.click()
        except BaseException:
            pass
        try:
            tip = wd.find_element_by_xpath(
                "//div[@class='video-study']//div[@class='el-dialog__wrapper dialog-back']//div[@class='el-dialog__header']//button/i")
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

    WebDriverWait(
        wd, 20, 0.5).until(
        EC.presence_of_element_located(
            (By.ID, "nextBtn")))
    js2 = 'document.getElementById("nextBtn").click()'
    wd.execute_script(js2)
    # 判定进度是否已达100

    # print("已结束一集")
