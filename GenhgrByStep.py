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


def CreateHgraphByStep(newComMap,listSet,edgeSets,hgr,cnt):
    for edge in newComMap:
        if newComMap[edge].count(1)==0 and newComMap[edge].count(-1)==0:
            return

    same = []
    for i in range(len(listSet)):
        for edge in newComMap:
            j=0
            if edge.find(str(i))<0:
                same=list(set(listSet[i][1])&set(newComMap[edge]))
                if (len(same)-same.count(0))>=step:
                    for k in range(len(listSet[i][1])):
                        if not (listSet[i][1][k] == listSet[j][1][k] and (
                            listSet[i][1][k] == 1 or listSet[i][1][k] == -1)):
                            newComSet[k] = 0
                        else:
                            newComSet[k] = listSet[i][1][k]
                    hedge +=1
                    newComMap[edge+str(i)]=newComSet
                    for j in range(len(edgeSets)):
                        if list(edge)==edgeSets[j]:
                            edgeSets[j].append(i)
                    WriteEdge(edgeSets[j],hgr)

    cnt+=1
    print "edge nodes:",cnt
    CreateHgraphByStep(newComMap,listSet,edgeSets,hgr,cnt)

def mainfunc():
    CreateHgraphByStep()