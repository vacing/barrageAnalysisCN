import os
import sys
import re
from collections import Counter

import LocalTool
from LocalTool import BarrageTool
from JiebaSegment import jiegSeg
import SentimentAnalysis as localsa

# filePath = 'temp'
# filePath = './highlightClips.log'
DICT_PATH='./dict/'
wordCount = Counter()
meaninglessPath = DICT_PATH + "/xiaowei.meaningless.dict.utf8.priv"
meaninglessPath_2 = DICT_PATH + "/barrage.meaningless.dict.utf8"
meaninglessSet = set()
meaninglessSet |= LocalTool.readLinesToSet(meaninglessPath)
meaninglessSet |= LocalTool.readLinesToSet(meaninglessPath_2)

sa = localsa.SentimentAnalysis(DICT_PATH)
def sentEmotDetect(sentence):
    segResult = jiegSeg(sentence)
    segResult = LocalTool.getRidInSet(segResult, meaninglessSet)
    wordCount.update(segResult)
    score = sa.sentimentScore(segResult)
    return score

def processFile(localbt, filePath, logPath, subPath, inlPath):
    lineNum = 0
    maxLine = False
    # barrageReStr = r'[0-9\]: \/]+room\[[0-9]+\] uid\([0-9]+\).*\]: (.*)$'
    barrageReStr = r'[0-9\]: \/]+room\[[0-9]+\] uid\([0-9]+\) +event\[[\w ]*\].*\]: (.*)$'
    barrageRe = re.compile(barrageReStr)
    with open(filePath, 'rb') as f:
        for line in f.readlines():
            if maxLine and lineNum > maxLine:
                break;
            lineNum += 1;
            try:
                line = line.decode('utf-8').rstrip()
            except:
                print('[ERROR]:' + str(lineNum), file=sys.stderr)
                continue;
            # print('line: ' + line.decode('utf-8'))
            mat = barrageRe.match(line)
            lineFlag = ''
            if mat is not None:
                sent = mat.groups(0)[0]
                sentBefore = sent
                sent = localbt.sentPreProcess(sent)
                if not sentBefore == sent:
                    lineFlag = '[Substitue]'
                    with open(subPath, 'a') as f:
                        f.write(lineFlag + "[" + sentBefore + "][" + sent + "]" + "\n")
                if localbt.isValidSent(sent):
                    score = sentEmotDetect(sent)
                    flag = "__POS__" if score[0] > score[1] else \
                           ("__NEG__" if score[0] < score[1] else "__EQU__")
                    lineFlag = '[' + str(score[0]) + ', ' + str(score[1]) + ", " + flag + "]"
                else:
                    lineFlag = '[Invalid]'
                    with open(inlPath, 'a') as f:
                        f.write(lineFlag + mat.groups(0)[0] + "\n")
            else:
                lineFlag = '[Empty]'
                print(lineFlag + ':' + str(lineNum) + ", " + line, file=sys.stderr)
                continue

            with open(logPath, 'a') as f:
                f.write(lineFlag + ':' + line + "\n")

def getEventInFile(localbt, filePath):
    eventSet = set()
    lineNum = 0
    maxLine = False
    barrageReStr = r'[0-9\]: \/]+room\[[0-9]+\] uid\([0-9]+\) +event\[([\w ]+)\].*\]: (.*)$'
    barrageRe = re.compile(barrageReStr)
    with open(filePath, 'rb') as f:
        for line in f.readlines():
            if maxLine and lineNum > maxLine:
                break;
            lineNum += 1;
            try:
                line = line.decode('utf-8').rstrip()
            except:
                print('[ERROR] line:' + str(lineNum), file=sys.stderr)
                continue;
            # print('line: ' + line.decode('utf-8'))
            mat = barrageRe.match(line)
            if mat is not None:
                event = mat.groups(0)[0]
                eventSet.add(event)
            else:
                print('[Empty] line:' + str(lineNum) + ", [" + line + "]", file=sys.stderr)

    return eventSet

if __name__ == '__main__':
    localbt = BarrageTool('./dict/barrage.filter.sent.utf8')
    tmpPath = './temp/'

    # filePath =  './origin.2018-06-12.log'
    # logPath =   tmpPath + '/origin.log.0612.temp'
    # subPath =   tmpPath + '/origin.sub.0612.temp'
    # inlPath =   tmpPath + '/origin.invalid.0612.temp'

    # filePath =  './origin.server.log'
    # logPath =   tmpPath + '/origin.log.server.temp'
    # subPath =   tmpPath + '/origin.sub.server.temp'
    # inlPath =   tmpPath + '/origin.invalid.server.temp'

    filePath = 'origin.180620-event/merge_687423.txt'
    logPath =   tmpPath + '/event.180620.log.merge_687423.temp'
    subPath =   tmpPath + '/event.180620.sub.merge_687423.temp'
    inlPath =   tmpPath + '/event.180620.invalid.merge_687423.temp'
    with open(logPath, 'w') as f:
        f.write("");
    with open(subPath, 'w') as f:
        f.write("");
    with open(inlPath, 'w') as f:
        f.write("");

    processFile(localbt, filePath, logPath, subPath, inlPath)
    with open('./tf.temp', 'w') as f:
        commons = wordCount.most_common(1000)
        print(commons)
        for e in [d[0]+":"+str(d[1]) for d in commons]:
            f.write(e + '\n')

    # events = getEventInFile(localbt, filePath)
    # print(events)


