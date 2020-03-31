from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys     #将点击按钮转化为回车
from selenium.webdriver.support.ui import WebDriverWait     #实现显示等待
a = input("请输入搜索内容：")

options = Options()
#禁止图片和css加载     设置下载地址
# help(options)
prefs = {"profile.managed_default_content_settings.images": 2,'permissions.default.stylesheet':2,"download.default_directory":r"C:\Users\User\Desktop\selenium下载地址"}
options.add_experimental_option("prefs", prefs)
 
wd = webdriver.Chrome(options=options)
# wd = webdriver.Chrome()

# wd.implicitly_wait(10)       #隐式等待

wd.get(r'http://www.zxxk.com/')

element1=wd.find_element_by_css_selector('.login-btn')     #找到‘登陆’元素
WebDriverWait(wd,10,0.2).until(lambda x:x.find_element_by_css_selector(".login-btn"))
element1.click()

element2=wd.find_element_by_class_name('lcon-weixin')       #找到‘账号密码’登陆
WebDriverWait(wd,10,0.2).until(lambda x:x.find_element_by_css_selector(".lcon-weixin"))
element2.click()

element3=wd.find_element_by_id('username')      #找到“账号”
WebDriverWait(wd,10,0.2).until(lambda x:x.find_element_by_css_selector("#username"))
element3.send_keys('13871367581')


element4=wd.find_element_by_css_selector("[name='password']")       #找到‘密码’
WebDriverWait(wd,10,0.2).until(lambda x:x.find_element_by_css_selector("[name='password']"))
element4.send_keys('525mmtzy')

element5=wd.find_element_by_css_selector("[value='登录']")
WebDriverWait(wd,10,0.2).until(lambda x:x.find_element_by_css_selector("[value='登录']"))
element5.click()

element6=wd.find_element_by_class_name('search-key')        #传入带搜内容
WebDriverWait(wd,10,0.2).until(lambda x:x.find_element_by_css_selector(".search-key"))
element6.send_keys('{}\n'.format(a))

for window in wd.window_handles:        #切换到搜索栏
    wd.switch_to.window(window)
    if "资料搜集" in wd.title:
        break
mainWindow = wd.current_window_handle
element7=wd.find_elements_by_css_selector(r".list-item-version[style='display:block'] :nth-child(2) .high_light")      #选择试卷所在元素
WebDriverWait(wd,10,0.2).until(lambda x:x.find_element_by_css_selector(r".list-item-version[style='display:block'] :nth-child(2) .high_light"))

# print(len(element7))
# print(element7)
for element in element7:
    # print(element.get_attribute('title'))       #获取元素标题
    # print(element.get_attribute('outerHTML'))     #获取元素完整html
    title=element.get_attribute('title')+'-学科网'
    # wd.execute_script("arguments[0].scrollIntoView();", element)
    #滑动页面至定位的元素
    
    # time.sleep(1)
    # element.send_keys(Keys.ENTER)       #用回车代替点击
    # print("已点击")
    element.click()


    for window in wd.window_handles:
        wd.switch_to.window(window)
        if title in wd.title:       #切换至下载页面

            break
    others=wd.find_elements_by_css_selector('.download[style="background-color: #ff4c4c;width: 238px;"]')
    
    if others !=[]:
        wd.close()
        print("{}为第三方资料，无法下载".format(title))
    ##判断是否为第三方资料
    else:
        element8=wd.find_element_by_css_selector('#btnSoftDownload > div')
        WebDriverWait(wd,10,0.2).until(lambda x:x.find_element_by_css_selector("#btnSoftDownload > div"))
        element8.click()        #点击下载按钮

        time.sleep(1)

        
        element9=wd.find_elements_by_css_selector('body > div.settlementconfirm-content > div.modal-dialog > div.modal-body > div.download.privilege > a')
        if element9 == []:      #判断“确认按钮是否存在”
            time.sleep(5)
            wd.close()
        else:
            try:
                element9=wd.find_element_by_css_selector('body > div.settlementconfirm-content > div.modal-dialog > div.modal-body > div.download.privilege > a')
                element9.click()
                time.sleep(5)
                wd.close()
            except Exception:
                try:
                    element9=wd.find_element_by_css_selector('body > div.settlementconfirm-content > div.modal-dialog > div.modal-body > div.download.free-soft-confirm > a')
                    element9.click()
                    time.sleep(5)
                    wd.close()
                except:
                    pass
            

    wd.switch_to.window(mainWindow)     #返回主界面





