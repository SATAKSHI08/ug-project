import cv2
import numpy as np
from tracker import *

# Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("highway_5min.mp4")

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
##################################################


f = 25
w = int(1000/(f-1))
print(w)


############# coordinate #############################################################
#####real coordinate are RealXY
xy_coordinate=[]

def click_event(event, x, y, flags, params):
    global xy_coordinate
    global ix,iy
#####checking for left mouse clicks########################
    if event == cv2.EVENT_LBUTTONDOWN:
        
        ########## displaying the coordinates#########
        #print(x, ' ', y)
        ix,iy=x,y
        xy_coordinate.append([ix,iy])
        
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(f, str(x) + ',' +
                    str(y), (x,y), font,
                    0.5, (255, 0, 0), 2)
        cv2.imshow('image',f)
 
    # checking for right mouse clicks    
    if event==cv2.EVENT_RBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        #print(x, ' ', y)
        ix,iy=x,y
        xy_coordinate.append([ix,iy])
        
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(f, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 0.5,
                    (255, 255, 0), 1)
        cv2.imshow('image', f)

r,f= cap.read()
cv2.imshow('image', f)


### setting mouse handler for the image
### and calling the click_event() function
cv2.setMouseCallback('image', click_event)

while(1):
    fr=cv2.resize(f,(600,400))
    cv2.imshow('img',fr)
    k = cv2.waitKey(20) & 0xFF
    cv2.waitKey(11000)
    if k == 27:
        break
    else:
        #print (xy_coordinate)
        RealXY = xy_coordinate.copy()
    break
cv2.destroyAllWindows()
print(RealXY)




############################################################################
        
while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape
    #image = cv2.line(image, start_point, end_point, color, thickness)
    cv2.line(frame,(RealXY[0][0] ,RealXY[0][1]), (RealXY[1][0],RealXY[1][1]), (45,0,210), 3)
    cv2.line(frame,(RealXY[1][0] ,RealXY[1][1]), (RealXY[2][0],RealXY[2][1]), (45,0,210), 3)
    cv2.line(frame,(RealXY[2][0] ,RealXY[2][1]), (RealXY[3][0],RealXY[3][1]), (45,0,210), 3)
    cv2.line(frame,(RealXY[3][0] ,RealXY[3][1]), (RealXY[0][0],RealXY[0][1]), (45,0,210), 3)
    ### croping for roi
    pts=np.array(RealXY)
    rect = cv2.boundingRect(pts)
    x,y,w,h = rect
    if ret:
        roi = frame[y:y+h, x:x+w].copy()
 
        pts = pts - pts.min(axis=0)
        mask = np.zeros(roi.shape[:2], np.uint8)
        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

        ##  do bit-op
        roi = cv2.bitwise_and(roi,roi, mask=mask)
        

##    # Extract Region of interest
##    roi = frame[340: 720,500: 800]

    # 1. Object Detection
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 100:
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)


            detections.append([x, y, w, h])

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)


##        if(tracker.getsp(id)<tracker.limit()):
##            cv2.putText(roi,str(id)+" "+str(tracker.getsp(id)),(x,y-15), cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
##            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
##        else:
##            cv2.putText(roi,str(id)+ " "+str(tracker.getsp(id)),(x, y-15),cv2.FONT_HERSHEY_PLAIN, 1,(0, 0, 255),2)
##            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 165, 255), 3)

        s = tracker.getsp(id)
        if (tracker.f[id] == 1 and s != 0):
            tracker.capture(roi, x, y, h, w, s, id)

            
    cv2.imshow("roi", roi)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(w-10)
    if key == 27:
        tracker.end()
        end=1
        break
if(end!=1):
    tracker.end()

cap.release()
cv2.destroyAllWindows()


