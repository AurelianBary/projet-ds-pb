
import cv2
import os

# Ouvrir la vidéo
video_capture = cv2.VideoCapture('crouch réduit (5fps).mp4')

# Chemin du dossier de sortie pour les images PNG
output_folder = 'dossier stockage frame'

# Vérifiez si le dossier de sortie existe, sinon, créez-le
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Liste pour stocker les frames

nombre_frame = []
frame_count = 0
while True:
    # Lire le frame suivant
    ret, frame = video_capture.read()
    
    # Vérifier si la lecture est terminée
    if not ret:
        break
    
    nombre_frame.append(1)
    # Construisez le nom de fichier pour chaque image PNG
    filename = f"{output_folder}/frame_{frame_count:04d}.png"
    # Construisez le nom de fichier pour chaque image PNG
    cv2.imwrite(filename, frame)
    frame_count += 1

# Fermer la capture vidéo
video_capture.release()
cv2.destroyAllWindows()

# Maintenant, "frames" contient toutes les frames de la vidéo
print(len(nombre_frame))
print("finito")