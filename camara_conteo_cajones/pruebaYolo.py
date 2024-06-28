import torch
import cv2

# Definir las regiones de interés (ROIs) para los cajones de estacionamiento
# Estas coordenadas deben ser ajustadas visualmente
parking_spots = [
    [47, 211, 241, 560],  # Cajón 1
    [522, 289, 901, 811], # Cajón 2
    [1132, 487, 1664, 889], # Cajón 3
    [1634, 261, 1861, 454], # Cajón 4
]

# Cargar el modelo YOLOv5 preentrenado
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Definir el índice de la clase "car" en COCO
CAR_CLASS_ID = 2

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
    for spot in parking_spots:
        cv2.rectangle(frame, (spot[0], spot[1]), (spot[2], spot[3]), (255, 0, 0), 2)
    
    # Dibujar las cajas de detección en la imagen y verificar intersección con los cajones
    for i in range(len(labels)):
        if int(labels[i]) == CAR_CLASS_ID:
            x1, y1, x2, y2, conf = coords[i]
            if conf > 0.5:  # Umbral de confianza
                start_point = (int(x1 * frame.shape[1]), int(y1 * frame.shape[0]))
                end_point = (int(x2 * frame.shape[1]), int(y2 * frame.shape[0]))
                cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)
                cv2.putText(frame, f'Car {conf:.2f}', start_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                # Verificar intersección con los cajones de estacionamiento
                for spot in parking_spots:
                    if (start_point[0] < spot[2] and end_point[0] > spot[0] and
                        start_point[1] < spot[3] and end_point[1] > spot[1]):
                        cv2.putText(frame, "Ocupado", (spot[0], spot[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        cv2.rectangle(frame, (spot[0], spot[1]), (spot[2], spot[3]), (0, 0, 255), 2)
    
    # Mostrar la imagen con las detecciones y ROIs
    cv2.imshow('YOLOv5 Parking Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
