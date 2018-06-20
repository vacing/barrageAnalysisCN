import collections
from collections import Counter

tmpPath = './temp/'
# filePath = tmpPath + '/origin.log.server.temp'
filePath = tmpPath + '/origin.log.0612.temp'

freq = Counter()
freq_up = freq.update
with open(filePath, 'r') as f:
    freq_up([line.strip() for line in f])

sentList = freq.most_common(2000)
with open(tmpPath + "/sent.freq.temp", 'w') as f:
    for (sent, freq) in sentList:
        f.write(str(freq) + ", \t" + sent + "\n")

sentDict = collections.OrderedDict(sorted(dict(sentList).items()))
with open(tmpPath + "/sent.words.temp", 'w') as f:
    for item in sentDict.items():
        f.write("[" + item[0].strip() + "] ,\t" + str(item[1]) + "\n")


