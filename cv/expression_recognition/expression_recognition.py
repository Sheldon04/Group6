import os

import requests
from PIL import Image, ImageDraw

import torch
import torch.nn.functional as F
import torchvision.transforms as T
import cv2
import time

from models.make_target_model import make_target_model
from oldcare.facial import FaceUtil
import imutils
import argparse

class Config:
    pass


cfg = Config()
cfg.ori_shape = (256, 256)
cfg.image_crop_size = (224, 224)
cfg.normalize_mean = [0.5, 0.5, 0.5]
cfg.normalize_std = [0.5, 0.5, 0.5]
cfg.last_stride = 2
cfg.num_classes = 8
cfg.num_branches = cfg.num_classes + 1
cfg.backbone = 'resnet18'  # 'resnet18', 'resnet50_ibn'
cfg.pretrained = "./weights/AffectNet_res18_acc0.6285.pth"
cfg.pretrained_choice = ''  # '' or 'convert'
cfg.bnneck = True
cfg.BiasInCls = False
key = {0: 'Neutral', 1: 'Happy', 2: 'Sad', 3: 'Surprise', 4: 'Fear', 5: 'Disgust', 6: 'Anger', 7: 'Contempt'}


def inference(model, img_path, transform, is_cuda=True):
    img = Image.open(img_path).convert('RGB')
    img_tensor = transform(img).unsqueeze(0)
    if is_cuda:
        img_tensor = img_tensor.cuda()

    model.eval()
    if is_cuda:
        model = model.cuda()

    pred = model(img_tensor)
    prob = F.softmax(pred, dim=-1)
    idx = torch.argmax(prob.cpu()).item()

    key = {0: 'Neutral', 1: 'Happy', 2: 'Sad', 3: 'Surprise', 4: 'Fear', 5: 'Disgust', 6: 'Anger', 7: 'Contempt'}
    print('Predicted: {}'.format(key[idx]))
    print('Probabilities:')
    for i in range(cfg.num_classes):
        print('{} ----> {}'.format(key[i], round(prob[0, i].item(), 4)))


def report_record(idx, name, frame):
    if idx == 2 or idx == 4 or idx == 5 or idx == 6:
        file_name = './face/face_{}.png'.format(idx)
        cv2.imwrite(file_name, frame)
        url = "http://47.106.148.74:8080/api/event/postemo"
        files = {'img': ('face.png', open(file_name, 'rb'), 'image/png', {})}
        data = {"cid": "1", "oid": "{}".format(name), "detail": "{}号老人十分伤心".format(name), "emo": key[idx]}
        resp = requests.post(url, data=data, files=files)
        print(resp)


def init_model(cfg):
    model = make_target_model(cfg)
    model.load_param(cfg)
    model.eval()
    model = model.cuda()
    return model


def init_cap():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(0, 640)  # set Width (the first parameter is property_id)
    cap.set(1, 480)  # set Height
    return cap


if __name__ == '__main__':
    img_path = './images/test1.jpg'
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--img", required=False, default='',
                    help="")
    ap.add_argument("-s", "--save", required=False, default='',
                    help="")
    args = vars(ap.parse_args())

    key = {0: 'Neutral', 1: 'Happy', 2: 'Sad', 3: 'Surprise', 4: 'Fear', 5: 'Disgust', 6: 'Anger', 7: 'Contempt'}
    transform = T.Compose([
        T.Resize(cfg.ori_shape),
        T.CenterCrop(cfg.image_crop_size),
        T.ToTensor(),
        T.Normalize(mean=cfg.normalize_mean, std=cfg.normalize_std),
    ])

    print('Building model......')
    model = init_model(cfg)
    print('Loaded pretrained model from {0}'.format(cfg.pretrained))

    # inference(model, img_path, transform, is_cuda=True)
    faceutil = FaceUtil()
    cap = init_cap()
    time.sleep(2)

    prev_expression = {}
    report = {}
    cnt = {}
    while True:
        if args['img'] != '':
            img = cv2.imread(args['img'], cv2.IMREAD_COLOR)
        else:
            ret, img = cap.read()
        frame = img
        frame = imutils.resize(frame, width=600)
        # face_location_list, names = faceutil.get_face_location_and_name(frame)
        face_location_list = faceutil.get_face_location(frame)
        names = [1] * len(face_location_list)

        for ((left, top, right, bottom), name) in zip(face_location_list, names):
            face_img = frame[top:bottom, left:right]
            face_img = Image.fromarray(face_img)
            img_tensor = transform(face_img).unsqueeze(0)
            img_tensor = img_tensor.cuda()
            pred = model(img_tensor)
            prob = F.softmax(pred, dim=-1)
            idx = torch.argmax(prob.cpu()).item()
            expression = key[idx]
            cv2.putText(frame, expression, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (0, 0, 255), 2)
            if name not in prev_expression or idx == prev_expression[name]:
                if name not in prev_expression:
                    cnt[name] = 0
                cnt[name] += 1
                if cnt[name] > 5 and not report[name]:
                    report_record(idx, name, frame)
                    # print('report {} man, emo {}'.format(name, idx))
                    report[name] = True
            else:
                cnt[name] = 0
                report[name] = False
            prev_expression[name] = idx

        cv2.imshow('img', frame)
        if args['save'] != '':
            cv2.imwrite(args['save'], frame)
        if args['img'] != '':
            break
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
