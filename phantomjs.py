from selenium import webdriver

browser = webdriver.PhantomJS()
url = 'http://www.baidu.com'
browser.get(url)
browser.save_screenshot("baidu.png")

browser.close()
