import cv2
import mediapipe as mp
import numpy as np
import time
from collections import Counter
import joblib
import pickle
import pandas as pd

# Cargar el modelo entrenado
modelo = joblib.load('modelo_letras.pkl')

# Cargar el LabelEncoder
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Iniciar captura de video
cap = cv2.VideoCapture(0)

palabra = []

print("Presiona 'ESPACIO' para capturar una letra (5 segundos)")
print("Presiona 'ESC' para salir y mostrar la palabra final")

while True:
    predicciones = []
    letra_final = ''

    # Esperar que el usuario presione ESPACIO para iniciar la captura de una letra
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.putText(frame, "Presiona ESPACIO para capturar letra (5s) o ESC para terminar", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Captura Letra", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            cap.release()
            cv2.destroyAllWindows()
            print("Palabra final:", ''.join(palabra))
            exit()

        if key == 32:  # ESPACIO
            print("Capturando letra por 5 segundos...")
            inicio = time.time()
            while time.time() - inicio < 5:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        keypoints = []
                        for lm in hand_landmarks.landmark:
                            keypoints.extend([lm.x, lm.y, lm.z])

                        if len(keypoints) == modelo.n_features_in_:
                            # Crear DataFrame con nombres de columnas esperados
                            df = pd.DataFrame([keypoints], columns=[f'col{i}' for i in range(1, 64)])
                            pred = modelo.predict(df)[0]
                            letra = label_encoder.inverse_transform([pred])[0]
                            predicciones.append(letra)

                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                tiempo_restante = 5 - int(time.time() - inicio)
                cv2.putText(frame, f"Tiempo restante: {tiempo_restante}s", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                cv2.imshow("Captura Letra", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            if predicciones:
                letra_final = Counter(predicciones).most_common(1)[0][0]
                palabra.append(letra_final)
                print(f"Letra detectada: {letra_final}")
            else:
                print("No se detectó letra. Intenta nuevamente.")
            break
