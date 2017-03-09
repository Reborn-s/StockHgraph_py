from __future__ import division
import datetime
import time
import json
import os

path = "./historicaldata/"
outpath = "./out/"
startTime = "2013-01-02"
#startTime = "2015-09-15"
endTime = "2015-10-30"
mapSet = {}
mapForSame={}
listSet = []
NodeCnt = 1
hedge=0
step = 400
mapForNode = {}
tmpstr = ""
endday = datetime.datetime.strptime(endTime,'%Y-%m-%d').date()
def GetStockInfo(filename):
    ans = {}
    try:
        fi = open(path+filename,"r")
    except:
        return ans
    
    if not fi:
        return ans
    content = fi.read()
    lines = content.split("\n")
    for line in lines:
        elems = line.split(",")
        if len(elems) > 6:
            UpOrDown = 0
            if float(elems[2])>float(elems[5])+0.5 or float(elems[2])*(1-0.02)>float(elems[5]):
                UpOrDown = -1
            elif float(elems[2])<float(elems[5])-0.5 or float(elems[2])*(1+0.02)<float(elems[5]):
                UpOrDown = 1
            try:
                mapSet[elems[1]][elems[0]] = UpOrDown
            except:
                mapSet[elems[1]] = {}
                mapSet[elems[1]][elems[0]] = UpOrDown


    fi.close()
    
def ListFile():
    for root, dirs, files in os.walk(path):
        for onefile in files:
            GetStockInfo(onefile)
    fo = open("m2.txt","w+")
    for item in mapSet:
        #print item
        daym = mapSet[item]
        uplist = []
        downlist = []
        for st in daym:
            if daym[st] == 1:
                uplist.append(st)
            elif daym[st] == -1:
                downlist.append(st)
        if len(uplist)>0:
                fo.write(uplist[0])
        for loop in range(1,len(uplist)):
            fo.write(","+uplist[loop])
        if len(uplist)>0:
            fo.write("\n")
            
        if len(downlist)>0:
            fo.write(downlist[0])
        for loop in range(1,len(downlist)):
            fo.write(","+downlist[loop])
        if len(downlist)>0:
            fo.write("\n")
    fo.close()
    

def GetCompMap(filename):
    fi = open(filename,"r")
    jsonstr = fi.read()
    CompMap = json.loads(jsonstr)
    fi.close()
    return CompMap

def WriteEdge(weight,NodeSet,fileHandler):

    global mapForNode
    global NodeCnt
    global tmpstr
    fileHandler.write(str(int(weight/step))+" ")
    for item in NodeSet:
        try:
            node = mapForNode[item]
        except:
            node = NodeCnt
            mapForNode[item]=node
            tmpstr += "\n"+str(NodeCnt)+":"+item
            NodeCnt += 1
            
        fileHandler.write(str(node)+" ")
    fileHandler.write("\n")

def sortLength(L):
    n=len(L)
    for i in range(n):
        k=i
        j=i+1
        while j<n:
            if len(L[k])>len(L[j]):
                k=j
            j=j+1
        if i!=k:
            temp=L[k]
            L[k]=L[i]
            L[i]=temp

def CreateHgraphByStep(oldComMap,listSet,edgeSets,hgr,cnt):
    print str(cnt+1)+" nodes in edges then..."
    global hedge
    print "hedge now:",hedge
    ifreturn=0
    for edge in oldComMap:
        for day in oldComMap[edge]:
            if oldComMap[edge][day]==1 or oldComMap[edge][day]==-1:
                ifreturn+=1
    if ifreturn==0:
        return

    newComMap={}
    newEdgeSets=[]
    for i in range(len(listSet)):
        for edge in oldComMap:
            same = []
            newComSet={}
            thisnodes=edge.split("#")
            if not listSet[i][0] in thisnodes:
                for day1 in listSet[i][1]:
                    try:
                        if listSet[i][1][day1] == oldComMap[edge][day1]:
                            same.append(listSet[i][1][day1])
                    except:
                        continue
                if (len(same)-same.count(0))>=step:
                    for k in listSet[i][1]:
                        try:
                            if not (listSet[i][1][k] == oldComMap[edge][k] and (
                                listSet[i][1][k] == 1 or listSet[i][1][k] == -1)):
                                newComSet[k] = 0
                            else:
                                newComSet[k] = listSet[i][1][k]
                        except:
                            continue
                    hedge +=1
                    newComMap[edge+"#"+listSet[i][0]]=newComSet
                    for j in range(len(edgeSets)):
                        if thisnodes==edgeSets[j]:
                            edgeSets[j].append(listSet[i][0])
                            newEdgeSets.append(edgeSets[j])
                            break
                    edgeSets=[]
    for e in newEdgeSets:
        WriteEdge(len(same)-same.count(0),e,hgr)

    cnt+=1
    print "edge nodes:",cnt
    CreateHgraphByStep(newComMap,listSet,newEdgeSets,hgr,cnt)


def CreateHgraph(hgr):
    global hedge


    for day in mapSet:
        for st in mapSet[day]:
            try:
                mapForSame[st][day]=mapSet[day][st]
            except:
                mapForSame[st]={}
                mapForSame[st][day] = mapSet[day][st]
            #mapForSame.setdefault(st,[]).append(mapSet[day][st])

    print "two nodes in hedge first..."
    listSet=mapForSame.items()

    newComMap={}
    edgeSets=[]

    for i in range(len(listSet)-1):
        for j in range(i+1,len(listSet)):
            same = []
            newComSet = {}
            for day1 in listSet[i][1]:
                try:
                    if listSet[i][1][day1]==listSet[j][1][day1]:
                        same.append(listSet[i][1][day1])
                except:
                    continue
            if (len(same)-same.count(0))>=step:
                for k in listSet[i][1]:
                    try:
                        if not (listSet[i][1][k] == listSet[j][1][k] and (listSet[i][1][k] == 1 or listSet[i][1][k] == -1)):
                            newComSet[k]=0
                        else:
                            newComSet[k]=listSet[i][1][k]
                    except:
                        continue
                hedge+=1
                nodeSet=[]
                nodeSet.append(listSet[i][0])
                nodeSet.append(listSet[j][0])
                edgeSets.append(nodeSet)
                newComMap[listSet[i][0]+"#"+listSet[j][0]]=newComSet
                WriteEdge(len(same)-same.count(0),nodeSet,hgr)

    CreateHgraphByStep(newComMap,listSet,edgeSets,hgr,2)

    tmpfile = open(outpath + "tmp.txt", "w+")
    tmpfile.write(tmpstr)
    tmpfile.close()


def mainfunc():
    NodeCnt = 1
    ListFile()
    hgr = open(outpath + "Hgraph.hgr", "w+")
    CreateHgraph(hgr)
    hgr.close()
    #CreateHgraphFile()

mainfunc()
