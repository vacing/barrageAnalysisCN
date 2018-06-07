import os
import sys
import re

# filePath = './server.log'
filePath = './highlightClips.log'

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
            print(mat.groups(0)[0])
        else:
            print('[Empty] line:' + str(lineNum) + ", [" + line + "]", file=sys.stderr)




