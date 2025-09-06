# LESCO Mediapipe - Boceto Inicial

Este proyecto es un boceto inicial para la captura y reconocimiento de gestos de la Lengua de Señas Costarricense (LESCO) usando visión por computadora con OpenCV y MediaPipe.

## Descripción

La aplicación permite capturar gestos de la mano a través de la cámara web, asociando cada gesto a una letra del abecedario. Los datos de los puntos clave (keypoints) de la mano se almacenan en un archivo CSV para su posterior uso en modelos de aprendizaje automático.

Actualmente, el sistema está en fase de refinamiento y sirve como prototipo para experimentación y desarrollo futuro.

## Dependencias

- Python 3.8 o superior
- OpenCV (`opencv-python`)
- MediaPipe
- (Opcional) Pipenv para gestión de entornos

## Instalación

1. **Clona este repositorio o descarga los archivos del proyecto.**

2. **Crea un entorno virtual (opcional pero recomendado):**
   - Con `venv`:
     ```bash
     python -m venv venv
     venv\Scripts\activate  # En Windows
     # source venv/bin/activate  # En Linux/Mac
     ```
   - O con `pipenv`:
     ```bash
     pip install pipenv
     pipenv install
     pipenv shell
     ```

3. **Instala las dependencias necesarias:**
   - Si usas `pip`:
     ```bash
     pip install opencv-python mediapipe
     ```
   - Si usas `pipenv`, las dependencias ya estarán instaladas con el paso anterior.

## Uso detallado

1. **Conecta una cámara web a tu computadora.**

2. **Ejecuta el script principal para capturar los datos de la mano:**
   ```bash
   python dataset_hands.py
   ```

3. **Funcionamiento de la ventana de captura:**
   - Se abrirá una ventana mostrando la imagen de la cámara y la letra actual seleccionada.
   - Coloca tu mano frente a la cámara para que sea detectada (aparecerán puntos y líneas sobre tu mano).
   - Presiona la barra espaciadora para guardar el gesto actual (los puntos clave de la mano) asociado a la letra mostrada en pantalla. Cada vez que presiones espacio, se guardará una nueva muestra en el archivo CSV.
   - Cambia la letra presionando cualquier tecla de la A a la Z. La letra actual se actualizará en la pantalla y los siguientes gestos que guardes estarán asociados a esa letra.
   - Presiona la tecla `,` (coma) para salir del programa y cerrar la ventana.

4. **Salida:**
   - Los datos capturados se guardarán en el archivo `prueba.csv` en el mismo directorio del proyecto. Cada fila contiene la letra y los puntos clave de la mano detectada (coordenadas x, y, z de cada punto).

## Estado del proyecto

> **Nota:** Este proyecto es un boceto inicial y está en proceso de refinamiento. El código y la estructura pueden cambiar en futuras versiones.

## Autor
- MrOwl07

---

Si tienes sugerencias o encuentras errores, no dudes en contribuir o abrir un issue.
