#runs detection code in detectbasicopencv2.py and calculate trajectory with calc.py, and display
#based off of detectandcalc.py, uses linear regression for less erratic trajectory calculation.
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

ERRORTHRESH = 8
SLOMO = False
VIDEO = True

#jerrycam3
YU = 21
YD = 493
#finalcam2 half
#YU = 0
#YD = 540
LEVERS = [306,504,704,801] #jerrycam3.mp4
#LEVERS = [294,552,813,951] #finalcam2.mp4 and resived

prevx = np.array([])
prevy = np.array([])



def checknewcolumn(px,py):
	lastx = prevx[-1]
	for i in LEVERS:
		if(px>i and lastx<i):
			return True
	return False


#takes in a point (px,py) which is the latest coordinate of the ball.
#uses linear regression and restarts calculating when ball crosses a lever (only time it can be deflected)
#return list that contains the y coordinate of ball at each of the levers
def calc(px,py):
	global prevx,prevy
	#print(px,py)
	#prev is empty
	if(len(prevx)==0):
		prevx = np.array([px])
		prevy = np.array([py])
		return

	#ball is going forward - check px > x of last point
	if(px <= prevx[-1]):
		prevx = np.array([px])
		prevy = np.array([py])
		return

	#in new column, restart checking linear regression
	if(checknewcolumn(px,py)):
		prevx = np.array([px])
		prevy = np.array([py])
		return



	#list that contains the y coordinate of ball at each of the levers
	#-1 means ball is in front of lever, so don't move it
	ret = [-1,-1,-1,-1]

	prevx = np.append(prevx,[px])
	prevy = np.append(prevy,[py])

	z,_,_,_,_ = np.polyfit(prevx,prevy,1,full=True)
	p = np.poly1d(z)
	print(str(z) + " " + str(len(prevx)))

	for i in range(len(LEVERS)):
		ret[i] = p(LEVERS[i])
		if(ret[i] < YU):
			ret[i] += 2*(YU-ret[i])
		if(ret[i] > YD):
			ret[i] -= 2*(ret[i]-YD)


	#print("hi" + ret)



	#print(ret)
	return ret

#takes in a point (px,py) which is the latest coordinate of the ball.
#uses linear regression and restarts when the regression reaches a certain error
#return list that contains the y coordinate of ball at each of the levers
def calc2(px,py):
	global prevx,prevy
	#print(px,py)
	#prev is empty
	if(len(prevx)==0):
		prevx = np.array([px])
		prevy = np.array([py])
		#print("ADD 1")
		return

	#ball is going forward - check px > x of last point
	if(px < prevx[-1]):
		prevx = np.array([px])
		prevy = np.array([py])
		#print("BACKWARDS")
		return


	#list that contains the y coordinate of ball at each of the levers
	#-1 means ball is in front of lever, so don't move it
	ret = [-1,-1,-1,-1]

	prevx = np.append(prevx,[px])
	prevy = np.append(prevy,[py])

	z,error,_,_,_ = np.polyfit(prevx,prevy,1,full=True)
	print(str(error) + " " + str(len(prevx)))
	#print(prevx)
	if(len(error) == 1 and error[0] > ERRORTHRESH):
		prevx = np.array([px])
		prevy = np.array([py])
		print("RESET")
		return


	p = np.poly1d(z)
	#print(str(z) + " " + str(len(prevx)))

	if(len(prevx) >= 3):
		for i in range(len(LEVERS)):
			ret[i] = p(LEVERS[i])
			if(ret[i] < YU):
				ret[i] += 2*(YU-ret[i])
			if(ret[i] > YD):
				ret[i] -= 2*(ret[i]-YD)


	#print("hi" + ret)



	#print(ret)
	return ret





def run(vs):
	print("running...")

	# define the lower and upper boundaries of the "green"
	# ball in the HSV color space, then initialize the
	# list of tracked points
	#greenLower = (29, 86, 6)
	greenLower = (100, 100, 100)
	greenUpper = (150, 255, 255)
	pts = deque(maxlen=args["buffer"])



	# keep looping
	while True:
		start=time.time()
		# grab the current frame
		frame = vs.read()

		# handle the frame from VideoCapture or VideoStream
		frame = frame[1] if args.get("video", False) else frame

		# if we are viewing a video and we did not grab a frame,
		# then we have reached the end of the video
		if frame is None:
			break

		# resize the frame, blur it, and convert it to the HSV
		# color space
		#frame = imutils.resize(frame, width=480)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		center = None

		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

			# only proceed if the radius meets a minimum size
			if radius > 0:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)



				#calculate intersect points with the levers and draw a blue circle there
				intersections = calc(int(x),int(y))
				if(intersections):
					for i in range(len(LEVERS)):
						#print(LEVERS[i],intersections[i])
						cv2.circle(frame,(LEVERS[i],int(intersections[i])),10,(255,0,0),-1)





		# update the points queue
		pts.appendleft(center)

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
		cv2.imshow("Frame", frame)
		if(VIDEO):
			out.write(frame)
		#print(time.time()-start)
		key = cv2.waitKey(1) & 0xFF

		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break

		#"slomo"
		if(SLOMO and len(cnts)>0):
			time.sleep(0.1)


	# if we are not using a video file, stop the camera video stream
	if not args.get("video", False):
		vs.stop()

	# otherwise, release the camera
	else:
		vs.release()
	out.release()
	# close all windows
	cv2.destroyAllWindows()



if __name__ == "__main__":
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video",
		help="path to the (optional) video file")
	ap.add_argument("-b", "--buffer", type=int, default=64,
		help="max buffer size")
	args = vars(ap.parse_args())

	# if a video path was not supplied, grab the reference
	# to the webcam
	if not args.get("video", False):
		vs = VideoStream(src=0).start()
	# otherwise, grab a reference to the video file
	else:
		vs = cv2.VideoCapture(args["video"])
	fourcc = cv2.VideoWriter_fourcc(*'XVID')									#commented out to not show
	out = cv2.VideoWriter("detectbasic2.avi", fourcc, 120, (852,480))
	# allow the camera or video file to warm up
	print("warming up...")
	time.sleep(2.0)

	run(vs)
