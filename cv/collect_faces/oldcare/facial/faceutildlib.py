# -*- coding: utf-8 -*-
'''
使用dlib实现人脸检测
'''
import face_recognition
import cv2

class FaceUtil:
    
    # 超参数
    detection_method = 'hog' # either 'hog' or 'cnn'. default is hog.
    
    # face detection
    def get_face_location(self, image):
        face_location_list = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_locations = face_recognition.face_locations(
                         gray, number_of_times_to_upsample=1, 
                         model = self.detection_method)
        # 人脸位置
        for (top, right, bottom, left) in face_locations:
            face_location_list.append((left, top, right, bottom))
        
        return face_location_list
    
    
    
    