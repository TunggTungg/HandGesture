import mediapipe as mp
import cv2
import math
import numpy as np
import pyautogui

class handDetector():
    def __init__(self, mode = False, max_hands = 2, min_detection = 0.7, min_tracking = 0.4):
        self.static_image_mode = mode
        self.max_num_hands = max_hands
        self.min_detection_confidence = min_detection
        self.min_tracking_confidence = min_tracking

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.static_image_mode, self.max_num_hands, self.min_detection_confidence,
                                        self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def find_Hands(self, img, draw = True):
        # BGR 2 RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Flip on horizontal
        img = cv2.flip(img, 1)
        
        # Set flag
        img.flags.writeable = False
        
        # Detections
        result = self.hands.process(img)
        
        # Set flag to true
        img.flags.writeable = True
        
        # RGB 2 BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        state = None
        if result.multi_hand_landmarks and len(result.multi_hand_landmarks) == 2:
            h, w, _ = img.shape
            hand_centers = []
            y_left, y_right = 0, 0
            for idx, handLms in enumerate(result.multi_hand_landmarks):
                hand_centers.append([int(handLms.landmark[9].x*w), int(handLms.landmark[9].y*h)])
                if handLms.landmark[8].y > handLms.landmark[5].y and idx == 0: 
                    pyautogui.press('space')

                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
            
            cv2.line(img, (hand_centers[0][0], hand_centers[0][1]), (hand_centers[1][0], hand_centers[1][1]), (0,255,0), 5)
            center_x = int(hand_centers[0][0]+hand_centers[1][0]) // 2
            center_y = int(hand_centers[0][1]+hand_centers[1][1]) // 2
            radius = int(math.sqrt((hand_centers[0][0] - hand_centers[1][0])**2 + (hand_centers[0][1] - hand_centers[1][1])**2) / 2)
            cv2.circle(img, (center_x, center_y), radius, (0,255,0), 5)
            delta = hand_centers[1][1] - hand_centers[0][1]
            if delta > 25:
                if delta > 50:
                    state = 2
                else:
                    state = 3
            elif delta < -25: 
                if delta < -50: 
                    state = 4
                else:
                    state = 5
        return img, state   
