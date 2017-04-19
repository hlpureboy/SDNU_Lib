# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 13:35:54 2017

@author: Administrator
"""
from selenium import webdriver
from PIL import Image
import time,requests,pytesseract
from bs4 import BeautifulSoup
import re
import os
def getUser():
    name=raw_input("please input the name:")
    pwd=raw_input("please input the pwd:")
    return name,pwd
def getPic(url):
    loc=url.location
    size=url.size
    print type(loc['x']),type(size['width'])
    ran=(int(loc['x']),int(loc['y']),int(loc['x']+size['width']),int(loc['y']+size['width']))
    f=Image.open("b.png",)
    frame=f.crop(ran)
    frame.save("yzm.png")
    #f.close()
    image=Image.open('yzm.png')
    word=pytesseract.image_to_string(image)
    return word
def login(name,pwd,b):
    #b=webdriver.Firefox()
    b.get("http://210.44.1.6:8080/reader/login.php")
   # b.find_element_by_xpath(".//*[@id='shfd_nav4']").click()
    time.sleep(1)
    b.find_element_by_xpath(".//*[@id='number']").clear()
    b.find_element_by_xpath(".//*[@id='number']").send_keys(name)
    b.find_element_by_xpath(".//*[@id='left_tab']/form/table/tbody/tr[2]/td[2]/input").clear()
    b.find_element_by_xpath(".//*[@id='left_tab']/form/table/tbody/tr[2]/td[2]/input").send_keys(pwd)
    b.find_element_by_xpath(".//*[@id='captcha']").clear()
    b.save_screenshot("b.png")
   # w=getPic("http://210.44.1.6:8080/reader/captcha.php")
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
def parser(text,name):
    soup=BeautifulSoup(text,"html.parser",from_encoding='utf-8')
    content=soup.find_all('div',id="mylib_info")
    #print content
    name=name+".html"
    f=open(name,'w')
    f.write("<html>")
    f.write("\n")
    f.write('''<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />''')
    for i in content:
        f.write(str(i))
    f.write("</html>")
    f.close()
def main():
   # Pic_url="http://210.44.1.6:8080/reader/captcha.php"
    #name,pwd=getUser()
#    word=getPic(Pic_url)
    #text=login(name,pwd)
   # parser(text,name)
   uer_id=int(raw_input("please input the begain number:"))
   end_id=uer_id+45
   #b = webdriver.Firefox()
   while True:
       b = webdriver.Firefox()
       text=login(str(uer_id),str(uer_id),b)
       parser(text,str(uer_id))
       uer_id=uer_id+1
       if uer_id==end_id:
           break
main()