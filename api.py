import mysql.connector
import cv2
import numpy as np
from threading import Thread
import time
import math

class VideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.ret, self.frame = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            self.ret, self.frame = self.stream.read()

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.stopped = True

# Carga los nombres de las clases para YOLO
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Índice de la clase "car" en coco.names
CAR_CLASS_ID = classes.index("car")

# Configuración de YOLO
net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")

# Verifica si CUDA está disponible y úsala si es posible
if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().reshape(-1)]

# Inicializa la cámara USB (src=0 para la primera cámara USB conectada)
cap = VideoStream(src=0).start()

entrada = 0
salida = 0
entradas_tiempos = []
salidas_tiempos = []

# Diccionario para almacenar el último centro y el tiempo de detección de cada objeto
last_detection = {}
car_ids = {}  # Diccionario para almacenar los IDs de los autos
current_car_id = 1  # Variable para asignar un nuevo ID a cada auto que entra

confidence_threshold = 0.5  # Valor inicial del umbral de confianza

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",       # Cambia esto si tu servidor MySQL no está en localhost
    user="root",            # Cambia esto por tu usuario de MySQL
    password="",            # Cambia esto por tu contraseña de MySQL
    database="parking"
)

cursor = db.cursor()

def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo obtener el frame. Reabriendo el stream...")
        cap.stop()
        cap = VideoStream(src=1).start()
        continue

    # Redimensionar el frame para mejorar la velocidad (opcional)
    frame = cv2.resize(frame, (640, 360))
    height, width, channels = frame.shape
    line_position_top = height // 4  # Posición de la línea de segmentación superior
    line_position_bottom = 3 * height // 4  # Posición de la línea de segmentación inferior

    # Detectando objetos con YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    current_detection = {}

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold and class_id == CAR_CLASS_ID:
                # Auto detectado
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectángulo delimitador del auto detectado
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Determinar si está en la parte superior o inferior de la línea de segmentación
                if center_y < line_position_top:
                    color = (0, 255, 0)  # Verde para la parte superior
                elif center_y > line_position_bottom:
                    color = (0, 0, 255)  # Rojo para la parte inferior
                else:
                    color = (0, 255, 255)  # Amarillo para el medio

                # Dibujar el rectángulo delimitador y la etiqueta en el frame
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, classes[class_id], (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)

                # Guardar el centro del auto y el tiempo actual
                current_center = (center_x, center_y)
                current_detection[current_center] = (current_center, time.time())

    # Asociar detecciones actuales con detecciones anteriores
    new_car_ids = {}
    for current_center, (center, current_time) in current_detection.items():
        min_distance = float('inf')
        assigned_car_id = None

        for last_center, car_id in car_ids.items():
            distance = euclidean_distance(current_center, last_center)
            if distance < min_distance:
                min_distance = distance
                assigned_car_id = car_id

        if assigned_car_id is not None and min_distance < 50:  # Ajustar umbral de distancia si es necesario
            new_car_ids[current_center] = assigned_car_id
        else:
            new_car_ids[current_center] = current_car_id
            car_ids[current_center] = current_car_id  # Asignar nuevo ID al auto
            current_car_id += 1

    car_ids = new_car_ids

    # Contar entradas y salidas
    for current_center, (center, current_time) in current_detection.items():
        car_id = car_ids[current_center]

        if car_id in last_detection:
            last_center, last_time = last_detection[car_id]
            if last_center[1] < line_position_top and center[1] >= line_position_top:
                entrada += 1
                entrada_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
                entradas_tiempos.append(entrada_time)
                print(f"Auto {car_id} entro. Hora: {entrada_time}")
                # Convertir car_id a str
                car_id_str = str(car_id)
                # Insertar registro en la base de datos
                cursor.execute("INSERT INTO estacionamiento_entrada (id_carro, Hora_Entrada) VALUES (%s, %s)", (car_id_str, entrada_time))
                db.commit()
            elif last_center[1] > line_position_bottom and center[1] <= line_position_bottom:
                salida += 1
                salida_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
                salidas_tiempos.append(salida_time)
                print(f"Auto {car_id} salio. Hora: {salida_time}")
                # Convertir car_id a str
                car_id_str = str(car_id)
                # Actualizar o insertar registro en la tabla estacionamiento_salida
                cursor.execute("UPDATE estacionamiento_salida SET Hora_Salida = %s WHERE id_carro = %s AND Hora_Salida IS NULL", (salida_time, car_id_str))
                db.commit()
                if cursor.rowcount == 0:
                    # Si no se actualizó ningún registro, insertar uno nuevo
                    cursor.execute("INSERT INTO estacionamiento_salida (id_carro, Hora_Salida) VALUES (%s, %s)", (car_id_str, salida_time))
                    db.commit()

    # Actualizar las detecciones
    last_detection = {car_id: (center, current_time) for center, (center, current_time) in current_detection.items()}

    # Dibujar las líneas de segmentación
    cv2.line(frame, (0, line_position_top), (width, line_position_top), (255, 255, 255), 2)
    cv2.line(frame, (0, line_position_bottom), (width, line_position_bottom), (255, 255, 255), 2)

    # Mostrar el conteo de entrada y salida en el frame
    cv2.putText(frame, f'Entrada: {entrada}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f'Salida: {salida}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Mostrar el frame procesado
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1)
    if key == 27:  # Presiona 'Esc' para salir
        break

# Liberar recursos
cap.stop()
cv2.destroyAllWindows()
cursor.close()
db.close()
