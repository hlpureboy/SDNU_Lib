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
        name=name+".html"
        f=open(name,'w')
        f.write("<html>")
        f.write("\n")
        f.write('''<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />''')
        for i in content:
            f.write(str(i))
        f.write("</html>")
        f.close()
        f=open(name,'r')
        html=f.read()
        f.close()
        cont=BeautifulSoup(html,"html.parser")
        data=cont.find_all("td")
        os.remove(name)
        return data
    except:
        print 'html error\n'
        return
def ConnectDB():
    try:
        conn=MySQLdb.connect(host="112.74.204.232",user="root",passwd="123pyj",db="student",charset="utf8")
        cursor=conn.cursor()
        return cursor,conn
    except:
        print "without mysql\n"
        return
def insert(cursor,data):
    try:
        sql="insert into user_data(user_ID,user_Name,user_Grade,user_ID_card,user_Phone_number,user_Email) values(%s,%s,%s,%s,%s,%s)"
        parm=(data[2].get_text(),data[1].get_text(),data[18].get_text(),data[17].get_text(),data[25].get_text(),data[16].get_text())
        cursor.execute(sql,parm)
    except:
        print 'write mysql error'
def close(cursor):
    cursor.close()
def main(u):
    c,d=ConnectDB()
    b=webdriver.Firefox()
    textt=login(u,u,b)
    data=parser(textt,u)
    insert(c,data)
    d.commit()
    close(c)
count=0
u=raw_input("input the number:")
while count<45:
    main(u)
    count=count+1
    s=int(u)+1
    u=str(s)