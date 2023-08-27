# import the necessary packages
from enum import Enum
from imutils.video import VideoStream
import imutils
import time
import cv2
import numpy as np

MIN_AREA = 500


class SpotState(str, Enum):
	EMPTY = "empty"
	OCCUPIED = "occupied"

	def __str__(self) -> str:
		return self.value



def main():
	COUNTER = 0
	video_stream = VideoStream(src=0).start()
	time.sleep(2.0)
	# initialize the first frame in the video stream
	first_frame = None
	# loop over the frames of the video
	while True:
		frame = video_stream.read()
		text = SpotState.EMPTY
		# resize the frame, convert it to grayscale, and blur it
		frame = imutils.resize(frame, width=500)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
		# if the first frame is None, initialize it
		if first_frame is None:
			first_frame = gray
			continue
		# compute the absolute difference between the current frame and
		# first frame
		frameDelta = cv2.absdiff(first_frame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
		# dilate the thresholded image to fill in holes, then find contours
		# on thresholded image
		all_zeros = not np.any(thresh)
		print(all_zeros)
		thresh = cv2.dilate(thresh, None, iterations=2)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		# loop over the contours
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < MIN_AREA:
				continue
			text = SpotState.OCCUPIED
		if COUNTER % 500 == 0:
			print(text)
		COUNTER += 1

if __name__ == '__main__':
	main()