import json
import random
def GetStocks(filename):
    fi = open(filename,"r+")
    content = fi.read()
    lines = content.split("\n")
    anslist = []
    for line in lines:
        if line!="":
            item = line.split(" ")[0]
            anslist.append(item)
    fi.close()
    return anslist

def loadfile(filename):
    fi = open(filename,"r+")
    content = fi.read()
    com = json.loads(content)
    sl = GetStocks("newnode.txt")
    fieldmap = {}
    for item in com:
        if item not in sl:
            continue
        field = com[item][1]
        if field in fieldmap:
            fieldmap[field].append(item)
        else:
            fieldmap[field] = [item]
    fi.close()
    return fieldmap

def deal():
    fields = loadfile("companies.json")
    fo = open("singleC.txt","w+")
    for item in fields:
        thislist = fields[item]
        print item,len(thislist)
        random.shuffle(thislist)
        index = 0
        while index<len(thislist):
            ilen = random.randint(6,18)
            if ilen+index>len(thislist):
                ilen = len(thislist)-index
            for elem in thislist[index:index+ilen]:
                fo.write(elem+" ")
            fo.write("\n")
            #print index
            index = index+ilen
        fo.write("\n")
    fo.close()
deal()
