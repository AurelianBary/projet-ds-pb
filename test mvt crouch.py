import os
import sys
import time
import numpy as np
import cv2

#cap=cv2.VideoCapture(0)
cap=cv2.VideoCapture("crouch originale.mp4")

kernel_blur=15
seuil=15  
surface=1000
ret, originale=cap.read()
originale=cv2.cvtColor(originale, cv2.COLOR_BGR2GRAY)   #passe la vidéo en noir et blanc
originale=cv2.GaussianBlur(originale, (kernel_blur, kernel_blur), 0)
kernel_dilate=np.ones((5, 5), np.uint8)

#ajout variable pour ajouter le temps
start_time = time.time()

while True:
    ret, frame=cap.read() #permet de lire chaque frame de la vidéo une par une 
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (kernel_blur, kernel_blur), 0)
    mask=cv2.absdiff(originale, gray)
    mask=cv2.threshold(mask, seuil, 255, cv2.THRESH_BINARY)[1]
    mask=cv2.dilate(mask, kernel_dilate, iterations=3)
    contours, nada=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame_contour=frame.copy()
    
    #ajout du chronometre
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    for c in contours:
        cv2.drawContours(frame_contour, [c], 0, (0, 255, 0), 5)
        if cv2.contourArea(c)<surface:
            continue
        x, y, w, h=cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    originale=gray
    #cv2.putText(frame, "[o|l]seuil: {:d}  [p|m]blur: {:d}  [i|k]surface: {:d}".format(seuil, kernel_blur, surface), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
    cv2.putText(frame, "[o|l]seuil: {:d}  [p|m]flou: {:d}  [i|k]surface: {:d}  Temps: {:.2f} s".format(seuil, kernel_blur, surface, elapsed_time), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
    cv2.imshow("frame", frame)
    cv2.imshow("contour", frame_contour)
    cv2.imshow("mask", mask)
    intrus=0
    key=cv2.waitKey(30)&0xFF
    if key==ord('q'):
        break
    if key==ord('p'):
        kernel_blur=min(43, kernel_blur+2)
    if key==ord('m'):
        kernel_blur=max(1, kernel_blur-2)
    if key==ord('i'):
        surface+=1000
    if key==ord('k'):
        surface=max(1000, surface-1000)
    if key==ord('o'):
        seuil=min(255, seuil+1)
    if key==ord('l'):
        seuil=max(1, seuil-1)
        
        


cap.release()
cv2.destroyAllWindows()