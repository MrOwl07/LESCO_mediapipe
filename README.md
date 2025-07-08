# **Documentación del proyecto - PuraSeña**

## Tabla de contenidos
1. [Introducción](#introducción)
2. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
3. [Dependencias y Entorno](#dependencias-y-entorno)  
   3.1. [Instalación rápida](#instalación-rápida)  
   3.2. [MediaPipe Hand Landmarker – Guía de Uso](#mediapipe-hand-landmarker--guía-de-uso)  
   3.3. [scikit-learn](#scikit-learn)
4. [Flujo de Trabajo Detallado](#flujo-de-trabajo-detallado)  
   4.1. [Re-entrenar con datos personalizados](#re-entrenar-con-datos-personalizados)
5. [Limitaciones actuales](#limitaciones-actuales)
6. [Próximos pasos](#próximos-pasos)
7. [Licencia](#Licencia)
7. [Referencias](#referencias)
8. [Especiales Gracias](#especiales-gracias)

---

## Introducción
El proyecto **PuraSeña** es un prototipo que detecta y reconoce gestos de la Lengua de Señas Costarricense (LESCO) en tiempo real, convirtiéndolos en texto escrito. Combina la extracción de puntos de referencia (landmarks) de la mano mediante MediaPipe con modelos clásicos de machine learning para clasificar señales estáticas (letras del alfabeto) y dinámicas (palabras breves).

**Objetivos clave**
- **Inclusión:** Facilitar la comunicación entre personas oyentes y la comunidad sorda costarricense.
- **Ligero y portátil:** Funciona en CPU y puede adaptarse a web o dispositivos móviles.
- **Extensible:** Permite añadir nuevas letras o gestos re-entrenando el modelo con datos adicionales.

**Estado actual**
- Reconocimiento estable de letras del alfabeto LESCO.
- Scripts listos para captura de datos, entrenamiento y predicción en vivo.
- Pruebas en escritorio (Python 3.12.7 + Pipenv).

---

## Arquitectura del Proyecto
```
LESCO_mediapipe/
├── .vscode/                # Configuración de VS Code (opcional)
├── Pipfile                 # Dependencias gestionadas con Pipenv
├── Pipfile.lock            # Versión exacta de cada paquete
├── crear_modelo.py         # Entrenamiento y serialización del modelo
├── dataset_hands.py        # Captura de datos y generación de CSV
├── datos_letras.csv        # Dataset pre-procesado (landmarks + etiqueta)
├── imprimir_palabra.py     # Reconstruye palabras a partir de letras detectadas
├── label_encoder2.pkl      # Codificador de etiquetas (letras)
├── modelo_letras.pkl       # Modelo de clasificación entrenado
├── predecir_en_vivo.py     # Inferencia en tiempo real con webcam
└── prueba_final.csv        # CSV de prueba / evaluación
```

---

## Dependencias y Entorno

Se recomienda **Python 3.12.7** y administración de paquetes con **Pipenv**.

```toml
[packages]
mediapipe = "*"
opencv-python = "*"
pandas = "*"
scikit-learn = "*"

[dev-packages]

[requires]
python_version = "3.12"
python_full_version = "3.12.7"
```

### Instalación rápida
```bash
# Clonar el repositorio
git clone https://github.com/MrOwl07/LESCO_mediapipe.git
cd LESCO_mediapi
# Crear entorno
pip install pipenv  # si no lo tienes
pipenv install      # lee el Pipfile
pipenv shell        # activa el entorno
```

---

### MediaPipe Hand Landmarker – Guía de Uso

| Concepto               | Detalles relevantes                                                                                                                                  |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Entrada**            | Fotogramas BGR (OpenCV) o RGB (NumPy) con manos visibles.                                                                                             |
| **Salida**             | Lista de 21 *landmarks* por mano (`x`, `y`, `z`) + `handedness` (probabilidad de ser derecha/izquierda) + *scores*.                                  |
| **Parámetros clave**   | `num_hands`: máx. manos detectadas.<br>`min_hand_detection_confidence`: umbral inicial (0 – 1).<br>`min_hand_presence_confidence`: confianza para validar.<br>`min_tracking_confidence`: confianza de seguimiento. |
| **Normalización**      | El eje `z` es la distancia normalizada a la cámara ⇒ opcionalmente escálala o elimínala antes del modelo.                                             |
| **Rendimiento**        | Para CPU ajusta `num_threads`; con GPU (Android/WebGL) la inferencia es más rápida.                                                                     |

**Integración en el proyecto**
- `dataset_hands.py` – Inicializa `HandLandmarker` y escribe un CSV con 63 columnas (21 × 3) + `label`.
- `predecir_en_vivo.py` – Ejecuta inferencia frame a frame, extrae la mano de mayor confianza y envía el vector de 63 features al clasificador.
- `imprimir_palabra.py` – Aplica debouncing (≥ 3 fotogramas con la misma letra) para mejorar la precisión.

> **Tip de estabilidad:** Iluminación homogénea y fondo despejado mejoran drásticamente la confiabilidad (> 95 % de detección con `min_hand_detection_confidence≈0.5`).

---

### scikit‑learn

1. **Pre‑procesamiento** – Conversión de landmarks en `NumPy arrays`, normalización y escalado opcional.
2. **Codificación de etiquetas** – `LabelEncoder` traduce letras (A, B, C…) a enteros.
3. **Modelos probados**  
   - `RandomForestClassifier(n_estimators=200)`  
   - `SVC(kernel="rbf", C=10, gamma="scale")`
4. **Validación** – `train_test_split(test_size=0.2)` y `cross_val_score(cv=5)`.
5. **Métricas** – `classification_report`, `confusion_matrix`, `accuracy_score`.
6. **Serialización** – `joblib.dump()` para `modelo_letras.pkl` y `label_encoder.pkl`.
7. **Actualizaciones** – Re-entrena con CSV ampliado y reemplaza los `.pkl`.

---

## Flujo de Trabajo Detallado

| Paso | Script/Fichero       | Descripción                                                                        |
|------|----------------------|------------------------------------------------------------------------------------|
| 1    | `dataset_hands.py`   | Captura vídeo, extrae landmarks, crea `datos_letras.csv`.                          |
| 2    | `crear_modelo.py`    | Limpia datos, balancea clases, entrena modelo, guarda artefactos.                  |
| 3    | `predecir_en_vivo.py`| Carga modelo y codificador, abre webcam, muestra predicciones.                     |
| 4    | `imprimir_palabra.py`| Lee salidas, forma palabras en consola/archivo.                                    |

### Re-entrenar con datos personalizados
1. Añade nuevas filas a `datos_letras.csv` (63 columnas + `label`).  
2. Corre `python crear_modelo.py --test-size 0.2`.  
3. Reemplaza los archivos `.pkl` generados.

---

## Limitaciones actuales

- **Letras con movimiento:** Ch, J, LL, Ñ, RR, Z  
- **Palabras dinámicas 
- **Expresiones faciales:** emociones y marcadores gramaticales  

---

## Próximos pasos

- **Optimizar para móviles** — TensorFlow Lite en Android.  
- **Interfaz gráfica** — UI web/desktop.  
- **Gestos dinámicos** — LSTM/CNN + Optical Flow.  
- **Expresiones faciales** — Detector de emociones.  
- **Dataset ampliado** — Más muestras y variación.
- **Entorno laboral y reuniones virtuales** - La aplicación se enfocará en entornos de trabajo colaborativo y videoconferencias (Zoom, Google Meet, Microsoft Teams, etc.). Cuando una persona sorda utilice LESCO frente a la cámara, todos los participantes podrán ver la traducción en pantalla en tiempo real.

---

## Licencia

Este proyecto se distribuye bajo la Licencia MIT.

```text
MIT License

Copyright (c) 2025 Mariana Lai Sánchez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
---

## Referencias
Google, "MediaPipe Hand Landmarker," https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker

Scikit-learn developers, "Scikit-learn: Machine Learning in Python – Stable Documentation," https://scikit-learn.org/stable/

---

## Agradecimientos Especiales
- Beker Esteban Martínez Arias
- Eliana Mena García  
- Keylin Beltrán Hernández  
- Graciela Lackwood - Intérprete LESCO  
- Andher Ramos  
