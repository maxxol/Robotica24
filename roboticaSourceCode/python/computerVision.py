import cv2 as cv
import numpy as np
from pyax12.connection import Connection
import RPi.GPIO as gpio
import time 

gpio.setup(18, gpio.OUT)

def get_computer_vision_results():
	GREEN_SCISSOR = True

	def colorRange(hsv, color_name):
		if color_name.lower() == "blue":
			lower = np.array([95, 20, 20])
			upper = np.array([130, 255, 255])
			return cv.inRange(hsv, lower, upper)
		elif color_name.lower() == "green":
			lower = np.array([40, 40, 40])
			upper = np.array([75, 255, 255])
			return cv.inRange(hsv, lower, upper)
		elif color_name.lower() == "red":
			lowerLeft = np.array([0, 50, 50])
			upperLeft = np.array([10, 255, 255])
			maskLeft = cv.inRange(hsv, lowerLeft, upperLeft)

			lowerRight = np.array([170, 50, 50])
			upperRight = np.array([180, 255, 255])
			maskRight = cv.inRange(hsv, lowerRight, upperRight)

			return maskLeft | maskRight

	KERNEL_SIZE = 21

	camera_index = 0
	cam = cv.VideoCapture(camera_index)
	gpio.output(18, gpio.HIGH)
	time.sleep(0.03)
	ret, image = cam.read()
	time.sleep(0.03)
	gpio.output(18, gpio.LOW) 
	hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

	if GREEN_SCISSOR:
		mask = colorRange(hsv, "green")
	else:
		mask = colorRange(hsv, "blue")

	mask = cv.GaussianBlur(mask, (KERNEL_SIZE, KERNEL_SIZE), 0)
	_, thresh = cv.threshold(mask, 100, 255, cv.THRESH_BINARY)
	contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

	num_points = len(contours[0])
	reshaped_contours = np.reshape(contours[0], (num_points, 2))

	rect = cv.minAreaRect(reshaped_contours)
	box = cv.boxPoints(rect)
	box = np.intp(box)

	M = cv.moments(reshaped_contours)
	if M['m00'] != 0:
		cx = int(M['m10'] / M['m00'])
		cy = int(M['m01'] / M['m00'])
	else:
		cx = 0
		cy = 0

	cont_img = cv.drawContours(image, [reshaped_contours], -1, color=(0, 255, 0), thickness=2)
	cont_img = cv.drawContours(cont_img, [box], 0, (255, 0, 0), 2)
	cont_img = cv.circle(cont_img, (cx, cy), 1, color=(255, 255, 255), thickness=3)
	cont_img = cv.circle(cont_img, (320, 240), 1, color=(255, 255, 255), thickness=6)

	if GREEN_SCISSOR:
		cv.imwrite('/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', cont_img)
		cv.imwrite('/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRechtThresh.jpg', thresh)
	else:
		cv.imwrite('/home/rob8/Desktop/Robotica24/roboticaSourceCode/python/pyIMG/schaarScheef.jpg', cont_img)
		cv.imwrite('/home/rob8/Desktop/Robotica24/roboticaSourceCode/python/pyIMG/schaarScheefThresh.jpg', thresh)

	rows, cols = cont_img.shape[:2]
	vx, vy, x, y = cv.fitLine(reshaped_contours, cv.DIST_L2, 0, 0.01, 0.01)


	# sc = Connection(port="/dev/serial0",baudrate=1000000, rpi_gpio=True)
	# ellebooghoek = sc.get_present_position(18)

	cvResults = [cx ,cy ,vx ,vy]
	return cvResults

	cam.release()

