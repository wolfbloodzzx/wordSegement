# wordSegement
自然语言课堂练习，基于2-gram实现的一个最大概率路径分词，不定期更新。
## 使用
### 1.基本使用
NGram模块的Segement类为主要分词模块。

代码示例：
···
# -*- coding:utf-8 -*-
from NGram import Segment
seg = Segment()
print seg.cut(u"我爱北京天安门。")
# output : 我 爱 北京 天安门 。
···
### 2.指定词典
代码默认读取原始字典文件计算一元词和二元词，data文件夹中添加了json文件，其中包含了已统计好的词频等信息，时间更快，可在初始化Segment时进行指定
代码示例：
···
# -*- coding:utf-8 -*-
from NGram import Segment
seg = Segment(jsonData="data/DicData.json")
print seg.cut(u"我爱北京天安门。")
# output : 我 爱 北京 天安门 。
···
### 3.未登录词识别
对未登录词，指定HMM分词
···
# -*- coding:utf-8 -*-
from NGram import Segment
seg = Segment(jsonData="data/DicData.json")
print seg.cut(u"北邮距离北交很近。")
# output ： 北 邮 距离 北 交 很 近 。
print seg.cut(u"北邮距离北交很近。",HMM=True)
# output ： 北邮 距离 北交 很 近 。
···
## 相关说明
程序自带的字典使用了icwb2-data种的msr训练的语料库，对未登录词的概率计算中使用了Good-Turing平滑。对未登录词的识别，程序使用HMM提高识别精度，其中HMM部分借鉴结巴分词的相关代码。
对一个句子的切分主要在Segment.cut()中实现，主要切分流程如下所示：
1. 对与一个待切分的句子，先根据标点，将句子切分为没有标点的短句
2. 针对一个短句，根据其中成词情况建立DAG图
3. 计算DAG图的最大概率路径，依照路径做原始切分
4. 若HMM=False，则回到步骤2直到对每个子句进行切分，否则对其中连续两个以上的单个词进行拼接，使用HMM预测未登录词
5. 输出结果

## 致谢
感谢jieba分词原作者fxsjy，在完成这个作业的过程中收到了很多启发。HMM相关部分本来使用的是自己训练出的模型，但识别精度很低，后续也会针对这部分进行修改。
感谢北京邮电大学王小捷教授，在他的计算语言学的课堂上，我学到了很多知识，虽然也经常翘课睡懒觉……（希望老师不要看到）
这个项目只是实现了一个简单的分词程序，后续会不断进行改进，最后附上fxsiy大神的jieba链接
[结巴分词](https://github.com/fxsjy/jieba)

