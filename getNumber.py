import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHandLms(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList
def getNumber(ar):
    s = ""
    for i in ar:
        s += str(ar[i])
    if (s == "00000"):
        return (0)
    elif (s == "01000"):
        return (1)
    elif (s == "01100"):
        return (2)
    elif (s == "01110"):
        return (3)
    elif (s == "01111"):
        return (4)
    elif (s == "11111"):
        return (5)
    elif (s == "01001"):
        return (6)
    elif (s == "01101"):
        return (7)

HandDetector = handDetector(detectionCon=0.75)
webcam = cv2.VideoCapture(0)

while True:
    s = time.time()
    ret, img = webcam.read()

    if not ret:
        break
    img = HandDetector.findHandLms(img, draw=True)
    lmList = HandDetector.findPosition(img, draw=False)
    # print(lmList)
    tipId = [4, 8, 12, 16, 20]
    if (len(lmList) != 0):
        fingers = []
        # thumb
        if (lmList[tipId[0]][1] > lmList[tipId[0] - 1][1]):
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 fingers
        for id in range(1, len(tipId)):

            if (lmList[tipId[id]][2] < lmList[tipId[id] - 2][2]):
                fingers.append(1)

            else:
                fingers.append(0)

        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(getNumber(fingers)), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 20)

    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    cv2.imshow("Number", img)

webcam.release()
cv2.destroyAllWindows()
