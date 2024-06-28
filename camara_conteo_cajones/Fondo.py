import cv2

# Crear el objeto de sustracción de fondo
fgbg = cv2.createBackgroundSubtractorMOG2()

# Leer la imagen desde la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Aplicar la sustracción de fondo
    fgmask = fgbg.apply(frame)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Ignorar pequeñas áreas de movimiento
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Mostrar la imagen original con las detecciones de movimiento
    cv2.imshow('Motion Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
