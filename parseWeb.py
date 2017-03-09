from bs4 import BeautifulSoup
import urllib2
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
def GetCompanies():
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    table = soup.find_all(class_="wikitable sortable")[0]
    rows = table.find_all("tr")
    comMap = {}
    #print "rows:",len(rows)
    for item in rows:
        #print item.contents
        elems = item.find_all("td")
        if len(elems)==0:
            continue
        infoList = [elems[1].get_text(),elems[3].get_text(),elems[4].get_text()]
        comMap[elems[0].get_text()] = infoList
        print elems[0].get_text(),":",infoList
    jsonstr = json.dumps(comMap)
    fi = open("companies.json","w+")
    fi.write(jsonstr)
    fi.close()
GetCompanies()
