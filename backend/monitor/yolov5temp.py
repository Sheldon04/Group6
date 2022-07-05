            # # Images
            # video = frame_lwpCV  # or file, PIL, OpenCV, numpy, multiple
            # # Inference
            # results = model(video)
            # # Results
            # # results.show()  # or .show(), .save(), .crop(), .pandas(), etc.
            # # print(type(results.pandas().xyxy[0]['xmin'].values[0]))
            # if len(results.pandas().xyxy[0]['xmin'].values) != 0:
            #     cv2.rectangle(frame_lwpCV, (
            #         int(results.pandas().xyxy[0]['xmin'].values[0]), int(results.pandas().xyxy[0]['ymin'].values[0])),
            #         (int(results.pandas().xyxy[0]['xmax'].values[0]), int(results.pandas().xyxy[0]['ymax'].values[0])),
            #             (255, 255, 0), 2)

                # 物体追踪
                # if not flag:
                #     tracker = cv2.TrackerKCF_create()
                #     bbox = cv2.selectROI(frame_lwpCV, False)
                #     # print(bbox)
                #     # bbox = (x, y, w, h)
                #     print(bbox)
                #     ok = tracker.init(frame_lwpCV, bbox)
                #     flag = True
                #
                # ok, bbox = tracker.update(frame_lwpCV)
                # # if ok:
                # # new_frame = frame_lwpCV.copy()
                # p1 = (int(bbox[0]), int(bbox[1]))
                # p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                # cv2.rectangle(new_frame, p1, p2, (255, 0, 0), 2, 1)