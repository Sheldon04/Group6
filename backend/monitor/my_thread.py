import os
import threading
import time

import cv2
import face_recognition
from django.contrib.auth.models import User
from django.core.mail import send_mail

from datamodel.models import invationRecord, segmentation
import djangoProject.settings as settings


# debug
import torch
from datamodel.models import mypicture, WhiteList
import pinyin

# 1. 分析保存的视频，判断入侵区域的级别
# 2. 分析截图，判断入侵者身份
# 3. 根据以上的分析结果，保存入侵信息并发送邮件
class Invasion_Record_Saver(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, known_face_encodings, admin_levels_names, yolo, _date, _time, camera_id=1, area='仓库'):
        threading.Thread.__init__(self)
        self._date = _date
        self._time = _time
        self.invasion_num = -1
        self.area_level = -1
        self.camera_id = camera_id
        self.area = area
        self.known_face_encodings = known_face_encodings
        self.admin_levels_names = admin_levels_names
        self.yolo = yolo

        self.segmentation = [[], [], []]
        seg_list = list(segmentation.objects.values('top','left','width','height', 'level'))
        print(seg_list)
        for seg in seg_list:
            xmin = int(seg['left'])
            ymin = int(seg['top'])
            xmax = int(seg['left']) + int(seg['width'])
            ymax = int(seg['top']) + int(seg['height'])
            self.segmentation[int(seg['level']) - 1].append({'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax})

        print(self.segmentation)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        self.process_video()
        self.process_pic()
        try:
            if self.area_level != 0:
                invationRecord.objects.create(date=self._date, time=self._time, invation_num=self.invasion_num,
                                          level=self.invade_level, camera_id=1, area='厨房')
        except Exception as e:
            print(e)
            print('保存入侵信息失败')

    def process_video(self):
        print('processing video')
        times = self._time.split(':')
        file_path = 'E:\\watchDogs\\djangoProject\\monitor\\video\\' + self._date + '-' + times[0] + '-' + times[1] + '-' + times[2] + '.avi'
        print(file_path)
        camera = cv2.VideoCapture(file_path)
        # 判断视频是否打开
        if not camera.isOpened():
            print('摄像头未打开')
            return
        while camera.isOpened():
            grabbed, frame_lwpCV = camera.read()  # 读取视频流
            # yolov5
            if not grabbed:
                break
            video = frame_lwpCV.copy()
            results = self.yolo(video)

            for index, item in results.pandas().xyxy[0].iterrows():
                if item['class'] == 0:
                    centerX = int((item['xmin'] + item['xmax']) / 2)
                    centerY = int((item['ymin'] + item['ymax']) / 2)
                    for i in range(2, self.area_level, -1):
                        for seg in self.segmentation[i]:
                            if centerX > seg['xmin'] and centerX < seg['xmax'] and centerY > seg['ymin'] and centerY < seg['ymax']:
                                self.area_level = max(i, self.area_level)
                                break

            results.render()  # updates results.imgs with boxes and labels
            for i in range(3):
                for seg in self.segmentation[i]:
                    xmin = seg['xmin']
                    ymin = seg['ymin']
                    xmax = seg['xmax']
                    ymax = seg['ymax']
                    msg = 'area level: ' + str(i + 1) + ' invade: ' + str(self.area_level + 1)
                    cv2.rectangle(results.imgs[0], (xmin, ymin), (xmax, ymax), (i * 60, 255, 0), 2)
                    cv2.putText(results.imgs[0], msg, (xmin + 6, ymax - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

            self.invasion_num = max(self.invasion_num, list(results.pandas().xyxy[0]['class']).count(0))

            cv2.imshow('show', results.imgs[0])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.area_level += 1
        print('final level: ', self.area_level)


    def process_pic(self):
        if self.area_level == 0:
            return
        time.sleep(0.1)
        times = self._time.split(':')
        filename = self._date + '-' + times[0] + '-' + times[1] + '-' + times[2]
        path = 'E:\\watchDogs\\djangoProject\\media\\screen_shots\\' + filename
        print('path ', path)
        file_num = sum([os.path.isfile(path + '/' + listx) for listx in os.listdir(path)])
        print('pic num ', file_num)
        flag = True
        for i in range(0, file_num):
            time.sleep(0.1)
            frame = cv2.imread(path + '\\' + str(i) + '.jpg')
            print('processing ' + str(i) + '.jpg')
            scale = 1
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=2,
                                                             model="cnn")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, known_face_locations=face_locations,
                                                             num_jitters=50)
            face_names = []
            time.sleep(0.1)
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
                # If a match was found in known_face_encodings, just use the first one.
                name = 'Unknown'
                # 员工进入
                if True in matches:
                    first_match_index = matches.index(True)
                    admin_level = int(self.admin_levels_names[first_match_index]['level'])
                    name = self.admin_levels_names[first_match_index]['name']
                    if flag:
                        # 不发邮件，记录入侵级别为1
                        if admin_level > self.area_level:
                            self.invade_level = 1
                            self.send_my_mail(True, name)
                            print(name + '进入，警戒等级1级')
                        # 发邮件，入侵级别为2
                        elif admin_level == self.area_level:
                            self.invade_level = 2
                            self.send_my_mail(True, name)
                            print(name + '进入，警戒等级2级')
                        # 发邮件，入侵级别为3
                        else:
                            self.invade_level = 3
                            self.send_my_mail(True, name)
                            print(name + '进入，警戒等级3级')
                        flag = False
                    name = pinyin.get_initial(name, delimiter="").lower()
                face_names.append(name)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top = int(top / scale)
                right = int(right / scale)
                bottom = int(bottom / scale)
                left = int(left / scale)

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)
                if name != 'Unknown':
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left, bottom + 6), font, 0.7, (255, 255, 255), 1)

            cv2.imwrite(path + '\\' + str(i) + '.jpg', frame)

        if flag:
            # 未知人员进入，发邮件，入侵级别为3
            self.invade_level = 3
            self.send_my_mail(False)
            print('未知人员进入，警戒等级3级')

    def send_my_mail(self, is_staff, name=None):
        emails = list(User.objects.filter(is_superuser=1).values('email'))
        email_list = []
        for email in emails:
            email_list.append(email['email'])
        title = "美团骑手offer"
        msg = ""
        if is_staff:
            msg = "{}进入{}\n警戒等级：{}\n报警来自摄像头{}\n日期：{}\n时间：{}" \
                .format(name, self.area, self.invade_level, self.camera_id, self._date, self._time)
        else:
            msg = "您的{}遭到未知人员入侵！\n入侵数量：{}\n警戒等级：{}\n报警来自摄像头{}\n日期：{}\n时间：{}" \
                .format(self.area, self.invasion_num, self.invade_level, self.camera_id, self._date, self._time)
        email_from = settings.DEFAULT_FROM_EMAIL
        reciever = email_list
        # 发送邮件
        try:
            send_mail(title, msg, email_from, reciever)
            print('send mail')
        except Exception as e:
            print(e)
            print('邮件发送失败')


