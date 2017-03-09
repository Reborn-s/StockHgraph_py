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

def GetFieldsForC():
    fi = open("companies.json","r+")
    content = fi.read()
    com = json.loads(content)
    fi.close()
    fi = open("ans.txt","r+")
    content = fi.read()
    lines = content.split("\n")
    fo = open("fields.txt","w+")
    fieldcnt = {}
    cnt = 0
    for line in lines:
        elems = line.split(" ")
        fields = []
        for elem in elems:
            if elem=="":
                continue
            field = com[elem][1]
            if field not in fields:
                fields.append(field)
        for f in fields:
            fo.write(f+";")
            if f in fieldcnt:
                fieldcnt[f] += 1
            else:
                fieldcnt[f] = 1
        fo.write("\n")
    fo2 = open("fieldcnt.txt","w+")
    for f in fieldcnt:
        fo2.write(f+" "+str(fieldcnt[f])+"\n")
    fo.close()
    fo2.close()
    
GetFieldsForC()
