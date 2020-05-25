# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 09:15:49 2019

@author: samue
"""
import re
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait


start = int(input('start from: '))
end = int(input('end: '))

website = open("paper.txt", 'r',encoding = 'utf8')
f = open("citescore701to1500.txt", 'w',encoding = 'utf8')


a = website.readlines()
website.close()

driver = webdriver.Chrome(r'C:\Users\samue\Anaconda3\chromedriver.exe')
wait = WebDriverWait( driver, 3 )

total=0
num=len(a)
right=0
error=0
citescore=[]
ISSN=[]
count=0
#for i in range(1):

for i in range(start-1, end):
  
    a[i] = a[i].strip()
    X,Y,Z = a[i].split('$')
    Url='%s' %(str(Z))
    
    #res= requests.get(Url, auth=('user', 'passwd'))
    #soup = bs(res.text, 'lxml')
    driver.get(Url)
    source = driver.page_source
    soup = bs(source, 'lxml')
    content = soup.find_all('ul',{"id":"citationInfo"})
    
    
    
    apikey = "af481373c3126924cac8b32db190a029"
    
    
    for cont in content:
        con = cont.find('li').text
        if 'ISSN' in con:
            total=total+1
            right=right+1
            print("O :",right,total)
            ISSN.append(con[7:len(con)])
        else:
            total=total+1
            error=error+1
            print("X :",error,total)
            ISSN.append(0)

         
    #https://api.elsevier.com/content/author/author_id/56181319200?apiKey=af481373c3126924cac8b32db190a029    
    
    #url = 'https://api.elsevier.com/content/serial/title/issn/00046361?apiKey=af481373c3126924cac8b32db190a029'
    #driver.get(url)
    #source = driver.page_source
    #soup = bs(source, 'lxml')
    #score = soup.find("div",{"id":"collapsible4"})
    #x=re.findall(r"\d+\.?\d*",score.text)
    #citescore.append(x[0])

for issn in ISSN:
    if issn == 0 :
        citescore.append('0')
    else:
        url = "https://api.elsevier.com/content/serial/title/issn/"+issn+"?apiKey="+apikey
        driver.get(url)
        source = driver.page_source
        soup = bs(source, 'lxml')
        score = soup.find("div",{"id":"collapsible4"})
        if score is None :
            citescore.append('0')
            
        else:
            s=re.findall(r"\d+\.?\d*",score.text)      
            citescore.append(s[0])

for item in citescore:     
    f.write(item+'\n')
    

#print(citescore)
f.close()
driver.close()