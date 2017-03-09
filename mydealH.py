from __future__ import division
import datetime
import time
import json
import os

path = "./historicaldata/"
outpath = "./out/"
startTime = "2013-01-02"
endTime = "2015-10-30"
mapSet = {}
listSet = []
NodeCnt = 1
step = 8
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

def WriteEdge(NodeSet,fileHandler):
    global mapForNode
    global NodeCnt
    global tmpstr
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
            
def CreateGraphByStep(thisday,golen,curSet,fileHandler):
    if golen>=step and len(curSet)>=2:
        WriteEdge(curSet,fileHandler)
        return
    elif golen>=step:
        return
    
    if thisday>=endday:
        return
    key = str(thisday).replace("-","")
    try:
        dayInfo = mapSet[key]
    except:
        CreateGraphByStep(thisday+datetime.timedelta(1),golen,curSet,fileHandler)
        return
    
    UpSet = []
    DownSet = []
    for item in curSet:
        try:
            if dayInfo[item]==1:
                UpSet.append(item)
            elif dayInfo[item]==-1:
                DownSet.append(item)
        except:
            continue
    CreateGraphByStep(thisday+datetime.timedelta(1),golen+1,UpSet,fileHandler)
    CreateGraphByStep(thisday+datetime.timedelta(1),golen+1,DownSet,fileHandler)
    
def CreateGraph():
    hgrfile = open(outpath+"temp.hgr","w+")
    NodeCnt = 1
    
    thisday = datetime.datetime.strptime(startTime,'%Y-%m-%d').date()
    edgeCnt = 0
    while thisday<=endday:
        anyday = thisday.strftime("%w")
        if anyday=='0' or anyday=='6':
            thisday += datetime.timedelta(1)
            continue
        
        print thisday
        edgeCnt += 1
        
        initSet = []
        CompMap = GetCompMap("companies.json")
        for item in CompMap:
            initSet.append(item)
        CreateGraphByStep(thisday,0,initSet,hgrfile)
        
        thisday += datetime.timedelta(1)
    print "DayCnt:",edgeCnt

    '''
    for item in mapForNode:
        hgrfile.write("\n1")
    '''
    hgrfile.close()
    
    jsonfile = open(outpath+"node.json","w+")
    jsonstr = json.dumps(mapForNode)
    jsonfile.write(jsonstr)
    jsonfile.close()
    
    tmpfile = open(outpath+"tmp.txt","w+")
    tmpfile.write(tmpstr)
    tmpfile.close()


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

def CreateHgraphFile():
    Hgrfile=open(outpath+"Hgraph.hgr","w+")

    temp = open(outpath + "temp.hgr", "r+")
    allECnt=0
    mapForEdges={}
    allEdges = []

    for line in temp.readlines():
        line=line.strip()
        edge=line.split(' ')
        allEdges.append(edge)
        allECnt+=1

    sortLength(allEdges)
    edge1=[]
    tempE = []
    for loop in range(0,len(allEdges)):
        if allEdges[loop] in tempE:
            continue
        edge1 = allEdges[loop]
        w=1
        for i in range(loop+1,len(allEdges)):
            edge2=allEdges[i]
            if set(edge1).issubset(set(edge2)):
                w+=1
        tempE.append(edge1)
        mapForEdges[loop] = w / step

    Hgrfile.write(str(len(mapForEdges))+" "+str(NodeCnt)+" "+"11\n")
    for edge in mapForEdges:
        Hgrfile.write(str(int(mapForEdges[edge])))
        for i in range(len(allEdges[edge])):
            Hgrfile.write(" "+allEdges[edge][i])
        Hgrfile.write("\n")

    for i in range(NodeCnt-1):
         Hgrfile.write("1\n")
    Hgrfile.write("1")

    Hgrfile.close()



def mainfunc():
    NodeCnt = 1
    ListFile()
    CreateGraph()
    CreateHgraphFile()
mainfunc()
