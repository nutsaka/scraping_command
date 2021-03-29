import os
import requests
from bs4 import BeautifulSoup

for i in range(5):
    MM = (i)
    url = 'https://baania.com/th/listing?page='+ str(MM) +"&stype=for-sale&province="
    response = requests.get(url)
    #print(url)

    soup = BeautifulSoup(response.text, "html.parser")

    logFile = os.path.join("B:\\Pythone\\", "มือ5.csv")

    if os.path.exists(logFile):
        log = open(logFile, 'a', encoding="UTF-8")
    else:
        log = open(logFile, 'w', encoding="UTF-8")

    #for match in soup.findAll('span', {"class": "crr"}):
    #    match.decompose()

    #for match in soup.findAll('div', {"class": "fa-building-o"}):
    #    match.decompose()

    #for match in soup.findAll('div', {"class": "-address "}):
     #   match.decompose()

    for i in soup.findAll('div', {"class": "entity-data"}):

        for j in i.findAll('h3', {"class": "listing-title"}):
            sp = j.text.strip()#.split(' ')
            log.write(str(sp)+',')
                #print(sp)

        for r in i.findAll('div', {"class": "data-lines"}):
            #sp = r.text.strip().split(' ')
            #print(sp)
            spss = r.text.strip().split()
            log.write(str(spss))
            #print(spss)


        for m in i.findAll('div', {"class": "data-display-line"}):
            splittedText = m.text.strip().split(' ')
            #print(m)

            if (len(splittedText) > 1):
                if (splittedText[1] != '·' and splittedText[1] != '·'):
                    num_bedroom = splittedText[1]
                    num_bathroom = splittedText[3]
                    room_area = splittedText[5]
                    log.write(str(num_bedroom) + ',' + str(num_bathroom) + ',' + str(room_area) + ',')

        for n in i.findAll('span', {"class": "main-price-value"}):
            log.write(n.text.replace(',', '') + ',')
            print(n)

#            for o in i.findAll('span', {"class": "sub-price-value"}):
#                log.write(o.text.replace('-', '0') + ',')
#                print(o)

        for p in i.findAll('div', {"class": "living-score"}):
            for q in p.findAll('div', {"class": "value"}):
                log.write(q.text.replace('-', '0') + '\n')





#        for o in i.findAll('div', {"class": "data-display-line"}):
#            for p in o.findAll('div', {"i": "/i"}):
#                log.write(p.text.replace(',', '') + ',')
#                print(p)