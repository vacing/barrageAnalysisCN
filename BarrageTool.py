#-- encoding:utf-8 --

import re

class BarrageTool:
    illegalFiltRe = re.compile('\W')

    def __init__(self, filterSentPath=None):
        self.filtSentSet = set()
        if filterSentPath is not None:
            self.filtSentSet = self.readSentFilt(filterSentPath)
            
    def readSentFilt(self, path):
        filtSet = set()
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue
                sear = self.illegalFiltRe.search(line)
                if sear is not None:
                    print('[ERROR] Ignore illegal sentence filter pattern[' + line + ']')
                    continue
                else:
                    regStr = r'^.*' + line + '.*' 
                    filtRe = re.compile(regStr)
                    filtSet.add(filtRe)
        return filtSet

    # 判断是否是有效的句子
    def isValidSent(self, sent):
        sent.strip()
        if len(sent) == 0 or \
            re.match(r'^[0145789a-zA-Z ]*$', sent) or \
            re.match(r'^2*$', sent) or \
            re.match(r'^3*$', sent):
                return False
        else:
            for filtRe in self.filtSentSet:
                if filtRe.match(sent):
                    return False
            return True

        return True

    def sentPreProcess(self, sent):
        sent = sent.lower()
        sent = re.sub('\[emot:[a-z0-9\]]*', '', sent)   # 
        sent = re.sub('[.+]*66[693\+]+[\W]*', '666', sent)   # 
        sent = re.sub('[…\.。]{2,100}[\W]*', '...', sent)   # 
        sent = re.sub('23{3,100}[\W]*', '2333', sent)   # 
        sent = re.sub('[？\?]{2,100}[\W]*', '??', sent)   # 
        sent = re.sub('[呵哈啊或]{2,100}[\W]*', '哈哈哈', sent)   # 
        sent = re.sub('[喵~]{2,100}[\W]*', '喵喵喵', sent)   # 
        sent = re.sub('[汪~]{3,100}[\W]*', '汪汪汪', sent)   #  两眼泪汪汪
        sent = re.sub('[~嘤]{2,100}[\W]*', '嘤嘤嘤', sent)   # 
        sent = re.sub('[~嘟]{2,100}[\W]*', '嘟嘟嘟', sent)   # 
        sent = re.sub('[啦~]{2,100}[\W]*', '啦啦啦', sent)   # 
        sent = re.sub('[呜~]{2,100}[\W]*', '呜呜呜', sent)   # 
        sent = re.sub('[咕~]{2,100}[\W]*', '咕咕咕', sent)   # 
        sent = re.sub('[绿~]{2,100}[\W]*', '绿绿绿', sent)   # 
        sent = re.sub('[大~]{2,100}[\W]*', '大大大', sent)   # 
        sent = re.sub('[干他]{2,100}[\W]*', '干干干', sent)   # 
        sent = re.sub('(((大气)|(大力))(\W))+[\W]*', '大气', sent)   # 
        sent = re.sub('(冷静)+[\W]*', '冷静', sent)   # 
        sent = re.sub('(好听)+[\W]*', '好听', sent)   # 
        sent = re.sub('(加油)+[\W]*', '加油', sent)   # 
        sent = re.sub('(暴击)+[\W]*', '暴击', sent)   # 
        sent = sent.strip()
        return sent

    def readWordsToSet(self, filePath, wordsSet = None):
        if wordsSet is None:
            wordsSet = set()
        with open(filePath, 'rb') as f:
            for line in f.readlines():
                line = line.strip()
                wordsSet.add(line.decode('utf-8'))
        return wordsSet

    def getRidInSet(self, words, wordsSet):
        newWords=[]
        for word in words:
            if word in wordsSet:
                continue
            newWords.append(word)
        return newWords

if __name__ == '__main__':
    bt = BarrageTool()
    sent = '大力 大力 大力 大力 大力 大力 大力....'
    print(bt.sentPreProcess(sent))
    sent = '........'
    print(bt.sentPreProcess(sent))
    sent = 'abc........'
    print(bt.sentPreProcess(sent))
    # print(isValidSent(sent))


