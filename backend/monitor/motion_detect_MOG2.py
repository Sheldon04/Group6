import base64
import threading

import cv2
import time
from datetime import datetime
from time import time, sleep
import os
import torch
import pinyin

# 使用MOG2模型进行移动物体标注更稳定，但是易出现噪点（如当场景中大量移动物体移出场景时）
# 使用固定背景进行背景减除在上述场景下不会出现噪点，但是需要定期更新背景图
from cv2 import CAP_FFMPEG

from monitor.my_thread import Invasion_Record_Saver


class Detector():
    def __init__(self, choice, model=None, known_face_encodings=None, admin_levels_names=None):
        # threading.Thread.__init__(self)
        print('init detector')
        self.conf = {'save_path': './video/', 'min_motion_frames': 30, 'enable_save_img': True, 'min_static_frame': 30}
        self.video_writer = None
        # 使用ip摄像头
        if choice == 0:
            # video="http://admin:admin@192.168.43.1:8081"   #此处@后的ipv4 地址需要改为app提供的地址
            video = "http://admin:123456@10.168.30.160:8081"
            self.camera = cv2.VideoCapture(video)
            self.camera.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        # 使用本地视频文件（测试用）
        elif choice == 1:
            # file_path = 'C:\\Users\\ASUS\\Desktop\\data\\road.kux'
            # file_path = 'C:\\Users\\ASUS\\Desktop\\face_recognition\\unknown\\hall2_mid.mp4'
            file_path = 'C:\\Users\\ASUS\\Desktop\\face_recognition\\unknown\\known.mp4'
            # file_path = 'C:\\Users\\ASUS\\Desktop\\data\\example video.avi'
            self.camera = cv2.VideoCapture(file_path, CAP_FFMPEG)
        # 使用rtmp转发服务器读取视频流
        else:
            # file_path = 'http://47.106.148.74:80/tv_file/test.m3u8'
            file_path = 'rtmp://47.106.148.74:1935/tv_file/test'
            # file_path = 'C:\\Users\\ASUS\\Desktop\\data\\example video.avi'
            self.camera = cv2.VideoCapture(file_path, CAP_FFMPEG)

        # 场景的静态背景，用于计算差分图（run1()）
        # self.bg = cv2.imread('./monitor/data/back.jpg')
        # self.bg = cv2.cvtColor(self.bg, cv2.COLOR_BGR2GRAY)  # 转灰度图
        # self.bg = cv2.GaussianBlur(self.bg, (21, 21), 0)
        # Model
        # self.yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom
        self.yolo = model  # or yolov5m, yolov5l, yolov5x, custom
        self.known_face_encodings = known_face_encodings
        self.admin_levels_names = admin_levels_names

        # 判断视频是否打开
        if self.camera.isOpened():
            print('camera opened')
        else:
            print('摄像头未打开')

    # 使用MOG2模型进行背景减除
    def get_fgmask(self, frame):
        fgmask = self.fgbg.apply(frame)
        # 进行形态学开运算，即先腐蚀，再膨胀，以去除噪声
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
        # fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)
        # 再进行一次膨胀，扩大高亮区域（移动物体）
        fgmask = cv2.dilate(fgmask, None, iterations=2)
        return fgmask

    # 停止记录入侵视频
    def stop_video(self, _date, _time):
        if not self.video_writer is None:
            self.video_writer.release()
            self.video_writer = None
            t = Invasion_Record_Saver(self.known_face_encodings, self.admin_levels_names, self.yolo, _date, _time)
            t.start()


    # 开始记录入侵视频
    def start_video(self, size, time):
        if self.video_writer == None:
            print('invade start')
            os.mkdir('./media/screen_shots/' + time)
            self.video_writer = cv2.VideoWriter('./monitor/video/'
                                                + time + '.avi',
                                                cv2.VideoWriter_fourcc(*'XVID'), 20.0, size, True)

    def run2(self):
        print('run')
        # 测试用,查看视频size
        size = (1280, 720)

        is_first_invade = True  # 一次入侵中，是否第一次被记录，用于判断入侵开始时间
        is_invade = False  # 是否有入侵
        invade_frame_cnt = 0
        static_frame_cnt = 0
        invasion_date = None
        invasion_time = None
        fps = 10  # 直播流帧率
        maxDelay = 6  # 最大容许延时
        startTime = time()  # 开始时间
        frames = 0
        store = None
        pre_frame = None
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
        size = (width, height)
        print(size)
        while True:
            return_flag = False

            frames += 1
            # try:
            # grabbed, frame_lwpCV = self.camera.read()  # 读取视频流
            #     if not grabbed:
            #         continue
            #     # 延时小于最大容许延时才进行识别
            #     if frames <= (time() - startTime - maxDelay) * fps:
            #         for index, item in store.iterrows():
            #             cv2.rectangle(frame_lwpCV, (item['xmin'], item['ymin']), (item['xmax'], item['ymax']), (255, 255, 0), 2)
            #             cv2.putText(frame_lwpCV, str(item['name']), (item['xmin'] + 6, item['ymax'] - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
            #         yield frame_lwpCV
            # frame_lwpCV = cv2.resize(frame_lwpCV, size)
            # except:
            #     continue
            #
            grabbed, frame_lwpCV = self.camera.read()  # 读取视频流
            if not grabbed:
                if self.video_writer != None:
                    self.video_writer.write(pre_frame)
                continue
            # if pre_frame == None:
            #     pre_frame = frame_lwpCV
            # if not grabbed:
            #     if self.video_writer != None:
            #         self.video_writer.write(frame_lwpCV)
            #     continue
            # frame_lwpCV = cv2.resize(frame_lwpCV, size)
            # yolov5
            video = frame_lwpCV.copy()
            # video = frame_lwpCV[:, :, ::-1]
            # Inference
            results = self.yolo(video)
            store = results.pandas().xyxy[0]
            # 开始录像

            if 0 in list(results.pandas().xyxy[0]['class']):
                static_frame_cnt = 0
                invade_frame_cnt += 1
                if invade_frame_cnt > self.conf['min_motion_frames'] and self.conf[
                    'enable_save_img'] and is_first_invade:
                    now = datetime.now()
                    self.filename = now.strftime("%Y-%m-%d-%H-%M-%S")
                    invasion_date = now.strftime("%Y-%m-%d")
                    invasion_time = now.strftime("%H:%M:%S")
                    self.start_video(size, self.filename)
                    path = './media/screen_shots/' + self.filename + '/0.jpg'
                    print('save picture to: ', path)
                    cv2.imwrite(path, frame_lwpCV)
                    is_first_invade = False
                if invade_frame_cnt > 1000:
                    # self.conf['enable_save_img'] = False
                    self.stop_video(invasion_date, invasion_time)
                    is_first_invade = True
                    invade_frame_cnt = 0
                    print('forced stop')
                    # self.conf['enable_save_img'] = False
            else:
                # 没有移动物体时停止录制视频
                # print('invade stop')
                static_frame_cnt += 1
                if static_frame_cnt > self.conf['min_static_frame']:
                    self.stop_video(invasion_date, invasion_time)
                    is_first_invade = True
                    invade_frame_cnt = 0

            results.render()  # updates results.imgs with boxes and labels

            if self.video_writer != None:
                self.video_writer.write(results.imgs[0])
                if invade_frame_cnt % 40 == 0:
                    path = './media/screen_shots/' + self.filename + '/' + str(int(invade_frame_cnt / 40)) + '.jpg'
                    print('save picture to: ', path)
                    cv2.imwrite(path, frame_lwpCV)

            # 返回移动物体标注后的图像，移动物体数，是否为首次入侵，入侵时间
            yield results.imgs[0]

            pre_frame = results.imgs[0]

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # When everything done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    d = Detector(1)
    for test, mask, is_invade, invade_time, _ in d.run():
        cv2.imshow('test', test)
        retval, buffer = cv2.imencode('.jpg', test)
        pic_str = base64.b64encode(buffer)
