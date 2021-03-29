import os
import requests
from bs4 import BeautifulSoup

for i in range(1):
    MM = range(i)
    url = 'https://baania.com/th/projects?page=1&province=3781'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    logFile = os.path.join("B:\\Pythone\\", "DataNewProject.csv")

    if os.path.exists(logFile):
        log = open(logFile, 'a', encoding="UTF-8")
    else:
        log = open(logFile, 'w', encoding="UTF-8")

#    for match in soup.findAll('span', {"class": "crr"}):
#        match.decompose()

#    for match in soup.findAll('div', {"class": "fa-building-o"}):
#        match.decompose()

#    for match in soup.findAll('div', {"class": "-address "}):
#        match.decompose()

    for i in soup.findAll('div', {"class": "entity-data"}):

        for j in i.findAll('a', {"data-ls-event": "link"}):
            log.write(j.text.replace(',', '') + ',')

        for o in i.findAll('div', {"class": "data-display-line"}):
            log.write(o.text.replace(',', '')+ ',')

#        for o in i.findAll('div', {"class": "data-display-line"}):
#            for p in o.findAll('i'):
#                log.write(p.text.replace(',', '') + ',')
        #print(o)

        for k in i.findAll('div', {"class": "data-display-line -address district"}):
            log.write(str(k.text.replace('', '') + ','))
        #print(k)

        for l in i.findAll('span', {"class": "main-price-value"}):
            log.write(l.text.replace(',', '') + ',')
        #print(l)

        for m in i.findAll('div', {"class": "living-score"}):
            for n in m.findAll('div', {"class": "value"}):
                log.write(n.text.replace('-', '0') + '\n')


        for o in i.findAll('div', {"class": "data-display-line"}):
            for p in o.findAll('div', {"i": "/i"}):
                log.write(p.text.replace(',', '') + ',')
