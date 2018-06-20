#-- encoding:utf-8 --
import sys
import re
import jieba
import jieba.posseg as pseg

import SentimentAnalysis as localsa
import BarrageTool as localbt


DICT_PATH='./dict/'
jieba.load_userdict(DICT_PATH + '/xiaowei.commonWord.dict.utf8.priv')
jieba.load_userdict(DICT_PATH + '/barrage.commoWord.dict.utf8')
jieba.load_userdict(DICT_PATH + '/sentimentCN/negative.txt')
jieba.load_userdict(DICT_PATH + '/sentimentCN/positive.txt')

def fileSeg(filePath):
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
            sentence = re.sub('[\[\]]', '"', sentence)   # 替换掉非文字
            print("[" + sentence + "]", end=', ')

            sentenceSub = re.sub('\W', '', sentence)   # 替换掉非文字
            if len(sentenceSub) == 0:
                # TODO
                # print(str(lineNum) + ":" + sentence, file=sys.stderr)
                continue;

            result = ', '.join(localbt.getRidInSet(jieba.cut(sentenceSub), meaninglessSet))
            print(result)


meaninglessPath = DICT_PATH + "/xiaowei.meaningless.dict.utf8.priv"
meaninglessPath_2 = DICT_PATH + "/barrage.meaningless.dict.utf8"
meaninglessSet = set()
# meaninglessSet = localbt.readWordsToSet(meaninglessPath)
# meaninglessSet |= localbt.readWordsToSet(meaninglessPath_2)
meaninglessSet |= localbt.readWordsToSet(DICT_PATH + '/xiaowei.stopwords.dict.utf8')
meaninglessSent = set()
meaninglessSent = localbt.readWordsToSet(DICT_PATH + '/barrage.filter.sent.utf8')

sa = localsa.SentimentAnalysis(DICT_PATH)

filePath = './longbarrage.temp'
# filePath = './barrage.temp'
lineNum = 0
with open(filePath, 'rb') as f:
    for line in f.readlines():
        lineNum += 1
        if lineNum % 10000 == 0:
            print("LINE=" + str(lineNum), file=sys.stderr)

        try:
            sentence = line.decode('utf-8').strip()
            if sentence in meaninglessSent: # filter meaningless sentence
                continue
        except:
            print('[ERROR] line:' + str(lineNum), file=sys.stderr)
        sentenceTmp = re.sub('[\[\]]', '"', sentence)   # 替换掉非文字
        # print("[" + sentenceTmp + "]", end=', ')

        sentence = re.sub('\W', ' ', sentence).strip()   # 替换掉非文字
        if not localbt.isValidSent(sentence):
            continue
        segResult = list(jieba.cut(sentence))
        result = ' '.join(localbt.getRidInSet(segResult, meaninglessSet))
        if not result:
            continue
        print(result)
        
        # break;



