# encoding=utf-8
#本例子完成通过输入页数，进行跳转的操作
#需要安装selenium MySQLdb BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
import xlwt

driver = webdriver.Chrome()
driver2 = webdriver.Chrome()
driver.get("http://www.landnj.cn/LandBargainInfo.aspx?Type=0")

workbook = xlwt.Workbook() #注意Workbook的开头W要大写
sheet = workbook.add_sheet('sheet',cell_overwrite_ok=True)
row_num = 0;

for i in range(1,2):
    html = driver.page_source
    soup = BeautifulSoup(html)

    elem = driver.find_elements_by_name("ctl00$ContentPlaceHolder1$AspNetPager1_input")#跳到第pageNum页
    elem[0].clear()
    elem[0].send_keys(i)
    elem2 = driver.find_element_by_id("ctl00$ContentPlaceHolder1$AspNetPager1_btn")
    elem2.click()

    html = driver.page_source
    soup = BeautifulSoup(html)
    count = 1
    for temp in soup.body.find_all('a',attrs={"style":"text-decoration:underline"}):
        url = "http://www.landnj.cn/"+temp.get("href")
        print(url)
        count = count + 1
        row_num = row_num + 1

        driver2.get(url)
        html2 = driver2.page_source
        soup2 = BeautifulSoup(html2)
        id_value = "ctl00_ContentPlaceHolder1_GVList_ctl%02d_lbltown"%count

        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label1').string)#地块编号
        sheet.write(row_num, 1, soup2.find(id='ctl00_ContentPlaceHolder1_Label1').string)
        print (soup.find(id=id_value).string)#区域
        sheet.write(row_num, 2, soup.find(id=id_value).string)
        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label2').string)#地块位置
        sheet.write(row_num, 3, soup2.find(id='ctl00_ContentPlaceHolder1_Label2').string)
        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label3').string)#容积率
        sheet.write(row_num, 4, soup2.find(id='ctl00_ContentPlaceHolder1_Label3').string)
        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label4').string)#用地性质
        sheet.write(row_num, 5, soup2.find(id='ctl00_ContentPlaceHolder1_Label4').string)
        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label5').string)#规划面积
        sheet.write(row_num, 6, soup2.find(id='ctl00_ContentPlaceHolder1_Label5').string)
        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label6').string)#出让面积
        sheet.write(row_num, 7, soup2.find(id='ctl00_ContentPlaceHolder1_Label6').string)
        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label7').string)#公告时间
        sheet.write(row_num, 8,soup2.find(id='ctl00_ContentPlaceHolder1_Label7').string )
        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label8').string)#挂牌起始价
        sheet.write(row_num, 9, soup2.find(id='ctl00_ContentPlaceHolder1_Label8').string)
        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label13').string)#成交时间
        sheet.write(row_num, 10, soup2.find(id='ctl00_ContentPlaceHolder1_Label13').string)
        ss=soup2.find(id='ctl00_ContentPlaceHolder1_Label14')
        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label14').text)#成交总额
        sheet.write(row_num, 11,soup2.find(id='ctl00_ContentPlaceHolder1_Label14').text )
        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label18').string)#竞得人
        sheet.write(row_num, 12, soup2.find(id='ctl00_ContentPlaceHolder1_Label18').string)
        print (soup2.find(id='ctl00_ContentPlaceHolder1_Label19').string)#公告编号
        sheet.write(row_num, 13, soup2.find(id='ctl00_ContentPlaceHolder1_Label19').string)
        print ("http://www.landnj.cn/"+ (soup2.find_all('a',attrs={"style":"color:red"}))[0].get("href"))#公告编号地址
        sheet.write(row_num, 14, "http://www.landnj.cn/"+ (soup2.find_all('a',attrs={"style":"color:red"}))[0].get("href"))

workbook.save('D:\\Code\\Python\\test2.xls')
print ('创建excel文件完成！')