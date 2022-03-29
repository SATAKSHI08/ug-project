import cv2
import math
import os
import numpy as np
from cv2 import VideoCapture
from cv2 import waitKey
import pyautogui as pg
import turtle
import time
##

ix,iy = -1,-1


###################quadrilateral##############
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
## 
##
cap = cv2.VideoCapture('Highway_5min.mp4')
r,f= cap.read()
cv2.imshow('image', f)


### setting mouse handler for the image
### and calling the click_event() function
cv2.setMouseCallback('image', click_event)


##
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


###############################car Haar Cascade###################################################################
car_cascade= cv2.CascadeClassifier('cars.xml')

while True:
    ret,frame= cap.read()

    ################### joining point to create a quad########################################################
    #image = cv2.line(image, start_point, end_point, color, thickness)
    cv2.line(frame,(RealXY[0][0] ,RealXY[0][1]), (RealXY[1][0],RealXY[1][1]), (45,0,210), 3)
    cv2.line(frame,(RealXY[1][0] ,RealXY[1][1]), (RealXY[2][0],RealXY[2][1]), (45,0,210), 3)
    cv2.line(frame,(RealXY[2][0] ,RealXY[2][1]), (RealXY[3][0],RealXY[3][1]), (45,0,210), 3)
    cv2.line(frame,(RealXY[3][0] ,RealXY[3][1]), (RealXY[0][0],RealXY[0][1]), (45,0,210), 3)



    ############################# croping the quadrilaeral######################################################
    pts=np.array(RealXY)
    
    rect = cv2.boundingRect(pts)
    x,y,w,h = rect
    if ret:
        croped = frame[y:y+h, x:x+w].copy()

        # for  masking
        pts = pts - pts.min(axis=0)
        mask = np.zeros(croped.shape[:2], np.uint8)
        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

        ##  do bit-op
        dst = cv2.bitwise_and(croped, croped, mask=mask)

    ############################## VEHICLE DETECTION ##########################################################
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cars= car_cascade.detectMultiScale(gray)
        for (x,y,w,h) in cars:
            #plate=f[y:y+h,x:x+w]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame,'car',(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(23,43,212),2)
           
        #frame=cv2.resize(frame,(600,400))
        
            cv2.imshow('vid',dst)
            
            k=cv2.waitKey(1)
           
            if k==27:
                break
cv2.destroyAllWindows()        
cap.release()

##    ############################ video #######################################################################
##    cv2.imshow("dst", dst)
##    k=cv2.waitKey(1)   
##    if k==27:
##            break


#####################################################################################################
##    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
##    cars= car_cascade.detectMultiScale(gray)
##    for (x,y,w,h) in cars:
##        #plate=f[y:y+h,x:x+w]
##        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
##        cv2.putText(frame,'car',(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(23,43,212),2)
##       
##        #frame=cv2.resize(frame,(600,400))
##        
##        cv2.imshow('vid',frame)
##        
##        k=cv2.waitKey(1)
##       
##        if k==27:
##            break
##cv2.destroyAllWindows()        
##cap.release()
##
