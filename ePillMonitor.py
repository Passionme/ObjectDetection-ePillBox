import argparse
from picamera import PiCamera
import cv2
import numpy as np
import ctypes
import datetime
import imutils


parser =	argparse.ArgumentParser()
parser.add_argument("day")
args = parser.parse_args()

if args.day:
	day_count =	int(args.day)
else:
	now =	datetime.datetime.now()
	day_count =	int(now.day)


if  (28 <day_count <= 31) :
	with open('home/pi/Desktop/ePillMonitor/PrevData.txt','r') as file:
		data = json.loads(file)
		square_count =	data["square_count"]
		file.close()
elif 1 <day_count < 28:
	square_count =	0
else:
	ctypes.windll.user32.MessageBoxW(0, "Error! Day is beyond possible value: " + day_count, "ePill Monitor Error", 1)
	
	

#Access camera from pi
camera = PiCamera()
#camera.resoution =	(694x458)
#camera.framerate =	15

#capture from the camera
camera.capture('home/pi/Desktop/ePillMonitor/images/Day{}.png'.format(day_count))

#cap=	cv2.VideoCapture(0)
#ret, picture =	cap.read()
#cv2.imwrite('home/pi/Desktop/images/Day{}.png'.format(day), picture)

picture =	cv2.imread('home/pi/Desktop/ePillMonitor/images/Day{}.png'.format(day),0)
gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
 
# find contours in the thresholded image and initialize the
# shape detector
contours = cv2.findContours(thresh.copy(), cv.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(cnts)

for contour in contours:
	perimeter = cv.arcLength(contour, True)
	approx = cv.approxPolyDP(c, 0.04 * perimeter, True)
	if len(approx) == 4:
		square_count +=	1


#if  (28 <day_count > 31) :
todays_data =	{
          "day_count" : day_count,
          "square_count" : square_count
       }
with open('home/pi/Desktop/ePillMonitor/PrevData.txt','w') as file:
	json.dump(todays_data, file)
	file.close()
	
#is day count is equal to empty sqaure
if (square_count ==	day_count ):
	ctypes.windll.user32.MessageBoxW(0, "Pill Count up to date", "ePill Monitor", 1)
elif square_count < day_count	:
	ctypes.windll.user32.MessageBoxW(0, "Pill over dosed", "ePill Monitor Error", 1)
else:
	ctypes.windll.user32.MessageBoxW(0, "Pill under dosed", "ePill Monitor.Error", 1)





