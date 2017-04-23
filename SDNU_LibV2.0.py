# -*- coding: utf-8 -*-
"""
对图书馆自动程序进行优化
增加数据库操作功能
"""
from selenium import webdriver
from PIL import Image
import time,requests,pytesseract
from bs4 import BeautifulSoup
import re
import os
import MySQLdb
def getUser():
    name=raw_input("please input the name:")
    pwd=raw_input("please input the pwd:")
def getPic(url):
    try:
        loc=url.location
        size=url.size
        print type(loc['x']),type(size['width'])
        ran=(int(loc['x']),int(loc['y']),int(loc['x']+size['width']),int(loc['y']+size['width']))
        f=Image.open("b.png",)
        frame=f.crop(ran)
        frame.save("yzm.png")
        image=Image.open('yzm.png')
        word=pytesseract.image_to_string(image)
        return word
    except:
        print "the key word save error\n"
        return
def login(name,pwd,b):
    try:
        b.get("http://210.44.1.6:8080/reader/login.php")
        time.sleep(1)
        b.find_element_by_xpath(".//*[@id='number']").clear()
        b.find_element_by_xpath(".//*[@id='number']").send_keys(name)
        b.find_element_by_xpath(".//*[@id='left_tab']/form/table/tbody/tr[2]/td[2]/input").clear()
        b.find_element_by_xpath(".//*[@id='left_tab']/form/table/tbody/tr[2]/td[2]/input").send_keys(pwd)
        b.find_element_by_xpath(".//*[@id='captcha']").clear()
        b.save_screenshot("b.png")
        i=b.find_element_by_xpath(".//*[@id='captcha_tips']/a/img")
        w=getPic(i)
        b.find_element_by_xpath(".//*[@id='captcha']").send_keys(w)
        b.find_element_by_xpath(".//*[@id='left_tab']/form/table/tbody/tr[6]/td[2]/input[1]").click()
        time.sleep(1)
        b.get("http://210.44.1.6:8080/reader/redr_info_rule.php")
        text=b.page_source
        time.sleep(1)
        b.close()
        os.system('taskkill /IM firefox.exe')
        return text
    except:
        print 'Unknown Error\n'
        return
def parser(text,name):
    try:
        soup=BeautifulSoup(text,"html.parser",from_encoding='utf-8')
        content=soup.find_all('div',id="mylib_info")
        z= r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$'
        print type(content)
        t=re.findall(r'\d{15}|\d{18}',text)
        print t
        name=name+".html"
        f=open(name,'w')
        f.write("<html>")
        f.write("\n")
        f.write('''<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />''')
        for i in content:
            f.write(str(i))
        f.write("</html>")
        f.close()
        return t
    except:
        print 'html error\n'
        return
def ConnectDB():
    try:
        conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="student",charset="utf8")
        cursor=conn.cursor()
        return cursor,conn
    except:
        print "without mysql\n"
        return
def insert(cursor,num,idcard):
    try:
        sql="insert into stu(number,IDcard) values(%s,%s)"
        for i in idcard:
            IDcard=i
        parm=(num,IDcard)
        cursor.execute(sql,parm)
    except:
        print 'write mysql error'
def close(cursor):
    cursor.close()
def main(u):
    c,d=ConnectDB()
    b=webdriver.Firefox()
    textt=login(u,u,b)
    ID=parser(textt,u)
    insert(c,u,ID)
    d.commit()
    close(c)
count=0
u=raw_input("input the number:")
while count<45:
    main(u)
    count=count+1
    s=int(u)+1
    u=str(s)