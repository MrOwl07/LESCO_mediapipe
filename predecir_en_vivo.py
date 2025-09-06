import cv2
import mediapipe as mp
import numpy as np
import joblib

# Cargar el modelo y el codificador
modelo = joblib.load("modelo_letras.pkl")
le = joblib.load("label_encoder4.pkl")

# Inicializar MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Iniciar la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Voltear horizontalmente (espejo)
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    letra = ""

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Dibujar puntos en la mano
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extraer los 21 puntos (x, y, z)
            keypoints = []
            for lm in hand_landmarks.landmark:
                keypoints.extend([lm.x, lm.y, lm.z])

            if len(keypoints) == 63:
                keypoints_np = np.array(keypoints).reshape(1, -1)
                pred = modelo.predict(keypoints_np)[0]
                letra = le.inverse_transform([pred])[0]

    # Mostrar la letra predicha en pantalla
    cv2.putText(frame, f"Letra: {letra}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Reconocimiento de Letra", frame)

    if cv2.waitKey(1) & 0xFF == ord(','):
        break

cap.release()
cv2.destroyAllWindows()
