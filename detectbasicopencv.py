import cv2

cap = cv2.VideoCapture("C:/Users/zz198/Desktop/Senior Research/Videos/jerrycam1.mp4")
if not cap:
    print("!!! Failed VideoCapture: invalid parameter!")
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(frame_width,frame_height)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (frame_height, frame_width))
fr=0
while (True):
    # Capture frame-by-frame
    x_accum = 0
    y_accum = 0
    ctpix = 0
    ret, current_frame = cap.read()
    if type(current_frame) == type(None):
        print("!!! Couldn't read frame!")
        break

    for x in range(frame_width):
        for y in range(frame_height):
            color = current_frame[y, x]
            #bgr
            if color[0] < 70 and color[1] < 70 and color[2]>100:
                x_accum += x
                y_accum += y
                ctpix += 1
                #cv2.circle(current_frame,(x,y),2,(0,255,0),1)
    print(ctpix)
    cv2.circle(current_frame, (x_accum // ctpix, y_accum // ctpix), 3, (0, 0, 255), 2)
    #out.write(current_frame)
    cv2.imshow("hi",current_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    fr+=1
    print(fr)
# release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
