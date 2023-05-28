'''
=============
 經理人網站
=============
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

def search(keyword):
    article_list = []
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    # for page_num in range(1,6):
    url =f"https://www.managertoday.com.tw/gsearch?q={keyword}#gsc.tab=0&gsc.q={keyword}&gsc.sort="
    print("導入頁面中...")
    driver.get(url)

    ## 排序方式 button 的位置
    sort_button = driver.find_element(By.CLASS_NAME,"gsc-option-selector")
    print("點擊排序方式")
    sort_button.click()
    time.sleep(2)

    ## 改以日期排序
    sort_date = driver.find_element(By.XPATH,'//div[@class="gsc-option" and text()="日期"]')
    print("點選日期排序")
    sort_date.click()
    time.sleep(2)

    ## 尋找標題連結元素
    search = driver.find_elements(By.CSS_SELECTOR,"a.gs-title")
    # print(search)
    for title in search:
        title_url = title.get_attribute("href")
        # print(title_url)
        ## 抓取標題連結內文
        if title_url is not None:
            response = requests.get(title_url)
            soup = BeautifulSoup(response.text,"html.parser")
            ## 取出文章日期
            date = soup.find("div",class_="hidden md:block").find("span").text
            # print(date)
            ## 取出文章標題
            article_title = soup.find("h1",class_="text-xl font-semibold md:text-3xl inline-block px-5 md:px-0 my-3").text
            # print(article_title)
            article = soup.find("main",class_="htmlview mb-10").text
        #     print(article)
        #     article_list.append(article)
        # time.sleep(2)

    ## 寫入檔案
    # filename = f"{keyword}.txt"
    # with open(filename,mode="w",encoding="utf-8") as f:
    #     f.write(article+"\n")
search("7-11")