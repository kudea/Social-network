# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import sys
from bs4 import BeautifulSoup as bs
import time
f = open("AuthorId.txt", 'w',encoding = 'utf8')
authorid=0
#coauthorid=0
with open('scopus.csv', newline='',encoding='utf8') as csvfile:   
# 讀取 CSV 檔內容，將每一列轉成一個 dictionary
    rows = csv.DictReader(csvfile)
# 以迴圈輸出指定欄位
    for row in rows:
        AuthorId=row['id']
        authorid+=1
        url='https://www.scopus.com/authid/detail.uri?authorId=%s'%(AuthorId)
        driver = webdriver.Chrome(r'C:\Users\samue\Anaconda3\chromedriver.exe')
        driver.get(url)
        print(authorid)
        source = driver.page_source
        soup = bs(source, 'lxml')
        doctitle = soup.find_all('td',{"data-type":"docTitle"})
        for d in doctitle:
            href = d.find('a')['href']
            driver.get(href)
            f.write('\n')
            source = driver.page_source
            soup = bs(source, 'lxml')
            authorname = soup.find_all('ul',{'class':'list-inline'})
            for a in authorname:
                name = a.find_all('a')
                for i in name:
                    n = i.get('href')
                    f.write(n+'$')

                    #coauthorid+=1
                    #print(coauthorid)
                    

            
                
driver.close()
f.close()
                