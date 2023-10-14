
import cv2
import os
import sys
import time
import numpy as np

### Part1: réduction des fps

# Ouvrir la vidéo d'origine
video_path = 'crouch originale.mp4'
cap = cv2.VideoCapture(video_path)

fps_origine = cap.get(cv2.CAP_PROP_FPS)
fps_origine = int(fps_origine)

# Créer une vidéo de sortie avec un nombre de frames réduit
output_path = 'crouch réduit (5fps).mp4'
fps_reduit = 5  # Remplacez 10 par le nombre de frames par seconde souhaité

# Récupérer les dimensions de la vidéo d'origine
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Créer un objet VideoWriter pour écrire la vidéo de sortie
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps_reduit, (frame_width, frame_height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Écrire la frame dans la vidéo de sortie
    out.write(frame)

    # Ignorer un certain nombre de frames pour réduire le nombre de frames par seconde
    for _ in range(fps_origine - fps_reduit - 1):
        cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()

mult_speed_time = fps_origine/fps_reduit

### Part2: identification du mouvement

#cap=cv2.VideoCapture(0)
cap=cv2.VideoCapture("crouch réduit (5fps).mp4")

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
    cv2.putText(frame, "[o|l]seuil: {:d}  [p|m]blur: {:d}  [i|k]surface: {:d}  Temps: {:.2f} s".format(seuil, kernel_blur, surface, elapsed_time), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
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
