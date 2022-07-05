import cv2
from cv2 import WINDOW_AUTOSIZE

cv2.namedWindow("camera",1)
#开启ip摄像头
video="http://admin:123456@172.30.95.184:8081/video"   #此处@后的ipv4 地址需要改为app提供的地址
#video = "http://admin:admin@192.168.43.1:8081"
cap =cv2.VideoCapture(video)
while True:
    # Start Camera, while true, camera will run
    ret, image_np = cap.read()
    # Set height and width of webcam
    height = 600
    width = 1000
    # Set camera resolution and create a break function by pressing 'q'
    cv2.imshow('object detection', cv2.resize(image_np, (width, height)))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
# Clean up
cap.release()
cv2.destroyAllWindows()
