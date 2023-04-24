# import the opencv library
import cv2
import HandTrackingModule
import pyautogui
import time
import threading
import keyboard

def go_right():
    global key
    while key:
        pyautogui.press('d')
        time.sleep(0.01) 

def go_left():
    global key
    while key:
        pyautogui.press('a')
        time.sleep(0.01) 
 
def drift():
    global key 
    pyautogui.keyDown('s')
    while key:
        time.sleep(0.01) 
    pyautogui.keyUp('s') 

# define a video capture object
vid = cv2.VideoCapture(0)
handDetector = HandTrackingModule.handDetector()
state = None
pre_state = state
key = False

while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    frame, state = handDetector.find_Hands(frame)
    # State: 1: W, 2: D, 3: SD, 4: A, 5: SA
    if state != pre_state:
        key = False
        
        if state == 2:
            t = threading.Thread(target=drift)
        elif state == 3:
            t = threading.Thread(target=go_right)
        elif state == 4:
            t = threading.Thread(target=drift)
        elif state == 5:
            t = threading.Thread(target=go_left)
        elif state == None:
            key = False
        if state != None:
            time.sleep(0.2)
            key = True
            t.start()

        
        pre_state = state            
                        

    # Display the resulting frame
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()


 