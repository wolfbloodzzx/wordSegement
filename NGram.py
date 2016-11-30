# -*- coding:utf-8 -*-
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from dictionary import Dictionary
import math
import Hmm


class Segment:

    def __init__(self,jsonData=None):
        biaodianstr = u"： 。 ；  ， ： “ ”（ ） 、 ？ 《 》 "
        if not jsonData:
            self.dict = Dictionary()
        else:
            self.dict = Dictionary(json_data=jsonData)

    # 计算DAG的最大概率路径
    def maxProbPath(self,sentence,DAG):
        sent_len = len(sentence)
        # dp矩阵
        dp = []
        for i in xrange(sent_len+1):
            dp.append({})
        dp[0]['prob'] = 0
        dp[0]['word'] = '<s>'
        dp[0]['prenode'] = -1
        for i in range(1,sent_len+1):
            prelist = list(x[i] for x in DAG)
            dp[i]['prob'] = None
            for j in xrange(len(prelist)):
                if prelist[j] == 1:
                    prob = dp[j]['prob']+self.dict.get2GramProbLog(dp[j]['word'],sentence[j:i])
                    if dp[i]['prob'] == None or (dp[i]['prob'] != None and prob > dp[i]['prob']):
                        dp[i]['prob'] = prob
                        dp[i]['word'] = sentence[j:i]
                        dp[i]['prenode'] = j
        result_list = []
        node = sent_len
        while node != -1:
            result_list.append(node)
            node = dp[node]['prenode']
        result_list.reverse()
        return result_list
    # HMM分词
    def HMM(self,oblist):
        s = ''
        for i in oblist:
            s+=i
        return s
        pass

    def cut(self,sentence,HMM=False):
        # 切割整句
        mat = re.compile(u"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+")
        result = ''
        s = 0
        for i in xrange(len(sentence)+1):
            if i == len(sentence) or mat.match(sentence[i]):
                subsentence = " " + sentence[s:i]
                s = i+1
                if subsentence == "":
                    if i != len(sentence):
                        result += sentence[i]
                    continue
                DAG = self.dict.getDAG(subsentence)
                path = self.maxProbPath(subsentence,DAG)

                if not HMM:
                    for p in xrange(len(path)-1):
                        if subsentence[path[p]:path[p + 1]].strip() != "":
                            result += subsentence[path[p]:path[p+1]] + " "
                    result = result.strip()
                else:
                    temp = []
                    for p in xrange(len(path)-1):
                        if subsentence[path[p]:path[p+1]].strip() != "":
                            temp.append(subsentence[path[p]:path[p+1]])
                    ss = ''
                    for t in xrange(len(temp)):
                        if len(temp[t]) != 1:
                            if len(ss) == 1:
                                result += (ss + ' ')
                                ss = ''
                            elif len(ss) == 0:
                                pass
                            else:
                                result += (Hmm.HMMCut(ss) + ' ')
                                ss = ''
                            result += (temp[t] + ' ')
                        else:
                            ss += temp[t]
                    if len(ss) > 0:
                        if len(ss) == 1:
                            result += (ss + ' ')
                        else:
                            result += (Hmm.HMMCut(ss) + ' ')
                    result = result.strip()

                if i != len(sentence):
                    result += " " + sentence[i] + " "
        return result.strip()

if __name__ == "__main__":
    s = Segment(jsonData="data/DicData.json")
    # s = Segment()
    print s.cut(u"从电脑学习班的普及到教育软件的火爆，从中文打字机的风靡到中文学习机的商业奇迹，细窥其中的奥妙，有的并非靠技术取胜，而是更多地适应了中国用户的文化习惯和消费心理。", HMM=True)
    print s.cut(u"从电脑学习班的普及到教育软件的火爆，从中文打字机的风靡到中文学习机的商业奇迹，细窥其中的奥妙，有的并非靠技术取胜，而是更多地适应了中国用户的文化习惯和消费心理。")

    # print s.cut(u"我觉得这个事情你应该咨询咨询王之刚老师",HMM=True)
    # print s.cut(u"我觉得这个事情你应该咨询咨询王之刚老师")
    # print s.cut(u"习近平祝贺古特雷斯出任下届联合国秘书长",HMM=True)
    # print s.cut(u"习近平祝贺古特雷斯出任下届联合国秘书长")
    # print s.cut(u"习近平主席出席联合国成立70周年系列峰会期间指出中国将全力支持联合国工作",HMM=True)
    # print s.cut(u"习近平主席出席联合国成立70周年系列峰会期间指出中国将全力支持联合国工作")
    # print s.cut(u"古特雷斯感谢中方愿对其履行联合国秘书长职责给予宝贵支持",HMM=True)
    # print s.cut(u"古特雷斯感谢中方愿对其履行联合国秘书长职责给予宝贵支持")
    # print s.cut(u"海运业雄踞全球之首，按吨位计占世界总数的１７％。", HMM=True)
    # print s.cut(u"海运业雄踞全球之首，按吨位计占世界总数的１７％。")
