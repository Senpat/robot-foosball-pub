import cv2
import argparse
import time
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())
vs = cv2.VideoCapture(args["video"])
ct=328
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
	cv2.imwrite("C:/Users/zz198/Desktop/Senior Research/Videos/finalcam2frames/"+str(ct)+".jpg",frame)
	print(time.time()-start)
	key = cv2.waitKey(1) & 0xFF
	ct+=1
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()

# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()
