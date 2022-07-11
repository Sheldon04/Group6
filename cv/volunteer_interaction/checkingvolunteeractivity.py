# -*- coding: utf-8 -*-
'''
义工是否和老人有互动主程序

用法： 
python checkingvolunteeractivity.py
python checkingvolunteeractivity.py --filename tests/desk_01.mp4
'''
import sys

from oldcare.facial import FaceUtil
from scipy.spatial import distance as dist
from oldcare.utils import fileassistant
from PIL import Image, ImageDraw, ImageFont
import cv2
import time
import os
import imutils
import numpy as np
import argparse
import subprocess
import requests


class CheckingVolunteerActivity:
    def __init__(self, ap_id):
        self.ap_id = ap_id
        self.ap_imagedir = 'images'

        # 传入参数
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-f", "--filename", required=False, default='',
                             help="")
        self.args = vars(self.ap.parse_args())

        # 输入模型
        self.model_path = 'models/face_recognition_hog.pickle'
        self.people_info_path = 'info/people_info.csv'
        self.camera_turned = 0
        # your python path
        self.python_path = '/home/hsy/anaconda3/envs/tensorflow/bin/python'

        # 全局变量
        self.pixel_per_metric = None
        self.input_video = self.args['filename']
        self.output_activity_path = 'supervision/activity'

        # 全局常量
        self.FACE_ACTUAL_WIDTH = 20  # 单位厘米   姑且认为所有人的脸都是相同大小
        self.VIDEO_WIDTH = 640
        self.VIDEO_HEIGHT = 480
        self.ANGLE = 20
        self.ACTUAL_DISTANCE_LIMIT = 100  # cm
        self.details = ''
        self.flag = 0
        self.oid = 0
        self.vid = 0
        self.imgPath = ''

    def checkVolunteer(self):
        # 输入
        # 得到 ID->姓名的map 、 ID->职位类型的map
        id_card_to_name, id_card_to_type = fileassistant.get_people_info(self.people_info_path)
        # 初始化摄像头
        if not self.input_video:
            vs = cv2.VideoCapture(0)
            time.sleep(2)
        else:
            vs = cv2.VideoCapture(self.input_video)

        # 加载模型
        faceutil = FaceUtil(self.model_path)

        print('[INFO] 开始检测义工和老人是否有互动...')
        # 不断循环
        counter = 0
        while True:
            counter += 1
            camera_turned = 0
            # grab the current frame
            (grabbed, frame) = vs.read()

            # if we are viewing a video and we did not grab a frame, then we
            # have reached the end of the video
            if self.input_video and not grabbed:
                break

            if not self.input_video:
                frame = cv2.flip(frame, 1)

            frame = imutils.resize(frame,
                                   width=self.VIDEO_WIDTH,
                                   height=self.VIDEO_HEIGHT)  # 压缩，为了加快识别速度

            face_location_list, names = faceutil.get_face_location_and_name(frame)

            # 得到画面的四分之一位置和四分之三位置，并垂直划线
            one_sixth_image_center = (int(self.VIDEO_WIDTH / 6), int(self.VIDEO_HEIGHT / 6))
            five_sixth_image_center = (int(self.VIDEO_WIDTH / 6 * 5),
                                       int(self.VIDEO_HEIGHT / 6 * 5))

            cv2.line(frame, (one_sixth_image_center[0], 0),
                     (one_sixth_image_center[0], self.VIDEO_HEIGHT),
                     (0, 255, 255), 1)
            cv2.line(frame, (five_sixth_image_center[0], 0),
                     (five_sixth_image_center[0], self.VIDEO_HEIGHT),
                     (0, 255, 255), 1)

            people_type_list = list(set([id_card_to_type[i] for i in names]))

            volunteer_name_direction_dict = {}
            volunteer_centroids = []
            old_people_centroids = []
            old_people_name = []

            # loop over the face bounding boxes
            for ((left, top, right, bottom), name) in zip(face_location_list, names):  # 处理单个人

                person_type = id_card_to_type[name]
                # 将人脸框出来
                rectangle_color = (0, 0, 255)
                if person_type == 'old_people':
                    rectangle_color = (0, 0, 128)
                elif person_type == 'employee':
                    rectangle_color = (255, 0, 0)
                elif person_type == 'volunteer':
                    rectangle_color = (0, 255, 0)
                else:
                    pass
                cv2.rectangle(frame, (left, top), (right, bottom),
                              rectangle_color, 2)

                if 'volunteer' not in people_type_list:  # 如果没有义工，直接跳出本次循环
                    continue

                if person_type == 'volunteer':  # 如果检测到有义工存在

                    # 获取义工id
                    self.vid = name

                    # 获得义工位置
                    volunteer_face_center = (int((right + left) / 2),
                                             int((top + bottom) / 2))
                    volunteer_centroids.append(volunteer_face_center)

                    cv2.circle(frame,
                               (volunteer_face_center[0], volunteer_face_center[1]),
                               8, (255, 0, 0), -1)

                    adjust_direction = ''
                    # face locates too left, servo need to turn right,
                    # so that face turn right as well
                    if volunteer_face_center[0] < one_sixth_image_center[0]:
                        adjust_direction = 'right'
                    elif volunteer_face_center[0] > five_sixth_image_center[0]:
                        adjust_direction = 'left'

                    volunteer_name_direction_dict[name] = adjust_direction

                elif person_type == 'old_people':  # 如果没有发现义工
                    old_people_face_center = (int((right + left) / 2),
                                              int((top + bottom) / 2))
                    old_people_centroids.append(old_people_face_center)
                    old_people_name.append(name)

                    cv2.circle(frame,
                               (old_people_face_center[0], old_people_face_center[1]),
                               4, (0, 255, 0), -1)
                else:
                    pass

                # 人脸识别和表情识别都结束后，把表情和人名写上 (同时处理中文显示问题)
                img_PIL = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(img_PIL)
                final_label = id_card_to_name[name]
                draw.text((left, top - 30), final_label,
                          font=ImageFont.truetype('NotoSansCJK-Black.ttc', 40),
                          fill=(255, 0, 0))  # linux
                # 转换回OpenCV格式
                frame = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)

            # 义工追踪逻辑
            if 'volunteer' in people_type_list:
                volunteer_adjust_direction_list = list(volunteer_name_direction_dict.values())
                if '' in volunteer_adjust_direction_list:  # 有的义工恰好在范围内，所以不需要调整舵机
                    print('%d-有义工恰好在可见范围内，摄像头不需要转动' % (counter))
                else:
                    adjust_direction = volunteer_adjust_direction_list[0]
                    camera_turned = 1
                    print('%d-摄像头需要 turn %s %d 度' % (counter, adjust_direction, self.ANGLE))

            # 在义工和老人之间划线
            if camera_turned == 0:
                for i in volunteer_centroids:
                    for j_index, j in enumerate(old_people_centroids):
                        pixel_distance = dist.euclidean(i, j)
                        face_pixel_width = sum([i[2] - i[0] for i in face_location_list]) / len(face_location_list)
                        pixel_per_metric = face_pixel_width / self.FACE_ACTUAL_WIDTH
                        actual_distance = pixel_distance / pixel_per_metric

                        if actual_distance < self.ACTUAL_DISTANCE_LIMIT:
                            cv2.line(frame, (int(i[0]), int(i[1])),
                                     (int(j[0]), int(j[1])), (255, 0, 255), 2)
                            label = 'distance: %dcm' % (actual_distance)
                            cv2.putText(frame, label, (frame.shape[1] - 150, 30),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (0, 0, 255), 2)

                            current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                         time.localtime(time.time()))
                            event_desc = '%s正在与义工交互' % (id_card_to_name[old_people_name[j_index]])
                            event_location = '房间桌子'
                            print(
                                '[EVENT] %s, 房间桌子, %s 正在与义工交互.' % (
                                    current_time, id_card_to_name[old_people_name[j_index]]))
                            # 交互详情
                            self.details = '[EVENT] %s, 房间桌子, %s 正在与义工交互.' % (
                                current_time, id_card_to_name[old_people_name[j_index]])
                            # 获取老人id
                            self.oid = old_people_name[j_index]

                            cv2.imwrite(
                                os.path.join(self.output_activity_path,
                                             'snapshot_%s.png' % (time.strftime('%Y%m%d_%H%M%S'))), frame)  # snapshot

                            # print("第一", os.path.join(self.output_activity_path,
                            #                          'snapshot_%s.png' % (time.strftime('%Y%m%d_%H%M%S'))))
                            # 获取图片路径并打印查看是否正确
                            self.imgPath = os.getcwd() + "/" + os.path.join(self.output_activity_path,
                                                                            'snapshot_%s.png' % (
                                                                                time.strftime('%Y%m%d_%H%M%S')))
                            print("第二", self.imgPath)
                            # 展示获取的图片
                            # cv2.namedWindow('myPicture', 0)
                            # cv2.resizeWindow('myPicture', 500, 500)
                            # cv2.imshow('myPicture',cv2.imread(self.imgPath))

                            # insert into database
                            command = '%s inserting.py --event_desc %s --event_type 1 --event_location %s --old_people_id %d' % (
                                self.python_path, event_desc, event_location, int(name))
                            p = subprocess.Popen(command, shell=True)

                            # 打印判断id是否正确
                            # print("老人id", self.oid)
                            # print("义工id", self.vid)

                            if self.flag == 0:
                                url = "http://47.106.148.74:8080/api/event/postinteraction"
                                files = {'img': ('face.png', open(self.imgPath, 'rb'), 'image/png', {})}
                                # files = {'img': ('face.png', open('/home/hsy/local/face.png', 'rb'), 'image/png', {})}
                                data = {"cid": "2", "oid": self.oid, "vid": self.vid, "detail": self.details}
                                resp = requests.post(url, data=data, files=files)
                                self.flag = 1
                                print("just sending one time!")
                                print(resp)# resp为200时代表成功

            # show our detected faces along with smiling/not smiling labels
            cv2.imshow("Checking Volunteer's Activities", frame)

            # Press 'ESC' for exiting video
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break

        # cleanup the camera and close any open windows
        vs.release()
        cv2.destroyAllWindows()


def checkingVolunteerActivity():
    if len(sys.argv) == 1:
        CheckingVolunteerActivity("new").checkVolunteer()
    else:
        CheckingVolunteerActivity(sys.argv[1]).checkVolunteer()


if __name__ == '__main__':
    checkingVolunteerActivity()

