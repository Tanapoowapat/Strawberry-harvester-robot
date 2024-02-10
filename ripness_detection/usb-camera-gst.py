#!/usr/bin/env python3
#
#  USB Camera - Simple
#
#  Copyright (C) 2021-22 JetsonHacks (info@jetsonhacks.com)
#
#  MIT License
#

import sys
from ultralytics import YOLO
import cv2

import time

window_title = "USB Camera"

# ASSIGN CAMERA ADRESS to DEVICE HERE!
pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ])

# Sample pipeline for H.264 video, tested on Logitech C920
h264_pipeline = " ! ".join(["v4l2src device=/dev/video0",
                            "video/x-h264, width=1280, height=720, framerate=30/1, format=H264",
                            "avdec_h264",
                            "videoconvert",
                            "video/x-raw, format=(string)BGR",
                            "appsink sync=false"
                            ])


def show_camera():

    # Full list of Video Capture APIs (video backends): https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html
    # For webcams, we use V4L2
    video_capture = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    model = YOLO('model/segment/best.engine', task='segment')
    prev_frame_time = 0
    new_frame_time = 0
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(
                window_title, cv2.WINDOW_AUTOSIZE)
            # Window
            while True:
                ret_val, frame = video_capture.read()
                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user

                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    results = model(frame, stream=True, conf=0.9, half=True, device=0)
                
                    #CALCULATE FPS
                    new_frame_time = time.time()
                    fps = 1/(new_frame_time-prev_frame_time)
                    prev_frame_time = new_frame_time
                    fps = int(fps)
                    fps = str(fps)
                    
                    cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX , 3, (100, 255, 0), 3, cv2.LINE_AA)
                    
                    for result in results:
                        frame = result.plot()

                    cv2.imshow(window_title, frame)
                else:
                    break
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break

        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()
