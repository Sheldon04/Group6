import cv2
import time
import math
from datetime import datetime

# camera = cv2.VideoCapture(0) # 参数0表示第一个摄像头
# cv2.namedWindow("camera",1)
#开启ip摄像头
#video="http://admin:admin@192.168.43.1:8081"   #此处@后的ipv4 地址需要改为app提供的地址
camera =cv2.VideoCapture(0)

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
while True:
    start = time.time()
    grabbed, frame_lwpCV = camera.read() # 读取视频流
    dim = None
    (hh, ww) = frame_lwpCV.shape[:2]
    rr = 500 / float(ww)
    dim = (500, int(hh * rr))
    frame_lwpCV = cv2.resize(frame_lwpCV, dim, interpolation=cv2.INTER_AREA)
    gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY) # 转灰度图
    gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)

    if not grabbed:
        break
    end = time.time()

    # 运动检测部分
    seconds = end - start
    if seconds < 1.5 / fps:
        time.sleep(1.5 / fps - seconds)
    gray_lwpCV = cv2.resize(gray_lwpCV, (500, 500))
    # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
    gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)

    # 在完成对帧的灰度转换和平滑后，就可计算与背景帧的差异，并得到一个差分图（different map）。还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
    if pre_frame is None:
        pre_frame = gray_lwpCV
    else:
        # 背景移除
        img_delta = cv2.absdiff(pre_frame, gray_lwpCV)
        thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow('lwpCVWindow', img_delta)
        for c in contours:
            if cv2.contourArea(c) < 1500:
                continue
            else:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "test"

            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')
            cv2.putText(frame_lwpCV, ts, (10, frame_lwpCV.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        pre_frame = gray_lwpCV
    cv2.imshow('lwpCVWindow', frame_lwpCV)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        camera.release()
        cv2.destroyAllWindows()
        break
# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()