# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 12:13:17 2019

@author: samue
"""
import re
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait

start = int(input('start from: '))
end = int(input('end: '))

website = open("idnamefield.txt", 'r',encoding = 'utf8')
f = open("cited7001-8000.txt", 'w',encoding = 'utf8')

a = website.readlines()
website.close()

driver = webdriver.Chrome(r'C:\Users\samue\Anaconda3\chromedriver.exe')
wait = WebDriverWait( driver, 3 )

apikey= "9063e8fa0133b77bb9c2078bfb440618"

cited=[]
Id=0

for i in range(start-1 , end ):
  
    a[i] = a[i].strip()
    X,Y,Z = a[i].split('\t')
    authorid='%s' %(str(X))
    url = " https://api.elsevier.com/content/author/author_id/"+authorid+"?apiKey="+apikey
    #https://api.elsevier.com/content/serial/title/issn/11266708?apiKey=af481373c3126924cac8b32db190a029
    #https://api.elsevier.com/content/author/author_id/56181319200?apiKey=af481373c3126924cac8b32db190a029
    driver.get(url)
    source = driver.page_source
    soup = bs(source, 'lxml')
    content = soup.find("div",{"id":"collapsible1"})
    if content is None :
        cited.append('0re')
        Id=Id+1
        print("Id :",Id)
            
    else:
        s=re.findall(r"\d+\.?\d*",content.text)
        if len(s)> 6:
            cited.append(s[6])
            Id=Id+1
            print("Id :",Id)
        else:
            cited.append('0')
            Id=Id+1
            print("Id :",Id)
            
for item in cited:     
    f.write(item+'\n')
      
driver.close()
f.close()