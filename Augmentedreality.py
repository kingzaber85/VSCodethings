import cv2
import numpy as np
import math

# Load ArUco dictionary
aruco = cv2.aruco
dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

detector = aruco.ArucoDetector(dict_aruco, parameters)

# Target position (simulated goal)
TARGET_X = 320
TARGET_Y = 240

def get_distance(cx, cy):
    return math.sqrt((cx - TARGET_X)**2 + (cy - TARGET_Y)**2)

def get_feedback(distance):
    if distance < 50:
        return "VERY HOT", (0, 0, 255)
    elif distance < 100:
        return "HOT", (0, 100, 255)
    elif distance < 200:
        return "WARM", (0, 255, 255)
    else:
        return "COLD", (255, 0, 0)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    detector = aruco.ArucoDetector(dict_aruco, parameters)
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        for corner in corners:
            pts = corner[0]
            cx = int(np.mean(pts[:, 0]))
            cy = int(np.mean(pts[:, 1]))

            # Draw marker center
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            # Distance logic
            dist = get_distance(cx, cy)
            text, color = get_feedback(dist)

            # Draw feedback text
            cv2.putText(frame, text, (cx - 50, cy - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Draw line to target
            cv2.line(frame, (cx, cy), (TARGET_X, TARGET_Y), color, 2)

    # Draw target point
    cv2.circle(frame, (TARGET_X, TARGET_Y), 10, (255, 255, 255), -1)
    cv2.putText(frame, "TARGET", (TARGET_X - 40, TARGET_Y - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("AR Scavenger Hunt", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break
    
aruco.drawDetectedMarkers(frame, corners, ids)

cap.release()
cv2.destroyAllWindows()