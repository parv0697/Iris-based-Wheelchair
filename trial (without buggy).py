import numpy as np
import cv2
import time
cap = cv2.VideoCapture(0)          
w = 1280
h = 1024
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = cv2.CascadeClassifier('haarcascade_eye.xml')
        detected = faces.detectMultiScale(frame, 1.3, 5)
        pupilFrame = frame
        pupilO = frame
        windowClose = np.ones((5,5),np.uint8)
        windowOpen = np.ones((2,2),np.uint8)
        windowErode = np.ones((2,2),np.uint8)
        for (x,y,w,h) in detected:
            cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)
            cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)
            cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
            pupilFrame = cv2.equalizeHist(frame[int(y+(h*.25)):(y+h), x:(x+w)])
            pupilO = pupilFrame
            ret, pupilFrame = cv2.threshold(pupilFrame,20,255,cv2.THRESH_BINARY)
            pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_CLOSE, windowClose)
            pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_ERODE, windowErode)
            pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_OPEN, windowOpen)
            threshold = cv2.inRange(pupilFrame,250,255)
            _,contours, hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) >= 2:
                maxArea = 0
                MAindex = 0
                distanceX = []
                currentIndex = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    '''print(area)'''
                    center = cv2.moments(cnt)
                    if center['m00']!=0:
                        cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                    else:
                        cx,cy=0,0
                    '''if cx>42:
                        print('right')
                    elif cx<28:
                        print('left')
                    elif cx>28 && cx<42:
                        print('middle')'''
                    distanceX.append(cx)
                    if area > maxArea:
                        maxArea = area
                        MAindex = currentIndex
                        currentIndex = currentIndex + 1
                del contours[MAindex]
                del distanceX[MAindex]
            eye = 'right'
            if len(contours) >= 2:
                if eye == 'right':
                    edgeOfEye = distanceX.index(min(distanceX))
                else:
                    edgeOfEye = distanceX.index(max(distanceX))
                del contours[edgeOfEye]
                del distanceX[edgeOfEye]
            if len(contours) >= 1:
                maxArea = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area > maxArea:
                        maxArea = area
                        largeBlob = cnt
            if len(largeBlob) > 0:
                center = cv2.moments(largeBlob)
                cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                cv2.circle(pupilO,(cx,cy),5,255,-1)
            for i in distanceX:
                #print(i)
                if i>40:
                    print('left')
                elif i>25 and i<=35:
                    print('middle')
                elif i<24:
                    print('right')
        cv2.imshow('frame',pupilO)
        cv2.imshow('frame2',pupilFrame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
