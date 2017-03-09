import json
import random

def loadfile(filename):
    fi = open(filename,"r+")
    content = fi.read()
    com = json.loads(content)
    fi.close()
    fi = open("ans.txt","r+")
    fo = open("full.txt","w+")
    content = fi.read()
    lines = content.split("\n")
    for line in lines:
        elems = line.split(" ")
        for elem in elems:
            if elem=="":
                continue
            fullname = com[elem][0]
            fo.write(fullname+",")
        fo.write("\n")
    fo.close()
loadfile("companies.json")
