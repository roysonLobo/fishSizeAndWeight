import cv2
from object_detector import *
import numpy as np
import pyrebase

config={
    "apiKey": "AIzaSyC89FK4pNLaftno-VAKpCPJVQxIKDi7ung",
    "authDomain": "pythondbtest-8bff7.firebaseapp.com",
    "databaseURL": "https://pythondbtest-8bff7-default-rtdb.firebaseio.com",
    "databseURL":"https://pythondbtest-8bff7-default-rtdb.firebaseio.com/",
    "projectId": "pythondbtest-8bff7",
    "storageBucket": "pythondbtest-8bff7.appspot.com",
    "messagingSenderId": "1099219286383",
    "appId": "1:1099219286383:web:7d5a5da0de3b573e05d09a",
    "measurementId": "G-XG4CMK1W94"
  }
firebase=pyrebase.initialize_app(config)
database=firebase.database()

# Load Aruco detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

# Load Object Detector
detector = HomogeneousBgDetector()

# Load Cap
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
	_, img = cap.read()

    	# Get Aruco marker
	corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
	if corners:

		# Draw polygon around the marker
		int_corners = np.int0(corners)
		cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
		# Aruco Perimeter
		aruco_perimeter = cv2.arcLength(corners[0], True)

		# Pixel to cm ratio
		pixel_cm_ratio = aruco_perimeter / 20

		contours = detector.detect_objects(img)
		total_weight=0
		# Draw objects boundaries
		for cnt in contours:
			# Get rect
			rect = cv2.minAreaRect(cnt)
			(x, y), (l, b), angle = rect
			# Get Width and Height of the Objects by applying the Ratio pixel to cm
			object_length = l / pixel_cm_ratio
			object_breadth = b / pixel_cm_ratio
			# Display rectangle
			box=cv2.boxPoints(rect)
			box=np.int0(box)
			cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
			cv2.polylines(img, [box], True, (255, 0, 0), 2)
			object_length=max(object_length,object_breadth)
			object_breadth=min(object_length,object_breadth)
			cv2.putText(img, "Length {} cm".format(round(object_length,1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
			#cv2.putText(img, "Breadth {} cm".format(round(object_length,1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
			weight=0.0203*(object_length**3)
			cv2.putText(img, "Weight {} g".format(round(weight, 1)), (int(x - 50), int(y - 50)), cv2.FONT_HERSHEY_PLAIN, 2,(100, 200, 0), 2)
			# print(weight)
	cv2.imshow("Image", img)
	key = cv2.waitKey(1)
	if key == 27:
		n=0
		weights=[]
		lengths=[]
		_,img=cap.read()
		corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
		if corners:
			# Draw polygon around the marker
			int_corners = np.int0(corners)
			cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
			# Aruco Perimeter
			aruco_perimeter = cv2.arcLength(corners[0], True)

			# Pixel to cm ratio
			pixel_cm_ratio = aruco_perimeter / 20

			contours = detector.detect_objects(img)
			total_weight=0
			# Draw objects boundaries
			sub=0
			print(type(contours))
			for cnt in contours:
				# print(cnt)
				# Get rect
				rect = cv2.minAreaRect(cnt)
				(x, y), (l, b), angle = rect
				# Get Width and Height of the Objects by applying the Ratio pixel to cm
				object_length = l / pixel_cm_ratio
				object_breadth = b / pixel_cm_ratio
				# Display rectangle
				box=cv2.boxPoints(rect)
				box=np.int0(box)
				cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
				cv2.polylines(img, [box], True, (255, 0, 0), 2)
				object_length=max(object_length,object_breadth)
				object_breadth=min(object_length,object_breadth)
				cv2.putText(img, "Length {} cm".format(round(object_length,1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
				#cv2.putText(img, "Breadth {} cm".format(round(object_length,1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
				lengths.append(object_length)
				weight=0.0203*(object_length**3)
				weights.append(weight)
				cv2.putText(img, "Weight {} g".format(round(weight, 1)), (int(x - 50), int(y - 50)), cv2.FONT_HERSHEY_PLAIN, 2,(100, 200, 0), 2)
			cv2.imwrite('pic1.jpg',img)

			for i in range(0,len(weights)-1):
				data1={
					"length":lengths[i],
					"weight":weights[i]
				}
				database.push(data1)
				total_weight=total_weight+weights[i]
			print(weights)
			data2={
				"weight":total_weight
			}
			database.push(data2)
		break

cap.release()
cv2.destroyAllWindows()
