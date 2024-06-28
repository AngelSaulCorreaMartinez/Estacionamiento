import cv2

# Variables globales para almacenar las coordenadas del rectángulo
drawing = False  # Verdadero si el ratón está presionado
ix, iy = -1, -1
rois = []

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, rois

    # Si se presiona el botón izquierdo del ratón, se inicia el dibujo del rectángulo
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    # Si se suelta el botón izquierdo del ratón, se finaliza el dibujo del rectángulo
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rois.append((ix, iy, x, y))
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

# Inicializar la captura de video
cap = cv2.VideoCapture(0)

# Leer una imagen para definir las ROIs
ret, img = cap.read()
cv2.namedWindow('Definir ROIs')
cv2.setMouseCallback('Definir ROIs', draw_rectangle)

while True:
    cv2.imshow('Definir ROIs', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()

# Mostrar las ROIs definidas
print("ROIs definidas:")
for roi in rois:
    print(roi)

# Guardar las ROIs en una lista para usarlas en la detección
parking_spots = rois

# Ahora puedes usar la lista `parking_spots` en tu código de detección
