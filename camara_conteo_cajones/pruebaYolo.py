import torch
import cv2
import threading
from datetime import datetime

# Definir las regiones de interés (ROIs) para los cajones de estacionamiento
parking_spots = [
    [19, 29, 614, 688],   # Cajón 1
    [857, 12, 1118, 628],  # Cajón 2
    [1687, 210, 1902, 637],# Cajón 3
    [759, 769, 1074, 1049],# Cajón 4
]

# Verificar si la GPU está disponible
if torch.backends.mps.is_available():
    device = torch.device('mps')
elif torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')

print(f'Usando el dispositivo: {device}')

# Cargar el modelo YOLOv5 preentrenado y moverlo al dispositivo
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device).eval()

# Definir el índice de la clase "car" en COCO
CAR_CLASS_ID = 2

# Inicializar el estado de los cajones de estacionamiento
parking_status = [False] * len(parking_spots)
parking_times = [None] * len(parking_spots)
leaving_times = [None] * len(parking_spots)

# URL RTSP de tu cámara con usuario y contraseña
usuario = "admin"
contraseña = "Estacionamiento2"
direccion_ip = "169.254.10.144"
puerto_rtsp = "554"

# Formato de la URL RTSP
rtsp_url = f"rtsp://{usuario}:{contraseña}@{direccion_ip}:{puerto_rtsp}/Streaming/Channels/102"

# Inicializar la captura de video
cap = cv2.VideoCapture(rtsp_url)

# Verificar si la cámara RTSP está abierta
if not cap.isOpened():
    print("Error al abrir la cámara RTSP.")
    exit()

# Establecer la resolución de entrada para reducir la carga de procesamiento
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Configurar el frame rate
cap.set(cv2.CAP_PROP_FPS, 15)

# Variable para almacenar el último frame capturado
latest_frame = None
lock = threading.Lock()

def capture_frames():
    global latest_frame
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al leer el frame de la cámara.")
            break
        with lock:
            latest_frame = frame

# Iniciar el hilo de captura de frames
threading.Thread(target=capture_frames, daemon=True).start()

while True:
    with lock:
        frame = latest_frame

    if frame is None:
        continue

    # Redimensionar el frame para procesamiento más rápido
    frame_resized = cv2.resize(frame, (640, 480))

    # Convertir la imagen a RGB y luego a tensor, y mover al dispositivo
    img = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    img = torch.from_numpy(img).to(device).float() / 255.0  # Normalizar la imagen
    img = img.permute(2, 0, 1).unsqueeze(0)  # cambiar a formato de PyTorch y añadir dimensión de batch

    # Realizar la detección
    with torch.no_grad():
        results = model(img)[0]

    # Obtener los resultados de las detecciones y moverlos de vuelta a la CPU
    labels = results[:, -1].cpu()
    coords = results[:, :-1].cpu()

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