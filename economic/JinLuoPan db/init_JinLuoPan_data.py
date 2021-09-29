# encoding=utf-8
#本例子完成通过输入页数，进行跳转的操作
#需要安装selenium MySQLdb BeautifulSoup
from selenium import webdriver
import MySQLdb
from bs4 import BeautifulSoup
import re
import time

driver = webdriver.Chrome()
driver.get("http://q.stock.sohu.com/jlp/res/listresv2.up")

db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="golden compass", charset="utf8")
cursor = db.cursor()

for i in range(1,20638):
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    ############################################################################排除网页总是跳转网易主页的问题
    while len(soup.body.find_all(class_="td3")) == 0:#如果跳转就刷新
        driver.refresh();
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')

    elem = driver.find_elements_by_name("pageNum")#跳到第pageNum页
    elem[1].send_keys(i)
    elem2 = driver.find_element_by_class_name("go1")
    elem2.click()

    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    while len(soup.body.find_all(class_="td3")) == 0:#如果跳转就刷新
        driver.refresh();
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
    print (i)

    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    ############################################################################处理html
    # 研究员名字
    tag = soup.body.find_all(class_="td1")
    count = 0
    researcher = [1] * (len(tag))
    for s in tag:
        researcher[count] = s.find("a").text
        count = count + 1
    print (researcher[0])

    # 研究员公司
    tag = soup.body.find_all(class_="last")
    count = 0
    broker = [1] * (len(tag))
    for s in tag:
        broker[count] = s.find("a").text
        count = count + 1
    print (broker[0])

    # 公司名字和代码
    tag = soup.body.find_all(class_="td2")
    count = 0
    stockName = [1] * (len(tag))
    stockCode = [1] * (len(tag))
    for s in tag:
        temp = str(s)
        stockCode[count] = re.findall(r"secCode=([^\"]*)", temp)
        stockName[count] = s.find("a").text
        count = count + 1

    print (stockCode[0])
    print (stockName[0])

    # 公司所属行业
    tag = soup.body.find_all(class_="td3")
    count = 0
    stockIndustry = [1] * (len(tag))
    for s in tag:
        stockIndustry[count] = s.find("a").text
        count = count + 1
    print (stockIndustry[0])

    # 点评日期
    tag = soup.body.find_all(class_="td4")
    count = 0
    commentDate = [1] * (len(tag))
    for s in tag:
        ss=s.text
        ss=ss.replace("\n", "")
        ss=ss.replace(" ", "")
        commentDate[count] = s.text.replace("\r\n", "").replace(" ", "")
        count = count + 1
    print (commentDate[0])

    # 点评价格
    tag = soup.body.find_all(class_="td5")
    count = 0
    commentPrice = [1] * (len(tag))
    for s in tag:
        commentPrice[count] = s.text.replace("\n", "").replace(" ", "")
        count = count + 1
    print (commentPrice[0])

    # 目标价格
    tag = soup.body.find_all(class_="td7")
    count = 0
    targetPrice = [1] * (len(tag))
    for s in tag:
        targetPrice[count] = s.text.replace("\n", "").replace(" ", "")
        count = count + 1
    print (targetPrice[0])

    # 目标空间
    tag = soup.body.find_all(class_="td8")
    count = 0
    targetSpace = [1] * (len(tag))
    for s in tag:
        ss=s.text.replace("\n", "")
        ss=ss.replace(" ", "")
        targetSpace[count] = s.text.replace("\n", "").replace(" ", "")
        count = count + 1
    print (targetSpace[0])

    # 推荐理由
    tag = soup.body.find_all(class_="td13")
    count = 0
    commentReason = [1] * (len(tag))
    for s in tag:
        commentReason[count] = s.text.replace("\r", "").replace(" ", "").replace("\n", "")
        count = count + 1
    print (commentReason[0])


    ############################################################################存入数据库
    size = len(stockCode);
    for i in range(size):
        if stockCode[i][0]==None or stockName[i]==None or commentDate[i]==None:
            continue
        print (commentDate[i], commentPrice[i], targetPrice[i],targetSpace[i])
        cursor.execute("insert ignore into report(stockCode,stockName,stockIndustry,researcher,broker,commentDate,commentPrice,targetPrice,targetSpace,commentReason)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(stockCode[i][0],stockName[i], stockIndustry[i], researcher[i], broker[i], commentDate[i], commentPrice[i], targetPrice[i],targetSpace[i], commentReason[i]))
        db.commit();