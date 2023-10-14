import cv2

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

print("terminada")