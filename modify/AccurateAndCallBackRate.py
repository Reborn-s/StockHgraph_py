import json
import random
allcntmap1 = {}
allcntmap2 = {}
allcntmap3 = {}
def GetComMap():
    fi = open("companies.json","r+")
    content = fi.read()
    coms = json.loads(content)
    fi.close()
    return coms

def getAnsFile(file):
    allmap={}

    partmap = {}

    result=open(file,"r+")
    rcontent=result.read()
    rlines=rcontent.split("\n")

    mapfile = open("map.txt", "r+")
    mlines=mapfile.readlines()
    for lines in mlines:
        elems=lines.split(" ")
        allmap[elems[0]]=elems[1].strip("\n")

    node = 1
    for part in rlines:
        if part=="":
            continue
        if part in partmap:
            partmap[part].append(allmap[str(node)])
        else:
            partmap.setdefault(part, []).append(allmap[str(node)])
        node+=1

    ans = open("ans.txt", "w+")
    for part in partmap:
        for node in partmap[part]:
            ans.write(str(node)+" ")
        ans.write("\n")
    ans.close()
    result.close()
    mapfile.close()

def dealline(line,coms):
    elems = line.split(" ")
    fieldsmap = {}
    totalcnt = 0
    for elem in elems:
        if elem=="":
            continue
        totalcnt += 1
        thisf = coms[elem][1]
        if thisf in fieldsmap:
            fieldsmap[thisf] += 1
        else:
            fieldsmap[thisf] = 1
        if thisf in allcntmap3:
            allcntmap3[thisf]+=1
        else:
            allcntmap3[thisf]=1
    tmpdic = sorted(fieldsmap.iteritems(),key=lambda d:d[1],reverse=True)
    field = tmpdic[0][0]
    cnt = tmpdic[0][1]
    if field in allcntmap1:
        allcntmap1[field] += cnt
        allcntmap2[field] += totalcnt
    else:
        allcntmap1[field] = cnt
        allcntmap2[field] = totalcnt

def mainfunc(file):
    getAnsFile(file)
    fi = open("ans.txt","r+")
    content = fi.read()
    lines = content.split("\n")
    fi.close()
    coms = GetComMap()
    for line in lines:
        if line=="":
            continue
        dealline(line,coms)
    for item in allcntmap1:
        precision=float(allcntmap1[item])/allcntmap2[item]
        recall=float(allcntmap1[item])/allcntmap3[item]
        print item,"\t",allcntmap1[item],"\t",allcntmap2[item],"\t",allcntmap3[item],"\t","precision:",precision,"\t","recall:",recall
mainfunc("partition.txt")
