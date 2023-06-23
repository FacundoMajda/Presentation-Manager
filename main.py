from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
import pyautogui

# Parámetros
gestureThreshold = 300
folderPath = "Presentation"
zoomScale = 0.1
rotationAngle = 10

# Obtener resolución de pantalla actual o solicitarla al usuario
try:
    screenWidth, screenHeight = pyautogui.size()
except:
    screenWidth = int(input("Ingresa el ancho de la pantalla: "))
    screenHeight = int(input("Ingresa el alto de la pantalla: "))

# Calcular tamaño de la ventana de slides y cámara pequeña
windowWidth = int(screenWidth * 0.85)
windowHeight = int(screenHeight * 0.85)
cameraWidth = int(screenWidth * 0.15)
cameraHeight = int(screenHeight * 0.15)
cameraX = screenWidth - cameraWidth
cameraY = 0

# Inicializar captura de video
cap = cv2.VideoCapture(0)
cap.set(3, windowWidth)
cap.set(4, windowHeight)

# Inicializar detector de manos
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
imgList = []
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
# Ancho y alto de la imagen pequeña
hs, ws = int(windowHeight * 0.15), int(windowWidth * 0.15)

# Obtener lista de imágenes de la presentación
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

# Crear botón llamativo
buttonSize = 100
buttonMargin = 20
buttonColor = (255, 0, 0)
buttonX = screenWidth - buttonSize - buttonMargin
buttonY = buttonMargin

while True:
    # Obtener frame de la cámara
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    # Encontrar la mano y sus landmarks
    hands, img = detectorHand.findHands(img)  # con dibujos
    # Dibujar línea de umbral de gesto
    cv2.line(img, (0, gestureThreshold),
             (windowWidth, gestureThreshold), (0, 255, 0), 10)

    if hands and not buttonPressed:  # Si se detecta la mano
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # Lista de 21 puntos de referencia
        fingers = detectorHand.fingersUp(hand)  # Lista de dedos levantados

        # Limitar los valores para facilitar el dibujo
        xVal = int(np.interp(lmList[8][0], [
                   windowWidth // 2, windowWidth], [0, windowWidth]))
        yVal = int(np.interp(lmList[8][1], [
                   150, windowHeight-150], [0, windowHeight]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:  # Si la mano está a la altura de la cara
            if fingers == [1, 0, 0, 0, 0]:
                print("Izquierda")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:
                print("Derecha")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            print(annotationNumber)
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True

        if fingers == [1, 1, 0, 0, 0]:  # Zoom de acercamiento
            zoomScale += 0.01
            if zoomScale > 2.0:
                zoomScale = 2.0

        if fingers == [1, 0, 0, 0, 0]:  # Zoom de alejamiento
            zoomScale -= 0.01
            if zoomScale < 0.1:
                zoomScale = 0.1

        if fingers == [0, 1, 1, 0, 0]:  # Rotación en sentido horario
            rotationAngle += 1

        if fingers == [0, 0, 0, 0, 1]:  # Rotación en sentido antihorario
            rotationAngle -= 1

    else:
        annotationStart = False

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(imgCurrent, annotation[j - 1],
                         annotation[j], (0, 0, 200), 12)

    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    # Redimensionar ventanas según la resolución de pantalla
    resizedSlides = cv2.resize(imgCurrent, (windowWidth, windowHeight))
    resizedCamera = cv2.resize(img, (cameraWidth, cameraHeight))

    # Dibujar botón llamativo
    cv2.rectangle(resizedSlides, (buttonX, buttonY), (buttonX +
                  buttonSize, buttonY + buttonSize), buttonColor, cv2.FILLED)
    cv2.putText(resizedSlides, "Modo Dibujo", (buttonX + int(buttonSize * 0.1), buttonY + int(buttonSize * 0.5)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)

    cv2.imshow("Slides", resizedSlides)
    cv2.imshow("Camera", resizedCamera)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cv2.destroyAllWindows()
