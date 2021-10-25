import numpy as np
import pandas as pd
import os
import shutil
path1 = 'E:/codes/'
path2 = 'E:/codes/keras-yolov3-KF-objectTracking-master/camera1/'
data = open('E:/reid1.txt','w+')


point = open(path1 + 'track1.txt')
track = point.readlines()
#print(track[0][2:5])

'''n=0
for foldername in os.listdir(path2):
    data = open('D:/detect1/detect1_frame%s.txt' % n, 'w')
    for filename in os.listdir(os.path.join(path2, foldername)):
        print(filename,file=data)
    n+=1'''
def get_detect_frame_name(name):
    idx1 = name.find('e',5)
    idx2 = name.find('_',10)
    if idx1 == idx2:
        return name[idx1+1]
    else:
        return name[idx1+1:idx2]

def get_track_frame_name(track):
    IDX1 = track.find(',', 0)
    IDX2 = track.find(',', IDX1 + 1)
    if IDX1+1 == IDX2-1:
        return track[IDX1+1]
    else:
        return track[IDX1+1:IDX2]

for foldername, subfoldername,filenames in os.walk(path2):
    for filename in filenames:
        print(foldername+ '/' + filename)
        idx1 = filename.find('_', 10) + 2  #第二个下划线位置+2
        idx2 = filename.find('_', 19) - 1 #第三个下划线位置-1
        idx3 = filename.find(',', 9)
        idx4 = filename.find('_',0)   #第一个下划线位置 即id
        #print(idx4-1)
        idx5 = filename.find('n',0)  #person的n的位置
        # print(idx5+1)
        idx6 = filename.find('e',4)   #frame的e的位置
        #print(idx6+1)
        #print(idx1 - 3)
        center_x = int(filename[idx1:idx3] )
        center_y = int(filename[idx3 + 1:idx2])
        if center_x > 1800 or center_y > 900 :
            print(foldername + '/' + filename, file=data)

        min = abs(center_x - int(track[0][2:5])) + abs(center_y - int(track[0][6:9]))

        k = 0
        for i in range(len(track)):
            IDX1 = track[i].find(',', 0)
            IDX2 = track[i].find(',', IDX1+1)
            IDX3 = track[i].find(',', IDX2+1)
            IDX4 = track[i].find(',', IDX3 + 1)
            IDX5 = track[i].find(',', IDX4 + 1)
            IDX6 = track[i].find(',', IDX5 + 1)
            IDX7 = track[i].find(',', IDX6 + 1)
            IDX8 = track[i].find(',', IDX7 + 1)
            if get_detect_frame_name(filename) == get_track_frame_name(track[i]):
            #当图片帧数等于track帧数时
            # 防止匹配到不同帧的人
                min1 = abs(center_x - int(track[i][IDX3+1:IDX4])) + abs(center_y - int(track[i][IDX4+1:IDX5]))
                #print('两者差为：'+ str(min1))
                if min1 <= min:
                    #print("产生了更小的差，更新min，为：" + str(min1))
                    min  = min1
                    k= i
            #print('本轮最匹配的track序号为：%s'%k)
        IDX1 = track[i].find(',', 0)
        IDX2 = track[i].find(',', IDX1 + 1)
        IDX3 = track[i].find(',', IDX2 + 1)
        IDX4 = track[i].find(',', IDX3 + 1)
        IDX5 = track[i].find(',', IDX4 + 1)
        #print(IDX4, IDX1-2)
        '''if IDX4 == IDX1-2:
            if idx6 + 1 == idx1 - 3:
                print('equal all id%s frame%s ' % (track[k][0], filename[idx6 + 1]) + filename[idx4 - 1],
                          filename[idx6 + 1] )
            else:
                print('first equal ' + track[k][0], filename[idx6 + 1:idx1 - 3 + 1] )
        else:
            if idx6 + 1 == idx1 - 3:
                print('second equal ' + track[k][0:IDX1-1], filename[idx6 + 1] )
            else:
                print('not quall ' + track[k][0:IDX1-1], filename[idx6 + 1:idx1 - 3 + 1])'''
        if IDX2+1 == IDX3-1:
            if idx6 + 1 == idx1 - 3:
                shutil.move(foldername + '/' + filename, foldername + '/' + 'id%s_frame%s_(%s,%s)_camera1.jpg' % (track[k][IDX2+1], filename[idx6+1], track[i][IDX3+1:IDX4],track[i][IDX4+1:IDX5]))
            else:
                shutil.move(foldername + '/' + filename, foldername + '/' + 'id%s_frame%s_(%s,%s)_camera1.jpg' % (
                        track[k][IDX2+1], filename[idx6+1:idx1-3+1], track[i][IDX3+1:IDX4],track[i][IDX4+1:IDX5]))
        else:
            if idx6 + 1 == idx1 - 3:
                shutil.move(foldername + '/' + filename, foldername + '/' + 'id%s_frame%s_(%s,%s)_camera1.jpg' % (
                        track[k][IDX2+1:IDX3], filename[idx6 + 1], track[i][IDX3+1:IDX4],track[i][IDX4+1:IDX5]))
            else:
                shutil.move(foldername + '/' + filename, foldername + '/' + 'id%s_frame%s_(%s,%s)_camera1.jpg' % (
                        track[k][IDX2+1:IDX3], filename[idx6+1:idx1-3+1], track[i][IDX3+1:IDX4],track[i][IDX4+1:IDX5])

print('done!')