import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            fingers = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
                
                fingers.append((cx, cy))

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            if len(fingers) == 21:
                thumb_tip_x, thumb_tip_y = fingers[4]
                index_tip_x, index_tip_y = fingers[8]
                middle_tip_x, middle_tip_y = fingers[12]
                ring_tip_x, ring_tip_y = fingers[16]
                pinky_tip_x, pinky_tip_y = fingers[20]

                thumb_index_dist = ((thumb_tip_x - index_tip_x)**2 + (thumb_tip_y - index_tip_y)**2)**0.5
                thumb_middle_dist = ((thumb_tip_x - middle_tip_x)**2 + (thumb_tip_y - middle_tip_y)**2)**0.5
                thumb_ring_dist = ((thumb_tip_x - ring_tip_x)**2 + (thumb_tip_y - ring_tip_y)**2)**0.5
                thumb_pinky_dist = ((thumb_tip_x - pinky_tip_x)**2 + (thumb_tip_y - pinky_tip_y)**2)**0.5

                finger_name = ""
                if thumb_index_dist < thumb_middle_dist and thumb_index_dist < thumb_ring_dist and thumb_index_dist < thumb_pinky_dist:
                    finger_name = "Thumb"
                elif thumb_middle_dist < thumb_index_dist and thumb_middle_dist < thumb_ring_dist and thumb_middle_dist < thumb_pinky_dist:
                    finger_name = "Middle Finger"
                elif thumb_ring_dist < thumb_index_dist and thumb_ring_dist < thumb_middle_dist and thumb_ring_dist < thumb_pinky_dist:
                    finger_name = "Ring Finger"
                elif thumb_pinky_dist < thumb_index_dist and thumb_pinky_dist < thumb_middle_dist and thumb_pinky_dist < thumb_ring_dist:
                    finger_name = "Pinky Finger"

                letter = ""
                if thumb_index_dist > thumb_middle_dist and thumb_ring_dist > thumb_middle_dist and thumb_pinky_dist > thumb_middle_dist:
                    letter = "A"
                elif thumb_index_dist < thumb_middle_dist and thumb_ring_dist > thumb_middle_dist and thumb_pinky_dist > thumb_middle_dist:
                    letter = "B"
                elif thumb_index_dist < thumb_middle_dist and thumb_ring_dist < thumb_middle_dist and thumb_pinky_dist > thumb_middle_dist:
                    letter = "C"
                elif thumb_index_dist < thumb_middle_dist and thumb_ring_dist < thumb_middle_dist and thumb_pinky_dist < thumb_middle_dist:
                    letter = "D"

                cv2.putText(img, finger_name, (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
                cv2.putText(img, letter, (10, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
