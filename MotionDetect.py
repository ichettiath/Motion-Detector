import cv2
import time
import pandas
from datetime import datetime

Enter_Exit_Times = pandas.DataFrame(columns = ["Enter", "Exit"])

first_frame = None

#status indicates whether there is motion, 0 for no motion, 1 for motion
status_changes = [None, None]
status_times = []
onlyMotion = True

video = cv2.VideoCapture(0)

while (True):
    check, color_frame = video.read()
    status = 0

    gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)

    #GaussianBlur smoothens images, so shadows are not detected as motion
    gray_frame = cv2.GaussianBlur(gray_frame,(21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame
        #time is appended twice so plot is still rendered when there is no motion
        status_times.append(datetime.now())
        status_times.append(datetime.now())
        continue

    #finds the difference between the current frame and the previous frame
    delta_frame = cv2.absdiff(first_frame, gray_frame)

    #if delta value in an area meets the treshold value it is displayed
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    #creates a list of areas in which the tresh frame renders 
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        #searches for contours only if there are larger than 10000 pixels
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1
        #creates the rectangle around the area of motion
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(color_frame, (x,y), (x+w, y+h), (0,0,255), 3)

    if status == 0:
        onlyMotion = False
    else:
        noMotion = False
    status_changes.append(status)
    
    #if status changes from no motion to motion
    if status_changes[-1] == 1 and status_changes[-2] == 0:
        status_times.append(datetime.now())

    #if status changes from motion to no motion
    if status_changes[-1] == 0 and status_changes[-2] == 1:
        status_times.append(datetime.now())

    cv2.imshow("Detector", color_frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        if status == 1:
            status_times.append(datetime.now())
        elif status == 0:
            #time is appended twice so plot is still rendered when there is no motion at the ending of the program
            status_times.append(datetime.now())
            status_times.append(datetime.now())
        break

#time should not be added twice at the beginning when there is only motion
if (onlyMotion):
    status_times.pop(0)

#every odd index represents an enter and every even index represents an exit
for i in range(0, len(status_times), 2):
    Enter_Exit_Times = Enter_Exit_Times.append({"Enter": status_times[i], "Exit": status_times[i+1]}, ignore_index = True)

Enter_Exit_Times.to_csv("Motion_Times.csv")

video.release()
cv2.destroyAllWindows()
