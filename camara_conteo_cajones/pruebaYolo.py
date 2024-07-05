import torch
import cv2
from datetime import datetime
import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Cambia esto si tu servidor no está en localhost
            database='parkingdb',  # Nombre de tu base de datos
            user='root',  # Tu usuario de MySQL
            password=''  # Tu contraseña de MySQL
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    except Error as e:
        print("Error al conectar a la base de datos", e)
        return None

def insert_parking_record(connection, nivel, cajon, hora_entrada):
    cursor = connection.cursor()
    query = "INSERT INTO individual (Nivel, Cajon, Hora_Entrada) VALUES (%s, %s, %s)"
    cursor.execute(query, (nivel, cajon, hora_entrada))
    connection.commit()
    return cursor.lastrowid

def update_parking_record(connection, id_record, hora_salida):
    cursor = connection.cursor()
    query = "UPDATE individual SET Hora_Salida = %s WHERE ID = %s"
    cursor.execute(query, (hora_salida, id_record))
    connection.commit()

# Definir las regiones de interés (ROIs) para los cajones de estacionamiento
# Estas coordenadas deben ser ajustadas visualmente
parking_spots = [
    [40, 30, 221, 124],   # Cajón 1
    [452, 36, 583, 118],  # Cajón 2
    [20, 201, 259, 321],# Cajón 3
    [446, 232, 651, 360],# Cajón 4
]

# Cargar el modelo YOLOv5 preentrenado
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Definir el índice de la clase "car" en COCO
CAR_CLASS_ID = 2

# Inicializar el estado de los cajones de estacionamiento
parking_status = [False] * len(parking_spots)
parking_times = [None] * len(parking_spots)
leaving_times = [None] * len(parking_spots)
record_ids = [None] * len(parking_spots)

# Conectar a la base de datos
connection = connect_db()

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
                            record_ids[idx] = insert_parking_record(connection, 'N1', idx + 1, parking_times[idx])
                            print(f'Cajón {idx+1} ocupado a las {parking_times[idx]}')
                        
                        cv2.putText(frame, "Ocupado", (spot[0], spot[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        cv2.rectangle(frame, (spot[0], spot[1]), (spot[2], spot[3]), (0, 0, 255), 2)
    
    # Verificar cajones que se han desocupado
    for idx, spot in enumerate(parking_spots):
        if parking_status[idx] and not cars_in_spots[idx]:
            parking_status[idx] = False
            leaving_times[idx] = datetime.now()
            time_spent = leaving_times[idx] - parking_times[idx]
            update_parking_record(connection, record_ids[idx], leaving_times[idx])
            print(f'Cajón {idx+1} desocupado a las {leaving_times[idx]}. Tiempo ocupado: {time_spent}')
    
    # Mostrar la imagen con las detecciones y ROIs
    cv2.imshow('YOLOv5 Parking Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if connection.is_connected():
    connection.close()
    print("Conexión a la base de datos cerrada")