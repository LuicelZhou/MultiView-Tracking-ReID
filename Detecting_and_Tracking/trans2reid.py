import pandas as pd
import os
import shutil

path1 = 'E:/codes/'
path2 = 'E:/codes/keras-yolov3-KF-objectTracking-master/camera1/'

data = open('E:/reid1.txt','w+')

'''for foldername, subfoldername,filenames in os.walk(path2):
    for filename in filenames:
        idx1 = filename.find('_', 10) + 2  #第二个下划线位置+2
        idx2 = filename.find('_', 16) - 1 #第三个下划线位置-1
        idx3 = filename.find(',', 9)
        idx4 = filename.find('_',0)   #第一个下划线位置 即id
        #print(idx4-1)
        idx5 = filename.find('n',0)  #person的n的位置
        #print(idx5+1)
        idx6 = filename.find('e',4)   #frame的e的位置
        #print(idx6+1)
        #print(idx1 - 3)
        center_x = int(filename[idx1:idx3] )
        center_y = int(filename[idx3 + 1:idx2])
        #if center_x > 1700 or center_y > 900 :
            #print(foldername + '/' + filename, file=data)'''


point = open(path1 + 'track1.1.txt')
track = point.readlines()
for i in range(len(track)):
    idx = track[i].rfind(',')
    print(idx)
    print(track[i][idx+1:])