# -*- coding: utf-8 -*-
#from numpy import *
import itertools
 
support_dic = {}
 
'''
#����ԭʼ���ݣ����ڲ���
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
'''
#��ȡ�������ݿ��е�һ��Ԫ��
def createC1(dataSet):
    C1 = set([])
    for item in dataSet:
        C1 = C1.union(set(item))
    return [frozenset([i]) for i in C1]
 
#�������ݿ⣨dataset�� �� �ɵ�K-1�������ںϺ�õ��ĵ�K�����ݼ���Ck����
#����С֧�ֶȣ�minSupport)�� Ck ���ˣ��õ���k��ʣ�µ����ݼ��ϣ�Lk��
def getLk(dataset, Ck, minSupport):
    global support_dic
    print "getLK"
    Lk = {}
    #����Ck��ÿ��Ԫ�������ݿ��г��ִ���
    for item in dataset:
        for Ci in Ck:
            if Ci.issubset(item):
                if not Ci in Lk:
                    Lk[Ci] = 1
                else:
                    Lk[Ci] += 1
    #����С֧�ֶȹ���
    Lk_return = []
    for Li in Lk:
        support_Li = Lk[Li] / float(len(dataSet))
        if support_Li >= minSupport:
            print Li
            Lk_return.append(Li)
            support_dic[Li] = support_Li
    return Lk_return
 
#������֧�ֶȹ��˺�ĵ�K�����ݼ��ϣ�Lk���ں�
#�õ���k+1��ԭʼ����Ck1
def genLk1(Lk):
    print "getLK1"
    Ck1 = []
    for i in range(len(Lk) - 1):
        for j in range(i + 1, len(Lk)):
            if sorted(list(Lk[i]))[0:-1] == sorted(list(Lk[j]))[0:-1]:
                Ck1.append(Lk[i] | Lk[j])
    return Ck1
 
#�������ж��׼����ϵ�Ƶ�����
def genItem(freqSet, support_dic):
    for i in range(1, len(freqSet)):
        for freItem in freqSet[i]:
            genRule(freItem)
#����һ��Ƶ������ݡ����Ŷȡ����ɹ���
#�����˵ݹ飬�Թ��������м�֦
def genRule(Item, minConf=0.5):
    if len(Item) >= 2:
        for element in itertools.combinations(list(Item), 1):
            if support_dic[Item] / float(support_dic[Item - frozenset(element)]) >= minConf:
                print str([Item - frozenset(element)]) + "----->" + str(element)
                print support_dic[Item] / float(support_dic[Item - frozenset(element)])
                genRule(Item - frozenset(element))

def loadDataSet():
    transactions = []
    f = open("m3.txt","r+")
    for line in f.readlines():
        line = line.strip()
        tokens = line.split(' ')
        if len(tokens) > 0:
            transaction = []
            for token in tokens:
                if len(token)>0:
                    transaction.append(int(token))
            transactions.append(transaction) 
    print "start build...",len(transactions)
    f.close()
    return transactions

#������
if __name__ == '__main__':
    dataSet = loadDataSet()
    result_list = []
    Ck = createC1(dataSet)
    #ѭ������Ƶ����ϣ�ֱ�������ռ�
    k = 0
    while True:
        k += 1
        #print k,len(Ck)
        Lk = getLk(dataSet, Ck, 0.03)
        if not Lk:
            break
        result_list.append(Lk)
        Ck = genLk1(Lk)
        if not Ck:
            break

    #���Ƶ����䡰֧�ֶȡ�
    fo = open("f.txt","w+")
    print "start output..."
    #print support_dic
    for item in support_dic:
        if len(item)>1:
            w = int(support_dic[item]*len(dataSet))
            fo.write(str(w)+" ")
            for elem in item:
                fo.write(str(elem)+" ")
            fo.write("\n")
    fo.close()
    #�������
    #genItem(result_list, support_dic)
