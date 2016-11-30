# -*- coding:utf-8 -*-
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from NGram import Segment
import codecs

if __name__ == "__main__":
    seg = Segment()
    fp = open("D:/UserDocuments/Desktop/icwb2-data/testing/msr_test.utf8")
    outp =  codecs.open("D:/UserDocuments/Desktop/icwb2-data/outtest.utf8","a+","utf-8",)
    hmmp = codecs.open("D:/UserDocuments/Desktop/icwb2-data/outtest_hmm.utf8", "a+", "utf-8")
    ans = 0

    outstr = ""
    hmmout = ''
    for i in fp.readlines():
        line = i.strip().decode('utf-8')
        out_line = seg.cut(line)
        out_line = out_line.replace(" ","  ")
        # outp.write(out_line+'\n')
        outstr += (out_line + '\n')

        hmm_line = seg.cut(line,HMM=True)
        hmm_line = hmm_line.replace(" ","  ")
        # hmmp.write(hmm_line+'\n')
        hmmout += (hmm_line + '\n')
        ans += 1
        if ans % 100 == 0:
            print ans
    outp.write(outstr)
    hmmp.write(hmmout)
    outp.close()
    hmmp.close()
    fp.close()