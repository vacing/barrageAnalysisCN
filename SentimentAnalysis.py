
class SentimentAnalysis:
    def __init__(self, filePath):
        self.mostdict = set()
        self.verydict = set()
        self.moredict = set()
        self.ishdict = set()
        self.insufficientdict = set()
        self.inversedict = set()
        self.posdict = set()
        self.negdict = set()

        dictsAndFiles = [(self.mostdict, 'most.txt'),
                         (self.verydict, 'very.txt'),
                         (self.moredict, 'more.txt'),
                         (self.ishdict, 'ish.txt'),
                         (self.insufficientdict, 'insufficient.txt'),
                         (self.inversedict, 'inverse.txt'),
                         (self.posdict, 'positive.txt'),
                         (self.negdict, 'negative.txt'),
                        ]   
        for df in dictsAndFiles:
            with open(filePath + "/" + df[1], 'rb') as f:
                for line in f.readlines():
                    line = line.strip()
                    df[0].add(line.decode('utf-8'))

    def judgeodd(self, num):
        if (num/2)*2 == num:
            return 'even'
        else:
            return 'odd' 

    def sentimentScore(self, wordList):
        segtmp = wordList
        i = 0 #记录扫描到的词的位置
        a = 0 #记录情感词的位置
        poscount = 0 #积极词的第一次分值
        poscount2 = 0 #积极词反转后的分值
        poscount3 = 0 #积极词的最后分值（包括叹号的分值）
        negcount = 0
        negcount2 = 0
        negcount3 = 0
        for word in segtmp:
            if word in self.posdict: #判断词语是否是情感词
                poscount += 1                
                c = 0 # 记录否定词数量
                for w in segtmp[a:i]:  #扫描情感词前的程度词
                    if w in self.mostdict:
                        poscount *= 4.0
                    elif w in self.verydict:
                        poscount *= 3.0
                    elif w in self.moredict:
                        poscount *= 2.0
                    elif w in self.ishdict:
                        poscount /= 2.0
                    elif w in self.insufficientdict:
                        poscount /= 4.0
                    elif w in self.inversedict:
                        c += 1
                if self.judgeodd(c) == 'odd': #扫描情感词前的否定词数
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i + 1 #情感词的位置变化
            elif word in self.negdict: #消极情感的分析，与上面一致
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    if w in self.mostdict:
                        negcount *= 4.0
                    elif w in self.verydict:
                        negcount *= 3.0
                    elif w in self.moredict:
                        negcount *= 2.0
                    elif w in self.ishdict:
                        negcount /= 2.0
                    elif w in self.insufficientdict:
                        negcount /= 4.0
                    elif w in self.inversedict:
                        d += 1
                if self.judgeodd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1
            elif word == '！' or word == '!': ##判断句子是否有感叹号
                for w2 in segtmp[::-1]: #扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in self.posdict or self.negdict:
                        poscount3 += 2
                        negcount3 += 2
                        break                    
            i += 1 #扫描词位置前移

        # 以下是防止出现负数的情况
        pos_count = 0
        neg_count = 0
        if poscount3 < 0 and negcount3 > 0:
            neg_count += negcount3 - poscount3
            pos_count = 0
        elif negcount3 < 0 and poscount3 > 0:
            pos_count = poscount3 - negcount3
            neg_count = 0
        elif poscount3 < 0 and negcount3 < 0:
            neg_count = -poscount3
            pos_count = -negcount3
        else:
            pos_count = poscount3
            neg_count = negcount3
            
        return (pos_count, neg_count)



