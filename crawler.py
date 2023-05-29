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
import json
import pymysql

'''
=====================
 以日期排序爬取第一頁
=====================
'''
def search(keyword):
    article_list = []
    title_url_list = []
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    url =f"https://www.managertoday.com.tw/gsearch?q={keyword}#gsc.tab=0&gsc.q={keyword}&gsc.sort="
    print("--導入頁面中...--")
    driver.get(url)

    ## 排序方式 button 的位置
    sort_button = driver.find_element(By.CLASS_NAME,"gsc-option-selector")
    print("--點擊排序方式--")
    sort_button.click()
    time.sleep(2)

    ## 改以日期排序
    sort_date = driver.find_element(By.XPATH,'//div[@class="gsc-option" and text()="日期"]')
    print("--點選日期排序--")
    sort_date.click()
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source,"html.parser")
    elements = soup.findAll("div",{"class":"gs-webResult gs-result"})
    for content in elements:
        link = content.findChild("div").findChild("div").findChild("a").get("href")
    # print(type(title_url))
        title_url_list.append(link)
    # print(title_url_list)
    for title_url in title_url_list:
        if title_url is not None:
            response = requests.get(title_url)
            soup_title = BeautifulSoup(response.text,"html.parser")
            title = soup_title.find("h1").text
            date = soup_title.find("div",class_="hidden md:block").find("span").text
            article = soup_title.find("main",class_="htmlview mb-10").text
            article_dict = {}
            article_dict["Date"] = date
            article_dict["Title"] = title
            article_dict["Content"] = article
        article_list.append(article_dict)
    # print(article_list)
    filename = f"{keyword}.txt"
    with open(filename,mode="w",encoding="utf-8") as f:
        json.dump(article_list,f,ensure_ascii=False,indent=4)
        time.sleep(4)

# ===============================================
#                  匯入MySQL
# ===============================================
    # db = pymysql.connect(
    #     host = "127.0.0.1",
    #     user = "root",
    #     password = "123456",
    #     port = 3306,
    #     db = "Topic 3"
    # )
    # cursor = db.cursor()
    # # 顯示 Manager Table
    # cursor.execute("show tables like 'Manager'")
    # result = cursor.fetchone()
    # if result is not None:
    #     print("Manager Exists !")
    #     cursor.execute("drop table Manager")
    #     cursor.execute("create table Manager (Date varchar(300),Title varchar(1000),Content varchar(60000))")
    # else:
    #     print("Manager does Not Exists !")
    #     cursor.execute("create table Manager (Date varchar(300),Title varchar(1000),Content varchar(60000))")
    
# search("7-11")

'''
=====================
 以日期排序爬取每一頁
=====================
'''
def search_date(keyword):
    article_list = []
    title_url_list = []
    options = webdriver.ChromeOptions()
    # options.add_argument("incognito")
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    for page_num in range(1,5):
        # print("--第"+str(page_num-1)+"頁--")
        url =f"https://www.managertoday.com.tw/gsearch?q={keyword}#gsc.tab=0&gsc.q={keyword}&gsc.sort=date&gsc.page="+str(page_num)
        print("--導入頁面中...--")
        driver.get(url)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        elements = soup.findAll("div",{"class":"gs-webResult gs-result"})
        # print(elements)
        for content in elements:
            link = content.findChild("div").findChild("div").findChild("a").get("href")
            # print(type(title_url))
            title_url_list.append(link)
            # print(title_url_list)
        for title_url in title_url_list:
            if title_url is not None and title_url != "https://www.managertoday.com.tw/columnist/view/3421":
                response = requests.get(title_url)
                soup_title = BeautifulSoup(response.text,"html.parser")
                title = soup_title.find("h1").text
                date = soup_title.find("div",class_="hidden md:block").find("span").text
                article = soup_title.find("main",class_="htmlview mb-10").text
                article_dict = {}
                article_dict["Date"] = date
                article_dict["Title"] = title
                article_dict["Content"] = article
            article_list.append(article_dict)
        if page_num == 4:
            print("--已完成--")
        else:
            print("--下一頁--")
    # print(article_list)
    filename = f"{keyword}.txt"
    with open(filename,mode="w",encoding="utf-8") as f:
        json.dump(article_list,f,ensure_ascii=False,indent=4)
        time.sleep(4)

# ===============================================
#                  匯入MySQL
# ===============================================
    # db = pymysql.connect(
    #     host = "127.0.0.1",
    #     user = "root",
    #     password = "123456",
    #     port = 3306,
    #     db = "Topic 3"
    # )
    # cursor = db.cursor()
    # # 顯示 Manager Table
    # cursor.execute("show tables like 'Manager'")
    # result = cursor.fetchone()
    # if result is not None:
    #     print("Manager Exists !")
    #     cursor.execute("drop table Manager")
    #     cursor.execute("create table Manager (Date varchar(300),Title varchar(1000),Content varchar(60000))")
    # else:
    #     print("Manager does Not Exists !")
    #     cursor.execute("create table Manager (Date varchar(300),Title varchar(1000),Content varchar(60000))")
    
# search_date("7-11")

'''
=========================
 以關聯性為排序爬取每一頁
=========================
'''
def search_relation(keyword):
    article_list = []
    title_url_list = []
    options = webdriver.ChromeOptions()
    # options.add_argument("incognito")
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    for page_num in range(1,5):
        # print("--第"+str(page_num-1)+"頁--")
        url =f"https://www.managertoday.com.tw/gsearch?q={keyword}#gsc.tab=0&gsc.q={keyword}&gsc.sort=&gsc.page="+str(page_num)
        print("--導入頁面中...--")
        driver.get(url)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        elements = soup.findAll("div",{"class":"gs-webResult gs-result"})
        # print(elements)
        for content in elements:
            link = content.findChild("div").findChild("div").findChild("a").get("href")
            # print(type(title_url))
            title_url_list.append(link)
            # print(title_url_list)
        for title_url in title_url_list:
            if title_url is not None and title_url != "https://www.managertoday.com.tw/columnist/view/3421":
                response = requests.get(title_url)
                soup_title = BeautifulSoup(response.text,"html.parser")
                title = soup_title.find("h1").text
                date = soup_title.find("div",class_="hidden md:block").find("span").text
                article = soup_title.find("main",class_="htmlview mb-10").text
                article_dict = {}
                article_dict["Date"] = date
                article_dict["Title"] = title
                article_dict["Content"] = article
            article_list.append(article_dict)
        if page_num == 4:
            print("--已完成--")
        else:
            print("--下一頁--")
    # print(article_list)
    filename = f"{keyword}_relation.txt"
    with open(filename,mode="w",encoding="utf-8") as f:
        json.dump(article_list,f,ensure_ascii=False,indent=4)
        time.sleep(4)

# ===============================================
#                  匯入MySQL
# ===============================================
    # db = pymysql.connect(
    #     host = "127.0.0.1",
    #     user = "root",
    #     password = "123456",
    #     port = 3306,
    #     db = "Topic 3"
    # )
    # cursor = db.cursor()
    # # 顯示 Manager Table
    # cursor.execute("show tables like 'Manager'")
    # result = cursor.fetchone()
    # if result is not None:
    #     print("Manager Exists !")
    #     cursor.execute("drop table Manager")
    #     cursor.execute("create table Manager (Date varchar(300),Title varchar(1000),Content varchar(60000))")
    # else:
    #     print("Manager does Not Exists !")
    #     cursor.execute("create table Manager (Date varchar(300),Title varchar(1000),Content varchar(60000))")
    
# search_relation("7-11")
