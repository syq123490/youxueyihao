import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

while True:
    keyword = input("请输入关键词：")
    driver = webdriver.Chrome()
    url = 'https://www.baidu.com/s?wd={}'.format(keyword)
    driver.get(url=url)
    locator = By.CSS_SELECTOR,'#page > div > a.n'
    for i in range(5):

        source = driver.page_source
        pattern1 = re.compile('http://www\.baidu\.com/baidu\.php')
        pattern2 = re.compile('<div class="c-abstract">(.*?)</div>', re.S)
        soup = BeautifulSoup(source, 'lxml')
        title = soup.select('h3 a')
        # print(soup.prettify())
        for title in title:
            if re.findall(pattern1, title['href']) != []:
                pass
            else:
                print(title.text)
                print(title['href'])
                print("\n")

        element = WebDriverWait(driver,10)
        element.until(EC.element_to_be_clickable(locator))
        driver.execute_script('window.scrollBy(0,400)')
        page = driver.find_element_by_css_selector('.page-inner .n')
        page.click()
        time.sleep(1)

    driver.close()
