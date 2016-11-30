# -*- coding:utf-8 -*-
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from trie import Trie
import json
import math

class Dictionary:

    def __init__(self,json_data = None,u_file = "data/udict.txt",b_file = "data/bdict.txt",HMMfile="data/HMM.json"):
        # 字典树
        self.dictTree = Trie()

        # 一元
        self.u_word = {}
        self.wordN = 0

        # 二元
        self.b_word = {}
        self.bwordN = 0

        # Good-Turing 参数
        self.k = 5
        self.c = [0] * self.k

        # HMM字典
        self.HMM_init = {}
        self.HMM_trans = {}
        self.HMM_emit = {}
        self.__loadHMMJson(HMMfile)

        if not json_data:
            self.__loaddic(u_file,b_file)
        else:
            self.__loadjsondata(json_data)
        pass

    def findWord(self,word):
        return self.dictTree.getWrodN(word)[0]

    def getDAG(self,sentence):
        s_len = len(sentence)

        DAG = [([0] * (s_len+1)) for i in range((s_len+1))]

        for i in xrange(s_len+1):
            s_t = self.findWord(sentence[i:])
            if i != s_len:
                DAG[i][i+1] = 1
            for t in s_t:
                DAG[i][i+t] = 1
        return DAG

    def get2GramProb(self,word1,word2):
        key = word1 + ' ' + word2
        n = self.b_word.get(key,0)
        if n < self.k:
            n = self.c[n]
        return float(n) / self.bwordN

    def get2GramProbLog(self,word1,word2):
        key = word1 + ' ' + word2
        n = self.b_word.get(key,0)
        if n < self.k:
            n = self.c[n]
        return math.log(float(n)) - math.log(self.bwordN)

    def writeJsonData(self,filepath):
        data = {}
        data['root'] = self.dictTree.getData()
        data['u_word'] = self.u_word
        data['wordN'] = self.wordN
        data['b_word'] = self.b_word
        data['bwordN'] = self.bwordN
        data['K'] = self.k
        data['C'] = self.c

        print "writting json file..."
        fp = open(filepath,'a+')
        fp.write(json.dumps(data))
        fp.close()


    def __loadjsondata(self,json_file):
        # loading json file
        print "loading Json file..."
        jsonfp = open(json_file)
        jstr = jsonfp.read()
        data = json.loads(jstr)

        self.dictTree.setData(data['root'])

        self.u_word = data['u_word']
        self.wordN = data['wordN']

        self.b_word = data['b_word']
        self.bwordN = data['bwordN']

        self.c = data['C']
        self.k = data['K']

        # # 计算GoodTuring
        # NC = {}
        # for i in self.b_word.values():
        #     if i in NC.keys():
        #         NC[i] += 1
        #     else:
        #         NC[i] = 1
        # NC[0] = self.wordN * self.wordN - self.bwordN
        #
        # for i in xrange(self.k):
        #     self.c[i] = (((i + 1) * float(NC[i + 1]) / float(NC[i])) - \
        #                  (i * (self.k + 1) * NC[self.k + 1] / NC[1])) / \
        #                 (1 - (self.k + 1) * NC[self.k + 1] / NC[1])

        pass

    def __loaddic(self,u_file,b_file):
        # 读一元词典
        print "load 1gram dict..."
        ufp = open(u_file)
        for line in ufp.readlines():
            line = line.strip()
            if line == "":
                continue
            l = line.split('\t')
            # 防止字典错误
            if len(l)<2:
                continue
            word = l[0].decode('utf-8')
            freq = int(l[1])
            self.u_word[word] = freq
            self.wordN += freq
            self.dictTree.addWord(word)
        ufp.close()

        # 读二元词典
        print "load 2gram dict..."
        bfp = open(b_file)
        for line in bfp.readlines():
            line = line.strip()
            if line == "":
                continue
            l = line.split('\t')
            # 防止字典错误
            if len(l)<2:
                continue
            if len(l[0].split(' '))<2:
                continue
            word = l[0].decode('utf-8')
            freq = int(l[1])
            self.b_word[word] = freq
            self.bwordN += freq
        bfp.close()

        print "%d words." % self.wordN

        # 计算GoodTuring
        NC = {}
        for i in self.b_word.values():
            if i in NC.keys():
                 NC[i] += 1
            else:
                NC[i] = 1
        NC[0] = self.wordN * self.wordN - self.bwordN

        for i in xrange(self.k):
            self.c[i] = (((i+1)*float(NC[i+1])/float(NC[i]))-\
                         (i*(self.k+1)*NC[self.k+1]/NC[1]))/\
                        (1-(self.k+1)*NC[self.k+1]/NC[1])
        pass

    def __loadHMMJson(self,file):
        fp = open(file)
        jstr = fp.read()
        data = json.loads(jstr)
        self.HMM_init = data['init']
        self.HMM_trans = data['trans']
        self.HMM_emit = data['emit']
        fp.close()


if __name__ == "__main__":
    # dic = Dictionary(u_file="debug/debugu.txt",b_file="debug/debugb.txt")
    # # print dic.findWord(u"北京邮电大学")
    # x = dic.getDAG(u"北京邮电大学")
    # for i in x:
    #     print i

    dic = Dictionary()
    dic.writeJsonData("data/DicData.json")
    print len(dic.dictTree.getData())
    print len(dic.u_word)
    print dic.wordN
    print len(dic.b_word)
    print dic.bwordN
    print dic.k
    print dic.c
    print ""

    dic = Dictionary(json_data="data/DicData.json")
    print dic.HMM_init
    print dic.HMM_trans
    print dic.HMM_emit['B'][u'你']

    # print len(dic.dictTree.getData())
    # print len(dic.u_word)
    # print dic.wordN
    # print len(dic.b_word)
    # print dic.bwordN
    # print dic.k
    # print dic.c
    # print ""