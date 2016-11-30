# -*- coding:utf-8 -*-
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Trie:

    def __init__(self):
        self.root = {}
        pass

    def addWord(self,word):
        p = self.root
        for i in word:
            if i in p.keys():
                p = p[i]
            else:
                p[i] = {}
                p[i]['flag'] = False
                p = p[i]
        p['flag'] = True
        pass

    def isContain(self,word):
        p = self.root
        for i in word:
            if i in p.keys():
                p = p[i]
            else:
                return False
        if p['flag']:
            return True
        else:
            return False

    def getWrodN(self,word):
        N = []
        p = self.root
        flag = True
        for i in range(0,len(word)):
            c = word[i]
            if c in p.keys():
                p = p[c]
                if p['flag']:
                    N.append(i+1)
            else:
                flag = False
                break
        return N,flag
    def getData(self):
        return self.root
    def setData(self,root):
        self.root = root

if __name__ == "__main__":
    t = Trie()
    t.addWord("abcd")
    t.addWord("abc")
    t.addWord("ab")
    t.addWord('baa')
    import json
    print json.dumps(t.getData())
    a = Trie()
    a.setData(t.getData())
    print a.isContain("a")
    print a.isContain('baa')
