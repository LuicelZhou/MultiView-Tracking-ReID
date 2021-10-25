# -*- coding: utf-8 -*-

import copy
import colorsys
import os, sys, argparse, random
from timeit import default_timer as timer
import cv2
import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.layers import Input
from PIL import Image, ImageFont, ImageDraw

from yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
from yolo3.utils import letterbox_image
from keras.utils import multi_gpu_model
from yolo_matt import YOLO, detect_video
from tqdm import tqdm
from scipy import misc

from objecttracker.KalmanFilterTracker import Tracker  # 加载卡尔曼滤波函数

#data = open("I:/codes/track4new.txt", 'w+')
#data2 = open('I:/codes/box4.txt','w+')
def calc_center(out_boxes, out_classes, out_scores, score_limit=0.5):
    outboxes_filter = []
    for x, y, z in zip(out_boxes, out_classes, out_scores):
        if z > score_limit:
            if y == 0:
                outboxes_filter.append(x)

    centers = []
    number = len(outboxes_filter)
    '''计算中心点！！！！'''
    for box in outboxes_filter:
        top, left, bottom, right = box
        center = np.array([[(left + right) // 2], [(top + bottom) // 2]])
        xb= left
        yb=top
        w=right-left
        h = bottom-top
        centers.append(center)
        #print(',%s,%s,%s,%s'%(int(xb),int(yb),int(w),int(h)),file=data2)
    return centers, number


def get_colors_for_classes(num_classes):
    """Return list of random colors for number of classes given."""
    # Use previously generated colors if num_classes is the same.
    if (hasattr(get_colors_for_classes, "colors") and
            len(get_colors_for_classes.colors) == num_classes):
        return get_colors_for_classes.colors

    hsv_tuples = [(x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(
        map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
            colors))
    # colors = [(255,99,71) if c==(255,0,0) else c for c in colors ]  # 单独修正颜色，可去除
    random.seed(10101)  # Fixed seed for consistent colors across runs.
    random.shuffle(colors)  # Shuffle colors to decorrelate adjacent classes.
    random.seed(None)  # Reset seed to default.
    get_colors_for_classes.colors = colors  # Save colors for future calls.
    return colors


def trackerDetection(tracker, image, centers, number, frame,max_point_distance=30, max_colors=20, track_id_size=0.8):
    '''
        - max_point_distance为两个点之间的欧式距离不能超过30
            - 有多条轨迹,tracker.tracks;
            - 每条轨迹有多个点,tracker.tracks[i].trace
        - max_colors,最大颜色数量
        - track_id_size,每个
    '''
    # track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    #            (0, 255, 255), (255, 0, 255), (255, 127, 255),
    #            (127, 0, 255), (127, 0, 127)]
    n = 0
    track_colors = get_colors_for_classes(max_colors)

    result = np.asarray(image)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(result, str(number), (20, 40), font, 1, (0, 0, 255), 5)  # 左上角，人数计数

    if (len(centers) > 0):
        # Track object using Kalman Filter
        # tracker.Show_ID(centers)
        tracker.Update(centers)

        # For identified object tracks draw tracking line
        # Use various colors to indicate different track_id
        for i in range(len(tracker.tracks)):
            # 多个轨迹
            if (len(tracker.tracks[i].trace) > 1):
                x0, y0 = tracker.tracks[i].trace[-1][0][0], tracker.tracks[i].trace[-1][1][0]
                cv2.putText(result, str(tracker.tracks[i].track_id), (int(x0), int(y0)), font, track_id_size,
                            (255, 255, 255), 4)
                # (image,text,(x,y),font,size,color,粗细)
                for j in range(len(tracker.tracks[i].trace) - 1):
                    # 每条轨迹的每个点
                    # Draw trace line

                    x1 = tracker.tracks[i].trace[j][0][0]
                    y1 = tracker.tracks[i].trace[j][1][0]
                    x2 = tracker.tracks[i].trace[j + 1][0][0]
                    y2 = tracker.tracks[i].trace[j + 1][1][0]
                    list1 = [str(i) for i in tracker.tracks[i].prediction]
                    list2 = list(map(eval,list1))
                    #加上第0帧的初始位置
                    '''if frame ==1:
                        print("0,0,%s,%s,%s" % (tracker.tracks[i].track_id,int(tracker.tracks[i].trace[0][0][0]) ,int(tracker.tracks[i].trace[1][0][0])),file=data)
                    print("%s,%s,%s,%s,%s"%(int(frame/2.5),frame,tracker.tracks[i].track_id,int(float(list2[0][0])),int(float(list2[1][0]))),file=data)'''
                    #print('prediction:', tracker.tracks[i].prediction, 'trace:', tracker.tracks[i].trace)
                    clr = tracker.tracks[i].track_id % 9
                    distance = ((x2 - x1)** 2 + (y2 - y1)**2)**0.5
                    if distance <  max_point_distance:
                        cv2.line(result, (int(x1), int(y1)), (int(x2), int(y2)),
                                 track_colors[clr], 4)
    return tracker, result


if __name__ == '__main__':
    # 加载keras yolov3 voc预训练模型
    yolo_test_args = {
        "model_path": 'I:\\codes\\keras-yolov3-KF-objectTracking-master\\model_data\\yolo.h5',
        "anchors_path": 'I:\\codes\\keras-yolov3-KF-objectTracking-master\\model_data\\yolo_anchors.txt',
        "classes_path": 'I:\\codes\\keras-yolov3-KF-objectTracking-master\\model_data\\coco_classes.txt',
        "score": 0.3,
        "iou": 0.45,
        "model_image_size": (416, 416),
        "gpu_num": 1,
    }

    yolo_test = YOLO(**yolo_test_args)

    '''
    从视频保存成的图像文件中进行解析
        先把视频-> 拆分成图像文件夹，在文件夹中逐帧解析
        
    '''

    #capFrame('D:\\videos\\2.mp4', 'D:\\竞赛代码\\keras-yolov3-KF-objectTracking-master\\image2')
    #capFrame('D:\\videos\\3.mp4', 'D:\\竞赛代码\\keras-yolov3-KF-objectTracking-master\\image3')
    #capFrame('D:\\videos\\4.mp4', 'D:\\竞赛代码\\keras-yolov3-KF-objectTracking-master\\image4')

    base = 'I:/codes/keras-yolov3-KF-objectTracking-master/'
    #os.makedirs(base + 'camera1')
    #base1 = base + 'camera1/'
    #os.makedirs(base + 'camera2')
    base2 = base + 'camera2/'
    #os.makedirs(base + 'camera3')
    #base3 = base + 'camera3/'
    os.makedirs(base + 'camera4')
    base4 = base + 'camera4/'
    i = 0
    n = 1501 #总帧数
    for j in range(n):
        #file_name1 = base1+'frame'+ str(i)
        #file_name2 = base2 + 'frame' + str(i)
        #file_name3 = base3 + 'frame' + str(i)
        file_name4 = base4 + 'frame' + str(i)
        #os.mkdir(file_name1)
        #os.mkdir(file_name2)
        #os.mkdir(file_name3)
        os.mkdir(file_name4)
        i = i + 1

    #裁切视频+建立重识别图片库文件夹

    #开始追踪
    tracker = Tracker(160, 30, 6, 0)
    for n in tqdm(range(n)):  # n为image图片张数
        image = Image.open('I:\\codes\\keras-yolov3-KF-objectTracking-master\\camcut4\\%s.jpg' % n)
        r_image, out_boxes, out_scores, out_classes = yolo_test.detect_image(image,n)
        centers, number = calc_center(out_boxes, out_classes, out_scores, score_limit=0.5)
        tracker, result = trackerDetection(tracker, r_image, centers, number,n)
        misc.imsave('I:\\codes\\keras-yolov3-KF-objectTracking-master\\camdetec4\\%s.jpg' % n, result)
    #file  = open('E:/reid1')
    #file2 = reid(file)











