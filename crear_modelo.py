# entrenamiento
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

# Asignar los encabezados: la primera columna es 'letra', las demás son coordenadas
columnas = ['letra'] + [f'col{i}' for i in range(1, 1 + 63)]  # Ajusta 63 si hay otro número de columnas

# Cargar datos con encabezados personalizados
df = pd.read_csv('prueba_mariana.csv', header=None, names=columnas)

# Separar características y etiquetas
X = df.drop('letra', axis=1)
y = df['letra']

# Codificar etiquetas
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Guardar el codificador
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)

# Entrenar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Guardar el modelo
with open('modelo_letras.pkl', 'wb') as f:
    pickle.dump(modelo, f)

print("Modelo entrenado y guardado con éxito.")
