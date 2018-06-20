import os
import sys
import re

from BarrageTool import BarrageTool

# filePath = 'temp'
# filePath = './highlightClips.log'

localbt = BarrageTool('./dict/barrage.filter.sent.utf8')

tmpPath = './temp/'

filePath =  './origin.2018-06-12.log'
logPath =   tmpPath + '/origin.log.0612.temp'
subPath =   tmpPath + '/origin.sub.0612.temp'
inlPath =   tmpPath + '/origin.invalid.0612.temp'

# filePath =  './origin.server.log'
# logPath =   tmpPath + '/origin.log.server.temp'
# subPath =   tmpPath + '/origin.sub.server.temp'
# inlPath =   tmpPath + '/origin.invalid.server.temp'
with open(logPath, 'w') as f:
    f.write("");
with open(subPath, 'w') as f:
    f.write("");
with open(inlPath, 'w') as f:
    f.write("");

lineNum = 0
maxLine = False
barrageReStr = r'[0-9\]: \/]+room\[[0-9]+\] uid\([0-9]+\).*\]: (.*)$'
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
            sent = mat.groups(0)[0]
            sentBefore = sent
            sent = localbt.sentPreProcess(sent)
            if not sentBefore == sent:
                with open(subPath, 'a') as f:
                    f.write("[Substitue][" + sentBefore + "][" + sent + "]" + "\n")
            if localbt.isValidSent(sent):
                with open(logPath, 'a') as f:
                    f.write(sent + "\n");
            else:
                with open(inlPath, 'a') as f:
                    f.write('[Invalid]' + mat.groups(0)[0] + "\n")
        else:
            print('[Empty] line:' + str(lineNum) + ", [" + line + "]", file=sys.stderr)




