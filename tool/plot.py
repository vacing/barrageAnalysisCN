# -*- coding: utf-8 -*-
#%% 准备工作
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot(pathin, pathout, threshold=500, kmean1=3, kmean2=3):
    #%% 读取数据
    df = []
    f = open(pathin, encoding = 'utf-8')
    while True:
        line = f.readline()
        if not line:
            break
        fields = line.strip().split()
            
        if 'Invalid' in fields[0] or 'Empty' in fields[0]: 
            score = 0
            date0 = fields[0].split(':')[1]
            time0 = fields[1]
            room = fields[2].split('[')[1][:-1]
            
        else:
            cate,date0 = fields[2].split(':')
            if cate == '__POS__]':
                score = 1
            else:
                if cate == '__NEG__]':
                    score = -1
                else:
                    score = 0
            time0 = fields[3]
            room = fields[4].split('[')[1][:-1]
               
        record = [room,date0,time0,score]
        df.append(record)
    df = pd.DataFrame(df)
    df.columns = ['Room','Date','Time','Score']     
    
    
    #%% 整理数据结构
    #### 生成一天中的各秒并合并
    def sec_to_time(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return ("%02d:%02d:%02d" % (h, m, s))
    Room = list(set(df['Room']))
    Room.sort()
    Date = list(set(df['Date']))
    Date.sort()
    Time = [sec_to_time(x)  for x in range(24*60*60)]
    sec = []
    for r in Room:
        for d in Date:
            for t in Time:
                sec.append([r,d,t])
    sec = pd.DataFrame(sec)
    sec.columns = ['Room','Date','Time']
    df2 = pd.merge(df, sec, how = 'right', on = ['Room','Date','Time'])
    
    df2['Count'] = 1-np.isnan(df2['Score'])
    
    Score = list(df2['Score'])
    for i in range(len(Score)):
        if np.isnan(Score[i]):
            Score[i] = 0 
    df2['Score'] = Score
    
    df2 = df2.sort_values(by = ['Room','Date','Time'])
    
    
    #### 生成每分钟的标签
    Time_min = []
    for i in df2.index:
        Time_min.append(df2.loc[i,'Time'][:5])
    df2['Time_min'] = Time_min
    
    Time_10min = []
    for i in df2.index:
        Time_10min.append(df2.loc[i,'Time'][:4]+'0')
    df2['Time_10min'] = Time_10min
    
    
    #### 调整各列顺序
    df2['Count2'] = df2['Count']
    df2['Score2'] = df2['Score']
    del df2['Count']
    del df2['Score']
    df2.columns = ['Room','Date', 'Time', 'Time_min','Time_10min', 'Count','Score']
    
    
    #%% 画出图形
    for r in Room:
        dft = df2[df2['Room'] == r]
        roomt = r
        for d in Date:    
            #### 筛选出高频时段
            dft = df2[df2['Date'] == d]
            if dft.empty:
                continue
            datet = d.replace('/','-')
            df_10min = dft.groupby('Time_10min').sum()['Count']
            temp = []
            for k in range(len(df_10min)):
                if df_10min[k] > threshold:
                    temp.append(df_10min.index[k])
            if not temp:
                continue
            temp.sort()
            dft = dft[dft['Time_10min'] >= temp[0]]
            dft = dft[dft['Time_10min'] <= temp[-1]]
            
            
            #### 聚合数据
            summ = dft.groupby('Time_min').sum()
            df_count = summ['Count']
            df_score = summ['Score']
            
            
            #### 寻找峰值
            mn = df_count.mean()
            pos1 = []
            value1 = []
            pos0 = []
            value0 = []
            for i in range(len(df_count)):
                if df_count[i] > kmean1*mn:
                    pos0.append(i)
                    value0.append(df_count[i])
                else:
                    if pos0:
                        ind = value0.index(max(value0))
                        pos1.append(pos0[ind])
                        value1.append(value0[ind])
                        pos0 = []
                        value0 = []           
            text1 = [df_count.index[i] for i in pos1]
            
            df_score_abs = abs(df_score)
            mn = df_score_abs.mean()
            pos2 = []
            value2 = []
            pos0 = []
            value0 = []
            for i in range(len(df_score_abs)):
                if df_score_abs[i] > kmean2*mn:
                    pos0.append(i)
                    value0.append(df_score[i])
                else:
                    if pos0:
                        ind = value0.index(max(value0))
                        pos2.append(pos0[ind])
                        value2.append(value0[ind])
                        pos0 = []
                        value0 = []           
            text2 = [df_score_abs.index[i] for i in pos2]
            
            
            #### 绘制图形
            pname = 'Plot Count'+' in Room '+roomt+' on '+datet
            plt.figure(figsize = (40,15))
            plt.plot(df_count.index, df_count)
            plt.xticks([])
            plt.tick_params(labelsize=25)
            plt.xlabel('Time',{'size':25})
            plt.ylabel('Count',{'size':25})
            plt.title('Change of Count\n'+'Room '+roomt+' -- '+datet,{'size':40})
            for i in range(len(pos1)):
                plt.text(pos1[i], value1[i], text1[i], fontsize = 20)
            plt.savefig(pathout+'/'+pname+'.png')
            plt.close()
            
            pname = 'Plot Score'+pname[10:] 
            plt.figure(figsize=(40,15))
            plt.plot(df_score.index, df_score)
            plt.xticks([])
            plt.tick_params(labelsize=25)
            plt.xlabel('Time',{'size':25})
            plt.ylabel('Score',{'size':25})
            plt.title('Change of Score\n'+'Room '+roomt+' -- '+datet,{'size':40})
            for i in range(len(pos2)):
                plt.text(pos2[i], value2[i], text2[i], fontsize=20)
            plt.savefig(pathout+'/'+pname+'.png')
            plt.close()
        

#%% 命令行调用接口
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--pathin',  help = '需要作图的数据文件的路径。')
    parser.add_argument('--pathout', help = '存放输出图片的文件夹路径。')
    parser.add_argument('--threshold', type = int, default = 500,
                        help = "作图时，只作出每天中每10分钟弹幕数大于threshold的最早时间和最晚时间之间的图，默认值为500。")
    parser.add_argument('--kmean1', type = float, default =3,
                        help = '在弹幕频数图中，标记弹幕数大于kmean1倍弹幕数均值的尖峰的峰值时刻，默认值为3。')
    parser.add_argument('--kmean2', type = float, default =3,
                        help = '在弹幕情感得分图中，标记情感得分绝对值大于kmean2倍情感得分绝对值的均值的尖峰的峰值时刻，默认值为3。')

    args = parser.parse_args()


    plot(args.pathin, args.pathout, args.threshold, args.kmean1, args.kmean2)    
    




    


