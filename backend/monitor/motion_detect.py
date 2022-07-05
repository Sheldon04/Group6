import cv2
import time
import math
import torch
from datetime import datetime
import numpy as np

# Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5x, custom
def init_camera(choice):
    if choice == 0:
        video="http://admin:admin@192.168.43.1:8081"   #此处@后的ipv4 地址需要改为app提供的地址
        return cv2.VideoCapture(video)
    else:
        file_path = 'C:\\Users\\ASUS\\Desktop\\data\\road.kux'
        return cv2.VideoCapture(file_path)
    # camera = cv2.VideoCapture(0) # 参数0表示第一个摄像头
    # cv2.namedWindow("camera",1)
    # 开启ip摄像头

if __name__ == '__main__':
    camera = init_camera(1)

    # 判断视频是否打开
    if (camera.isOpened()):
        print('Open')
    else:
        print('摄像头未打开')

    # 测试用,查看视频size
    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('size:'+repr(size))

    fps = 60  # 帧率
    pre_frame = None  # 总是取视频流前一帧做为背景相对下一帧进行比较
    i = 0
    flag = None
    cnt = 0
    bg = cv2.imread('../monitor/data/back.jpg')
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY) # 转灰度图
    bg = cv2.GaussianBlur(bg, (21, 21), 0)

    while True:
        # if cnt % 3 != 0:
        #     cnt += 1
        #     continue
        start = time.time()
        grabbed, frame_lwpCV = camera.read() # 读取视频流
        gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY) # 转灰度图
        gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)

        if not grabbed:
            break
        end = time.time()

        # 运动检测部分
        seconds = end - start
        if seconds < 1.0 / fps:
            time.sleep(1.0 / fps - seconds)
        # gray_lwpCV = cv2.resize(gray_lwpCV, (500, 500))
        # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声
        # 对噪声进行平滑是为了避免在运动和跟踪时将其检测出来

        # 在完成对帧的灰度转换和平滑后，就可计算与背景帧的差异，并得到一个差分图（different map）
        # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
        # 背景移除
        # cv2.convertScaleAbs(avg)
        img_delta = cv2.absdiff(gray_lwpCV, bg)
        thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=4)
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            if cv2.contourArea(c) < 500:
                continue
            # 有移动物体
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(thresh, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.imshow('fgmask', img_delta)
            cv2.imshow('lwpCVWindow', frame_lwpCV)
        pre_frame = gray_lwpCV

        if cv2.waitKey(25) & 0xFF == ord('q'):
            camera.release()
            cv2.destroyAllWindows()
            break
    # When everything done, release the capture
    camera.release()
    cv2.destroyAllWindows()
