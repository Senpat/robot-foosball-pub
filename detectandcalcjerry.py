# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import math

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# greenLower = (29, 86, 6)
blueLower = (100, 100, 100)
blueUpper = (150, 255, 255)

pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=1).start()
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output.avi", fourcc, 120, (480, 852))
#out = cv2.VideoWriter("output.avi", fourcc, 120, (960, 540))
# allow the camera or video file to warm up
time.sleep(2.0)
start = time.time()
ct=0
# keep looping
while True:
    # grab the current frame
    frame = vs.read()

    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
    frame=cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #print(frame.shape[:2])
    #cv2.line(frame,(0,355),(480,355),(0,255,0),3)
    #cv2.line(frame, (0, 550), (480, 550), (0, 255, 0), 3)
    #cv2.line(frame, (0, 160), (480, 160), (0, 255, 0), 3)
    #cv2.line(frame, (0, 60), (480, 60), (0, 255, 0), 3)
    cv2.line(frame, (0, 280), (360, 280), (0, 255, 0), 3)
    cv2.line(frame, (0, 120), (360, 120), (0, 255, 0), 3)
    cv2.line(frame, (0, 35), (360, 35), (0, 255, 0), 3)
    cv2.line(frame, (0, 432), (360, 432), (0, 255, 0), 3)
    # resize the frame, blur it, and convert it to the HSV
    # color space
    #frame = imutils.resize(frame, width=480)


    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, blueLower, blueUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    pts.appendleft(center)
    #print(center)
    if len(pts)>15:
        if not (pts[0] is None or pts[8] is None or pts[10] is None or pts[15] is None):
            pt0 = np.array(pts[0])
            pt8 = np.array(pts[8])
            pt10 = np.array(pts[10])
            pt15 = np.array(pts[10])
            vec0=pt0-pt8
            vec1=pt0-pt10
            vec2=pt0-pt15
            #print(vec0,vec1,vec2)
            try:
                ang0=math.atan2(*np.flip(vec0))
                ang1 = math.atan2(*np.flip(vec1))
                ang2 = math.atan2(*np.flip(vec2))
                #print(ang0,ang1,ang2)
                if abs(ang0-ang1)<0.3 and abs(ang1-ang2)<0.3:
                    for y in (35,120,280,432):
                    #for y in (60,160,355,550):
                        x=int((y-pts[0][1])/math.tan(ang2)+pts[0][0])
                        #print(x,y)
                        if 0<x<480:
                            if pt0[1]<y:
                                cv2.circle(frame,(x,y),5,(255,0,0),3)
                            else:
                                cv2.circle(frame, (x, y), 5, (255, 255, 0), 3)
                #print("success")
            except:
                print("div by 0")
    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show the frame to our screen
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow("Frame", frame)
    out.write(frame)
    ct+=1
    print(ct*1.0/(time.time()-start))
    #print(time.time() - start)
    key = cv2.waitKey(1) & 0xFF
    #time.sleep(0.01)
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()
out.release()
# close all windows
cv2.destroyAllWindows()
