import torch
import cv2
from datetime import datetime

# Definir las regiones de interés (ROIs) para los cajones de estacionamiento
# Estas coordenadas deben ser ajustadas visualmente
parking_spots = [
    [19, 29, 614, 688],   # Cajón 1
    [857, 12, 1118, 628],  # Cajón 2
    [1687, 210, 1902, 637],# Cajón 3
    [759, 769, 1074, 1049],# Cajón 4
]

# Cargar el modelo YOLOv5 preentrenado
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Definir el índice de la clase "car" en COCO
CAR_CLASS_ID = 2

# Inicializar el estado de los cajones de estacionamiento
parking_status = [False] * len(parking_spots)
parking_times = [None] * len(parking_spots)
leaving_times = [None] * len(parking_spots)

# Leer la imagen desde la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Realizar la detección
    results = model(frame)
    
    # Obtener los resultados de las detecciones
    labels, coords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    # Dibujar las ROIs de los cajones de estacionamiento
    for idx, spot in enumerate(parking_spots):
        cv2.rectangle(frame, (spot[0], spot[1]), (spot[2], spot[3]), (255, 0, 0), 2)
    
    # Lista para verificar si hay coches en los cajones
    cars_in_spots = [False] * len(parking_spots)
    
    # Procesar cada detección
    for i in range(len(labels)):
        if int(labels[i]) == CAR_CLASS_ID:
            x1, y1, x2, y2, conf = coords[i]
            if conf > 0.5:  # Umbral de confianza
                start_point = (int(x1 * frame.shape[1]), int(y1 * frame.shape[0]))
                end_point = (int(x2 * frame.shape[1]), int(y2 * frame.shape[0]))
                cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)
                
                # Verificar intersección con los cajones de estacionamiento
                for idx, spot in enumerate(parking_spots):
                    if (start_point[0] < spot[2] and end_point[0] > spot[0] and
                        start_point[1] < spot[3] and end_point[1] > spot[1]):
                        
                        cars_in_spots[idx] = True
                        
                        if not parking_status[idx]:  # Si el cajón estaba desocupado
                            parking_status[idx] = True
                            parking_times[idx] = datetime.now()
                            print(f'Cajón {idx+1} ocupado a las {parking_times[idx]}')
                        
                        cv2.putText(frame, "Ocupado", (spot[0], spot[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        cv2.rectangle(frame, (spot[0], spot[1]), (spot[2], spot[3]), (0, 0, 255), 2)
    
    # Verificar cajones que se han desocupado
    for idx, spot in enumerate(parking_spots):
        if parking_status[idx] and not cars_in_spots[idx]:
            parking_status[idx] = False
            leaving_times[idx] = datetime.now()
            time_spent = leaving_times[idx] - parking_times[idx]
            print(f'Cajón {idx+1} desocupado a las {leaving_times[idx]}. Tiempo ocupado: {time_spent}')
    
    # Mostrar la imagen con las detecciones y ROIs
    cv2.imshow('YOLOv5 Parking Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