if __name__ == '__main__':
    _model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    admins = list(mypicture.objects.values("photo", "phone"))

    print(admins)

    known_face_encodings = []
    admin_levels_names = []

    for admin in admins:
        img = face_recognition.load_image_file('./media/' + admin['photo'])
        item = {}
        temp = WhiteList.objects.filter(phone_number=admin['phone']).values('name', 'level')[0]
        item['name'] = temp['name']
        item['level'] = temp['level']
        admin_levels_names.append(item)
        face_encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(face_encoding)

    print('known face encode done')
    print(admin_levels_names)

    t = Invasion_Record_Saver(known_face_encodings, admin_levels_names, _model, '2021-07-08', '09:10:23', 2)
    t.start()

# class Yolo_Thread(threading.Thread):  # 继承父类threading.Thread
#     def __init__(self, d):
#         threading.Thread.__init__(self)
#         # self.detector = d
#
#     def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#         # self.detector.run2()
#         d = Detector()
#         d.run2()

class Email_Sender(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, known_face_encodings, _date, _time, invasion_num, level=1, camera_id=1, area='仓库', ):
        threading.Thread.__init__(self)
        self._date = _date
        self._time = _time
        self.invasion_num = invasion_num
        self.level = level
        self.camera_id = camera_id
        self.area = area
        self.known_face_encodings = known_face_encodings

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        self.process_pic()

    def process_pic(self):
        # Grab a single frame of video
        times = self._time.split(':')
        filename = self._date + '-' + times[0] + '-' + times[1] + '-' + times[2]
        path = 'E:\\watchDogs\\djangoProject\\monitor\\video\\' + filename
        print('path ', path)
        file_num = sum([os.path.isfile(path + '/' + listx) for listx in os.listdir(path)])
        print('pic num ', file_num)
        for i in range(0, file_num):
            frame = cv2.imread(path + '\\' + str(i) + '.jpg')
            print('processing ' + str(i) + '.jpg')
            scale = 0.5
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=1,
                                                             model="cnn")
            print('face locate done')
            face_encodings = face_recognition.face_encodings(rgb_small_frame, known_face_locations=face_locations,
                                                             num_jitters=20)
            print('face encoded done')
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.5)
                print('compare done')
                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    return

        self.send_my_mail()

    def send_my_mail(self):
        emails = list(User.objects.filter(is_superuser=1).values('email'))
        email_list = []
        for email in emails:
            email_list.append(email['email'])
        title = "美团骑手offer"
        msg = "您的{}遭到入侵！\n入侵数量：{}\n警戒等级：{}\n报警来自摄像头{}\n日期：{}\n时间：{}" \
            .format(self.area, self.invasion_num, self.level, self.camera_id, self._date, self._time)
        email_from = settings.DEFAULT_FROM_EMAIL
        reciever = email_list
        # 发送邮件
        try:
            send_mail(title, msg, email_from, reciever)
            print('send mail')
        except Exception as e:
            print(e)
            print('邮件发送失败')
