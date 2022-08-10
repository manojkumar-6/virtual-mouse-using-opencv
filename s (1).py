from cv2 import VideoCapture
import mediapipe as mp
import cv2
import speech_recognition as sr
import pyttsx3
import numpy as np
import subprocess
from mediapipe.framework.formats import landmark_pb2
import time
from math import sqrt
import win32api
import pyautogui
import webbrowser
import mediapipe as mp
from math import hypot
import cv2
from cvzone.HandTrackingModule import HandDetector
import screen_brightness_control as sbc
import numpy as np
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
def SpeakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
click=0

video = cv2.VideoCapture(0)
SpeakText("welcome to virtual mouse using opencv the available functinalities are click,browser,notepad,volume and brightness adjustment")
numb=int(input("enter"))
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    if numb==1:
        SpeakText("you have enabled click functionality")
        while video.isOpened():
            _, frame = video.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            image = cv2.flip(image, 1)

            imageHeight, imageWidth, _ = image.shape

            results = hands.process(image)


            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for num, hand in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                            )

            if results.multi_hand_landmarks != None:
                for handLandmarks in results.multi_hand_landmarks:
                    for point in mp_hands.HandLandmark:


                        normalizedLandmark = handLandmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)

                        point=str(point)

                        if point=='HandLandmark.INDEX_FINGER_TIP':
                            try:
                                indexfingertip_x=pixelCoordinatesLandmark[0]
                                indexfingertip_y=pixelCoordinatesLandmark[1]
                                win32api.SetCursorPos((indexfingertip_x*4,indexfingertip_y*5))

                            except:
                                pass

                        elif point=='HandLandmark.THUMB_TIP':
                            try:
                                thumbfingertip_x=pixelCoordinatesLandmark[0]
                                thumbfingertip_y=pixelCoordinatesLandmark[1]
                                #print("thumb",thumbfingertip_x)

                            except:
                                pass

                        try:
                            #pyautogui.moveTo(indexfingertip_x,indexfingertip_y)
                            Distance_x= sqrt((indexfingertip_x-thumbfingertip_x)**2 + (indexfingertip_x-thumbfingertip_x)**2)
                            Distance_y= sqrt((indexfingertip_y-thumbfingertip_y)**2 + (indexfingertip_y-thumbfingertip_y)**2)
                            if Distance_x<5 or Distance_x<-5:
                                if Distance_y<5 or Distance_y<-5:
                                    click=click+1
                                    if click%5==0:
                                        print("single click")
                                        pyautogui.click()

                        except:
                            pass

            cv2.imshow('Hand Tracking', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    elif numb==2:
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        mpDraw = mp.solutions.drawing_utils
        SpeakText("you have enabled brightness functionality")
        while True:
            success,img = video.read()
            imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            lmList = []
            if results.multi_hand_landmarks:
                for handlandmark in results.multi_hand_landmarks:
                    for id,lm in enumerate(handlandmark.landmark):
                        h,w,_ = img.shape
                        cx,cy = int(lm.x*w),int(lm.y*h)
                        lmList.append([id,cx,cy])
                    mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)

            if lmList != []:
                x1,y1 = lmList[4][1],lmList[4][2]
                x2,y2 = lmList[8][1],lmList[8][2]

                cv2.circle(img,(x1,y1),4,(255,0,0),cv2.FILLED)
                cv2.circle(img,(x2,y2),4,(255,0,0),cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)

                length = hypot(x2-x1,y2-y1)

                bright = np.interp(length,[15,220],[0,100])
                print(bright,length)
                sbc.set_brightness(int(bright))

                # Hand range 15 - 220
                # Brightness range 0 - 100

            cv2.imshow('Image',img)
            if cv2.waitKey(1) & 0xff==ord('q'):
                break
    elif numb==3:
        SpeakText("you have enabled volume functionality")
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        mpDraw = mp.solutions.drawing_utils
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        volMin,volMax = volume.GetVolumeRange()[:2]

        while True:
            success,img = video.read()
            imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            lmList = []
            if results.multi_hand_landmarks:
                for handlandmark in results.multi_hand_landmarks:
                    for id,lm in enumerate(handlandmark.landmark):
                        h,w,_ = img.shape
                        cx,cy = int(lm.x*w),int(lm.y*h)
                        lmList.append([id,cx,cy])
                    mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)

            if lmList != []:
                x1,y1 = lmList[4][1],lmList[4][2]
                x2,y2 = lmList[8][1],lmList[8][2]

                cv2.circle(img,(x1,y1),4,(255,0,0),cv2.FILLED)
                cv2.circle(img,(x2,y2),4,(255,0,0),cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)

                length = hypot(x2-x1,y2-y1)

                vol = np.interp(length,[15,220],[volMin,volMax])
                print(vol,length)
                volume.SetMasterVolumeLevel(vol, None)

                # Hand range 15 - 220
                # Volume range -63.5 - 0.0

            cv2.imshow('Image',img)
            if cv2.waitKey(1) & 0xff==ord('q'):
                break
    elif numb==5:
        SpeakText("you have enabled browser functionality")
        webbrowser.open('http://www.google.com')
    elif numb==6:

        #path = r'path/to/your/file.txt'
        SpeakText("you have enabled Notepad  functionality")
        subprocess.Popen(['notepad.exe'])
    else:
        #capture = cv2.VideoCapture(0)
        src = cv2.imread('R:\\hdf\\gamer.png')
        rows,cols = src.shape[:2]
        # Zoom out the picture
        res = cv2.pyrDown(src,dstsize=(int(rows/2), int(cols/2)))
        cv2.imshow("src",src)
        cv2.imshow("res",res)

        # Zoom in picture
        res = cv2.pyrUp(src,dstsize=(int(rows * 2),int(cols *2)))
        cv2.imshow("res2",res)


        print(src.shape)
        print(res.shape)
        cv2.waitKey()
        cv2.destroyAllWindows()

video.release()