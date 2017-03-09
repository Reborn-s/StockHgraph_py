import json
mapdic = {}
fi = open("m2.txt","r+")
fo1 = open("m3.txt","w+")
fo2 = open("map.txt","w+")
cnt = 0
for line in fi.readlines():
    line = line.strip()
    tokens = line.split(',')
    for token in tokens:
        if token in mapdic:
            fo1.write(str(mapdic[token])+" ")
        else:
            cnt += 1
            mapdic[token] = cnt
            fo1.write(str(mapdic[token])+" ")
            fo2.write(str(cnt)+" "+token+"\n")
    fo1.write("\n")
fi.close()
fo1.close()
fo2.close()
    
