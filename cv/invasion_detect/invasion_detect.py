import cv2
import torch
import argparse

yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def init_cap(args):
    if args['video'] == '':
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(0, 640)  # set Width (the first parameter is property_id)
        cap.set(1, 480)  # set Height
    else:
        cap = cv2.VideoCapture(args['video'])
    return cap


def report(img, coord):
    person_type = "老人"
    cid = 1
    area = "宿舍"
    person_id = 99
    detail = "有人入侵辣！"
    file_name = './invasion/invasion_{}.png'.format(person_id)
    cv2.imwrite(file_name, img)



if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--video", required=False, default='',
                    help="")
    args = vars(ap.parse_args())

    cap = init_cap(args)
    # cap = cv2.VideoCapture(0)
    # cap.set(0, 640)  # set Width (the first parameter is property_id)
    # cap.set(1, 480)  # set Height

    invade_frame_cnt = 0
    min_motion_frames = 10
    reported = False
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
    size = (width, height)
    segmentation = [{'xmin': width / 4, 'xmax': width / 4 * 3, 'ymin': 0, 'ymax': height}]
    print(segmentation)

    while True:
        ret, img = cap.read()
        video = img.copy()
        results = yolo(video)

        for index, item in results.pandas().xyxy[0].iterrows():
            if item['class'] == 0:
                centerX = int((item['xmin'] + item['xmax']) / 2)
                centerY = int((item['ymin'] + item['ymax']) / 2)
                for seg in segmentation:
                    if centerX > seg['xmin'] and centerX < seg['xmax'] and centerY > seg['ymin'] and centerY < seg['ymax']:
                        invade_frame_cnt += 1
                        # print('invasion detected')
                        if invade_frame_cnt > min_motion_frames and not reported:
                            reported = True
                            report(img, item)
                    else:
                        reported = False
                        invade_frame_cnt = 0
        results.render()
        cv2.rectangle(results.imgs[0], (int(segmentation[0]['xmin']), int(segmentation[0]['ymin'])),
                      (int(segmentation[0]['xmax']), int(segmentation[0]['ymax'])), (60, 255, 0), 2)
        cv2.imshow('img', results.imgs[0])
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()