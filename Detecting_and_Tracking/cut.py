import cv2

def capFrame(videoPath, savePath):
    cap = cv2.VideoCapture(videoPath)
    numFrame = 0
    #kk = 0
    while True:

        if cap.grab():
            numFrame += 1
            #kk+=1
            # 每10桢截取一个图片

            if numFrame % 10 == 1:
                #retrieve 解码并返回一个桢
                flag, frame = cap.retrieve()
                if not flag:
                    continue
                else:
                    cv2.imshow('video', frame)
                    newPath = savePath + "\\" + str(int(numFrame/10)) + ".jpg"
                    cv2.imencode('.jpg', frame)[1].tofile(newPath)
                    #file_name = base + 'frame' + str(kk/5)
                    #os.mkdir(file_name)
        #检测到按下Esc时，break（和imshow配合使用）
        if numFrame/10 == 1500:
            break



#capFrame('E:\\codes\\video\\2.mp4', 'E:\\codes\\keras-yolov3-KF-objectTracking-master\\camcut2')
capFrame('I:\\codes\\video\\4.mp4', 'I:\\codes\\keras-yolov3-KF-objectTracking-master\\camcut4')