import os
import requests

from bs4 import BeautifulSoup

for i in range (1):
    pagenum = (i)
    url = 'https://www.baania.com/th/s/'+ str("ทั้งหมด") +'/listing?mapMove=true&page='+ str(pagenum) +'&propertyType=1,2,3&sellState=on-sale'
    #print(url)

    soup = BeautifulSoup(response.text, "html.parser")
    logFile = os.path.join("D:\\2. Project Python\\Python\\", "test.csv")

    #if os.path.exists(logFile):
    #    log = open(logFile, 'a', encoding="UTF-8")
    #else:
    #    log = open(logFile, 'w', encoding="UTF-8")   

    for i in soup.findAll('div', {"class": "boxList row"}):
        print(i)
        #for j in i.findAll('h3', {"class": "size-2 mb-0 qfCvIrOS7WEhmJ14DrrA9"}):
        #    sp = j.text.strip()#.split(' ')
        #    log.write(str(sp)+',')
        #    print(sp)

