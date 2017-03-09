#from __future__ import division
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
step = 22
mapForNode = {}
tmpstr = ""
endday = datetime.datetime.strptime(endTime,'%Y-%m-%d').date()

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

    allEdges=[]
    mapForEdges={}
    temp=open(outpath+"temp.hgr","r+")
    for line in temp.readlines():
        line=line.strip()
        edge=line.split(' ')
        allEdges.append(edge)

    sortLength(allEdges)
    edge1=[]
    tempE=[]
    for loop in range(0,len(allEdges)):
        if allEdges[loop] in tempE:
            continue
        edge1=allEdges[loop]
        w=1
        for i in range(loop+1,len(allEdges)):
            edge2=allEdges[i]
            if set(edge1).issubset(set(edge2)):
                w+=1
        tempE.append(edge1)
        #mapForEdges[loop]="%.3f"%(w/step)
        mapForEdges[loop]=w/step

    Hgrfile.write(str(len(mapForEdges))+" "+"387"+" "+"11\n")
    for edge in mapForEdges:
        Hgrfile.write(str(mapForEdges[edge]))
        for i in range(len(allEdges[edge])):
            Hgrfile.write(" "+allEdges[edge][i])
        Hgrfile.write("\n")

    for i in range(386):
        Hgrfile.write("1\n")
    Hgrfile.write("1")

    Hgrfile.close()


def printNodeCnt():
    Hgrfile=open(outpath+"Hgraph1.hgr","r+")

    for line in Hgrfile.readlines():
        line=line.strip()
        edge=line.split(' ')
        print str(len(edge))

def mainfunc():

    #CreateHgraphFile()
    printNodeCnt()
mainfunc()
