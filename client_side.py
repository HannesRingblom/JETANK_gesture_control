import cv2
import mediapipe as mp
import time
import socket

HOST = "XXX.XX.XX.X"
PORT = 12000
cap = cv2.VideoCapture(0)

# Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

fingers_right = []
fingers_left = []
hand_count = 0
command_count = 0
command_to_call = ''
string_command = ''
last_command = ''
start_time = 0
pTime, cTime = 0, 9
counta = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    print("Trying to connect")
    s.connect((HOST, PORT))
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        # Check for found hands
        if results.multi_hand_landmarks:
            counta += 1

            # Adds thumb and palm och the hand(s) found
            for handLms in results.multi_hand_landmarks:
                for landmark_id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if hand_count == 0:
                        if landmark_id == 0 or landmark_id == 4:
                            fingers_left.append(lm)
                            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    else:
                        if landmark_id == 0 or landmark_id == 4:
                            fingers_right.append(lm)
                            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

                hand_count = 1
            hand_count = 0
        if counta % 10 == 0:

            # check if there are two hands in the image
            if fingers_right and fingers_left:

                # Determining whether the thumbs are leveled with, above or below the base of the palm
                # This determines which command should later be sent through the socket
                if fingers_right[1].y < (fingers_right[0].y - 0.1):
                    if fingers_left[1].y < (fingers_left[0].y - 0.1):
                        command_to_call = 'w'
                        command_count += 1
                        string_command = "BOTH THUMBS UP"
                        print("Both UP")
                    elif fingers_left[1].y > (fingers_left[0].y + 0.1):
                        command_to_call = 'a'
                        command_count += 1
                        string_command = "RIGHT UP __ LEFT DOWN"
                        print("Right UP   Left DOWN")
                elif fingers_right[1].y > (fingers_right[0].y + 0.1):
                    if fingers_left[1].y > (fingers_left[0].y + 0.1):
                        command_to_call = 's'
                        command_count += 1
                        string_command = "BOTH THUMBS DOWN"
                        print("Both DOWN")
                    elif fingers_left[1].y < (fingers_left[0].y - 0.1):
                        command_to_call = 'd'
                        command_count += 1
                        string_command = "RIGHT DOWN __ LEFT UP"
                        print("Right DOWN   Left UP")
                elif (fingers_right[0].y - 0.08) < fingers_right[1].y < (fingers_right[0].y + 0.08):
                    if (fingers_left[0].y - 0.08) < fingers_left[1].y < (fingers_left[0].y + 0.08):
                        if abs(fingers_left[1].x - fingers_right[1].x) < 0.2:
                            command_to_call = 'g'
                            command_count += 1
                            string_command = "THUMBS TOGETHER"
                            print("THUMBS TOGETHER")
                        else:
                            command_to_call = 'l'
                            command_count += 1
                            string_command = "THUMBS APART"
                            print("THUMBS APART")

            # If only one hand is present in the image
            elif fingers_left:
                if fingers_left[1].y < (fingers_left[0].y - 0.1):
                    command_to_call = 'c'
                    command_count += 1
                    string_command = "ONE THUMB UP"
                    print("ONE THUMB UP")
                elif fingers_left[1].y > (fingers_left[0].y + 0.1):
                    command_to_call = 'x'
                    command_count += 1
                    string_command = "ONE THUMB DOWN"
                    print("ONE THUMB DOWN")

        # Counts the times the same finger combination is present in a row
        if last_command != command_to_call:
            command_count = 1
            last_command = command_to_call

        # Send the command through the socket when found a specified amount of times
        if command_to_call == 'c' or command_to_call == 'x':
            if command_count == 6:
                print("Sending ")
                s.sendto(command_to_call.encode(), (HOST, PORT))
                command_count = 0
        else:
            if command_count == 2:
                print("Sending ")
                s.sendto(command_to_call.encode(), (HOST, PORT))
                command_count = 0

        # Calculating fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        flipped = cv2.flip(img, 1)
        cv2.putText(flipped, "FPS: " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                    (100, 150, 100), 2)
        cv2.putText(flipped, "Last command sent: " + string_command, (200, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                    (100, 150, 100), 2)

        # Reset the found fingers
        fingers_right = []
        fingers_left = []
        cv2.imshow('Hand Steering', flipped)
        if cv2.waitKey(1) == 27:
            break
    if cv2.waitKey(1) == 27:
        break
s.close()
cap.release()
cv2.destroyAllWindows()
