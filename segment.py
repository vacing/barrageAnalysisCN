
import sys
import re
import jieba
import jieba.posseg as pseg
DICT_PATH='./dict/'
jieba.load_userdict(DICT_PATH + '/xiaowei.commonWord.dict.utf8.priv')
jieba.load_userdict(DICT_PATH + '/barrage.commoWord.dict.utf8')

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
meaninglessSet = readMeaningless(meaninglessPath)
meaninglessSet |= readMeaningless(meaninglessPath_2)

positivePath

filePath = './barrage.temp'
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

        result = ', '.join(getRidInSet(jieba.cut(sentenceSub), meaninglessSet))
        print(result)
        
        #break;



