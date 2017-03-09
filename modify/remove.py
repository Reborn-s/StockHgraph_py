alldic = {}
def GetCnt(filename):
    fi = open(filename,"r+")
    content = fi.read()
    lines = content.split("\n")
    for line in lines:
        elems = line.split(",")
        for elem in elems:
            if elem in alldic:
                alldic[elem] += 1
            else:
                alldic[elem] = 1
    tmpdic = sorted(alldic.iteritems(),key=lambda d:d[1],reverse=False)
    fo = open(filename+"o.txt","w+")
    for item in tmpdic:
        fo.write(item[0]+" "+str(item[1])+"\n")
    fo.close()
GetCnt("m2.txt")
