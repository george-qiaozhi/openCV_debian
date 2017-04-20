import imutils
import argparse
import cv2
 
ap = argparse.ArgumentParser()
ap.add_argument("-video", help="video file path")
ap.add_argument("-min_area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
 
# reading from a input video file
inpt = cv2.VideoCapture(args["video"])
 
# initialize a temporary frame 
temp = None
global_cnt = 0
while True:
	# from input get the current frame 
	(frame1, frame) = inpt.read()
	text = "undetected"
	
	# break if unable to get the frame
	if not frame1:
		break
 
	# coverting frame to grayscale
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	# storing it in temporary frame
	if temp is None:
		temp = gray
		continue

	# computing the absolute difference between the current frame and temporary frame
	diff = cv2.absdiff(temp, gray)
	thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
 
	# finding the contours
	thresh = cv2.dilate(thresh, None, iterations=2)
	#(_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
 	
	# for displaying the number of objects
	count = 0

	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue
 
		# compute the bounding box for the contour
		#(x, y, w, h) = cv2.boundingRect(c)
		#cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
		count=count+1
		#text = "detected"
	
	print 'Frame %d: %d' % (global_cnt, count)
	global_cnt+=1	

	# displaying the text and the number of objects detected on the frame
	#cv2.putText(frame, str(count), (10,50 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
	#cv2.putText(frame, "motion: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
 
	# Displaying the resultant video
	#cv2.imshow("Input Video", frame)
	#key = cv2.waitKey(1) & 0xFF
 
	# press space to exit 
	#if key == ord(" "):
	#	break
 
inpt.release()
cv2.destroyAllWindows()

