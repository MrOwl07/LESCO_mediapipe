import cv2
import mediapipe as mp
import csv

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Letra actual
letra_actual = "A"

# Abrir archivo CSV
with open('prueba_final.csv', mode='a', newline='') as archivo:
    escritor = csv.writer(archivo)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = hands.process(rgb)

        if resultado.multi_hand_landmarks:
            for hand_landmarks in resultado.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                keypoints = []
                for punto in hand_landmarks.landmark:
                    keypoints.extend([punto.x, punto.y, punto.z])

                # Guardar solo si se presiona ESPACIO
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    escritor.writerow([letra_actual] + keypoints)
                    print(f"[✔] Guardado gesto para letra: {letra_actual}")

        # Mostrar letra actual
        cv2.putText(frame, f"Letra actual: {letra_actual} (cambia con teclas A-Z)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.imshow("Captura de Letras", frame)

        # Leer entrada del teclado para cambiar letra
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord(','):  # Coma para salir
            break
        elif chr(tecla).upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            letra_actual = chr(tecla).upper()

cap.release()
cv2.destroyAllWindows()
