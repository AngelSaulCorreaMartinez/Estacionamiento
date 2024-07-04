import torch
import cv2
from datetime import datetime
import mysql.connector

# Definir las regiones de interés (ROIs) para los cajones de estacionamiento
cajones_estacionamiento = [
    [19, 29, 614, 688],   # Cajón 1
    [857, 12, 1118, 628],  # Cajón 2
    [1687, 210, 1902, 637],# Cajón 3
    [759, 769, 1074, 1049],# Cajón 4
]

# Cargar el modelo YOLOv5 preentrenado
modelo = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Definir el índice de la clase "car" en COCO
ID_CLASE_CARRO = 2

# Inicializar el estado de los cajones de estacionamiento
estado_cajones = [False] * len(cajones_estacionamiento)
tiempos_entrada = [None] * len(cajones_estacionamiento)
tiempos_salida = [None] * len(cajones_estacionamiento)

# Configurar la conexión a MySQL
conn = mysql.connector.connect(
    host="10.11.6.32",
    user="Pepillo",       # Cambia a tu usuario
    password="chat",  # Cambia a tu contraseña
    database="estacionamiento"
)
cursor = conn.cursor()

# Leer la imagen desde la cámara
captura = cv2.VideoCapture(0)

while True:
    lectura_correcta, fotograma = captura.read()
    if not lectura_correcta:
        break

    # Realizar la detección
    resultados = modelo(fotograma)
    
    # Obtener los resultados de las detecciones
    etiquetas, coordenadas = resultados.xyxyn[0][:, -1], resultados.xyxyn[0][:, :-1]

    # Dibujar las ROIs de los cajones de estacionamiento
    for idx, spot in enumerate(cajones_estacionamiento):
        cv2.rectangle(fotograma, (spot[0], spot[1]), (spot[2], spot[3]), (255, 0, 0), 2)
    
    # Lista para verificar si hay coches en los cajones
    coches_en_cajones = [False] * len(cajones_estacionamiento)
    
    # Procesar cada detección
    for i in range(len(etiquetas)):
        if int(etiquetas[i]) == ID_CLASE_CARRO:
            x1, y1, x2, y2, conf = coordenadas[i]
            if conf > 0.5:  # Umbral de confianza
                start_point = (int(x1 * fotograma.shape[1]), int(y1 * fotograma.shape[0]))
                end_point = (int(x2 * fotograma.shape[1]), int(y2 * fotograma.shape[0]))
                cv2.rectangle(fotograma, start_point, end_point, (0, 255, 0), 2)
                
                # Verificar intersección con los cajones de estacionamiento
                for idx, spot in enumerate(cajones_estacionamiento):
                    if (start_point[0] < spot[2] and end_point[0] > spot[0] and
                        start_point[1] < spot[3] and end_point[1] > spot[1]):
                        
                        coches_en_cajones[idx] = True
                        
                        if not estado_cajones[idx]:  # Si el cajón estaba desocupado
                            estado_cajones[idx] = True
                            tiempos_entrada[idx] = datetime.now()
                            print(f'Cajón {idx+1} ocupado a las {tiempos_entrada[idx]}')
                            cursor.execute("INSERT INTO ocupacion_cajones (cajon, tiempo_entrada) VALUES (%s, %s)", (idx+1, tiempos_entrada[idx]))
                            conn.commit()
                        
                        cv2.putText(fotograma, "Ocupado", (spot[0], spot[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        cv2.rectangle(fotograma, (spot[0], spot[1]), (spot[2], spot[3]), (0, 0, 255), 2)
    
    # Verificar cajones que se han desocupado
    for idx, spot in enumerate(cajones_estacionamiento):
        if estado_cajones[idx] and not coches_en_cajones[idx]:
            estado_cajones[idx] = False
            tiempos_salida[idx] = datetime.now()
            tiempo_estancia = tiempos_salida[idx] - tiempos_entrada[idx]
            print(f'Cajón {idx+1} desocupado a las {tiempos_salida[idx]}. Tiempo ocupado: {tiempo_estancia}')
            cursor.execute("UPDATE ocupacion_cajones SET tiempo_salida = %s, tiempo_estancia = %s WHERE cajon = %s AND tiempo_salida IS NULL", 
                           (tiempos_salida[idx], tiempo_estancia, idx+1))
            conn.commit()
    
    # Mostrar la imagen con las detecciones y ROIs
    cv2.imshow('YOLOv5 Parking Detection', fotograma)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()
