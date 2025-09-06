import cv2
import mediapipe as mp
import csv

# Inicialización de MediaPipe para la detección de manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,  # Modo de imagen estática desactivado para video en tiempo real
                       max_num_hands=1,         # Solo se detecta una mano a la vez
                       min_detection_confidence=0.7)  # Confianza mínima para la detección
mp_draw = mp.solutions.drawing_utils  # Utilidad para dibujar las conexiones de la mano

# Inicializa la cámara web (índice 0 por defecto)
cap = cv2.VideoCapture(0)

# Variable para almacenar la letra actual que se está capturando
letra_actual = "A"

<<<<<<< HEAD
# Abre (o crea) el archivo CSV en modo de añadir ('a') para guardar los datos
with open('prueba.csv', mode='a', newline='') as archivo:
=======
# Abrir archivo CSV
with open('prueba_final.csv', mode='a', newline='') as archivo:
>>>>>>> fb2e2c4d97d633a45ab88d8a91b6887c347e44e6
    escritor = csv.writer(archivo)

    while True:
        # Captura un frame de la cámara
        ret, frame = cap.read()
        if not ret:
            break  # Si no se pudo capturar el frame, termina el bucle

        # Invierte la imagen horizontalmente para que sea como un espejo
        frame = cv2.flip(frame, 1)
        # Convierte la imagen de BGR (OpenCV) a RGB (MediaPipe)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Procesa la imagen para detectar las manos
        resultado = hands.process(rgb)

        # Si se detectan manos en el frame
        if resultado.multi_hand_landmarks:
            for hand_landmarks in resultado.multi_hand_landmarks:
                # Dibuja los puntos y conexiones de la mano sobre la imagen
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                keypoints = []  # Lista para almacenar las coordenadas de los puntos clave
                for punto in hand_landmarks.landmark:
                    # Agrega las coordenadas x, y, z de cada punto de la mano
                    keypoints.extend([punto.x, punto.y, punto.z])

                # Si se presiona la barra espaciadora, guarda los datos en el CSV
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    escritor.writerow([letra_actual] + keypoints)
                    print(f"[✔] Guardado gesto para letra: {letra_actual}")

        # Muestra la letra actual en pantalla y cómo cambiarla
        cv2.putText(frame, f"Letra actual: {letra_actual} (cambia con teclas A-Z)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        # Muestra la imagen en una ventana llamada 'Captura de Letras'
        cv2.imshow("Captura de Letras", frame)

        # Lee la entrada del teclado para cambiar la letra o salir
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord(','):  # Si se presiona la coma, termina el bucle
            break
        elif chr(tecla).upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            # Si se presiona una letra, actualiza la letra actual
            letra_actual = chr(tecla).upper()

# Libera la cámara y cierra todas las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()
