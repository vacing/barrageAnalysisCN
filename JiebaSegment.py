import sys
import re
import jieba
import jieba.posseg as pseg

import SentimentAnalysis as localsa
from LocalTool import BarrageTool

DICT_PATH='/data/barragePriv/dict/'
jieba.load_userdict(DICT_PATH + '/common.jieba.complement.priv')
jieba.load_userdict(DICT_PATH + '/barrage.commoWord.dict.utf8')
jieba.load_userdict(DICT_PATH + '/sentimentCN/negative.txt')
jieba.load_userdict(DICT_PATH + '/barrage.negative.dict.utf8')
jieba.load_userdict(DICT_PATH + '/sentimentCN/positive.txt')
jieba.load_userdict(DICT_PATH + '/barrage.positive.dict.utf8')

def jiegSeg(sentence):
    segResult = list(jieba.cut(sentence))
    return segResult

def readMeaningless(filePath):
    meaninglessSet = set()
    with open(filePath, 'rb') as f:
        for line in f.readlines():
            line = line.strip()
            meaninglessSet.add(line.decode('utf-8'))
    return meaninglessSet

def getRidInSet(words, wordsSet):
    newWords=[]
    for word in words:
        if word in wordsSet:
            continue
        newWords.append(word)
    return newWords

meaninglessPath = DICT_PATH + "/xiaowei.meaningless.dict.utf8.priv"
meaninglessPath_2 = DICT_PATH + "/barrage.meaningless.dict.utf8"
meaninglessSet = set()
# meaninglessSet = readMeaningless(meaninglessPath)
# meaninglessSet |= readMeaningless(meaninglessPath_2)

localbt = BarrageTool(DICT_PATH + '/barrage.filter.sent.utf8')

def fileSeg(filePath, segPath, inlPath, labelStr):
    lineNum = 0
    with open(filePath, 'rb') as f:
        for line in f.readlines():
            lineNum += 1
            if lineNum % 10000 == 0:
                print("LINE=" + str(lineNum), file=sys.stderr)
            try:
                sentence = line.decode('utf-8').strip()
            except:
                print('[ERROR] line:' + str(lineNum), file=sys.stderr)

            sentenceTmp = sentence
            if not localbt.isValidSent(sentenceTmp):
                with open(inlPath, 'a') as f:
                    f.write('[Invalid]' + sentenceTmp + "\n")
                continue

            sentenceTmp = re.sub('[\[\]]', '"', sentenceTmp)   # 
            # with open(segPath, 'a') as f:
            #     f.write(sentenceTmp + "#"*4)

            result = ' '.join(jieba.cut(sentence))
            with open(segPath, 'a') as f:
                f.write(labelStr + " " + result + "\n")

def emotionDetect(filePath, outPath):
    sa = localsa.SentimentAnalysis(DICT_PATH)
    lineNum = 0
    with open(filePath, 'rb') as f:
        for line in f.readlines():
            lineNum += 1
            if lineNum % 10000 == 0:
                print("LINE=" + str(lineNum), file=sys.stderr)
            try:
                sentence = line.decode('utf-8').strip()
            except:
                print('[ERROR] line:' + str(lineNum), file=sys.stderr)

            sentenceTmp = sentence
            sentence = re.sub('\W', ' ', sentence).strip()   # 替换掉非文字
            if not localbt.isValidSent(sentence):
                print('[Invalid]' + sentenceTmp)
                continue

            sentenceTmp = re.sub('[\[\]]', '"', sentenceTmp)   
            with open(outPath, 'a') as f:
                f.write("[" + sentenceTmp + "]" + ",")

            segResult = list(jieba.cut(sentence))
            score = sa.sentimentScore(segResult)
            flag = "__POS__" if score[0] > score[1] else \
                   ("__NEG__" if score[0] < score[1] else "__EQU__")
            with open(outPath, 'a') as f:
                f.write('[' + str(score[0]) + ', ' + str(score[1]) + ", " + flag + "]" + ",")
                result = ', '.join(getRidInSet(segResult, meaninglessSet))
                f.write(result + '\n')

if __name__ == '__main__':

    # ----- emotion detection ---------
    filePath = './temp/origin.log.0612.temp'
    outPath = './temp/emot.log.0612.temp'
    with open(outPath, 'w') as f:
        f.write("");
    emotionDetect(filePath, outPath)
    

    # --------------- segment ----------------------
    #tmpPath = './label/'
    # filePath =  './label/positive.label'
    # segPath =  tmpPath + '/seg.positive.temp'
    # inlPath =  tmpPath + '/seg.positive.invalid.temp'
    # labStr = 'pos'

    # filePath =  './label/negtive.label'
    # segPath =  tmpPath + '/seg.negtive.temp'
    # inlPath =  tmpPath + '/seg.negtive.invalid.temp'
    # labStr = 'neg'

    # with open(segPath, 'w') as f:
    #     f.write("");
    # with open(inlPath, 'w') as f:
    #     f.write("");
    # fileSeg(filePath, segPath, inlPath, labStr)


