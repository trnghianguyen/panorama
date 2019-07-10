# USAGE
# python image_stitching.py --images images/scottsdale --output output.png --crop 1

from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

def stitching(image_list):
	
	# Khoi tao cac doi tuong de stitching
	stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
	(status, stitched) = stitcher.stitch(image_list)
	if status == 0:
		if args["crop"] > 0:
			# create border surrounding the stitched image
			print("[INFO] cropping...")
			stitched = cv2.copyMakeBorder(stitched, 5, 5, 5, 5,
				cv2.BORDER_CONSTANT, (0, 0, 0))

			# convert to grayscale and threshold
			gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
			thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

			# find all external contours in the threshold image then find
			cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
			c = max(cnts, key=cv2.contourArea)

			# allocate memory for the mask which will contain the
			# rectangular bounding box of the stitched image region
			mask = np.zeros(thresh.shape, dtype="uint8")
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

			# create two mask: one to serve as our actual
			# minimum rectangular region 
			minRect = mask.copy()
			sub = mask.copy()

			# subtracted image
			while cv2.countNonZero(sub) > 0:
				# thresholded image 
				minRect = cv2.erode(minRect, None)
				sub = cv2.subtract(minRect, thresh)

			# find contours 
			# (x, y)-coordinates
			cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
			c = max(cnts, key=cv2.contourArea)
			(x, y, w, h) = cv2.boundingRect(c)

			# stitched image
			stitched = stitched[y:y + h, x:x + w]

		# write the output stitched image to disk
		cv2.imwrite("ouput.png", stitched)

		# display output
		cv2.imshow("Stitched", stitched)
		cv2.waitKey(0)

	else:
		print("[INFO] image stitching failed ({})".format(status))
