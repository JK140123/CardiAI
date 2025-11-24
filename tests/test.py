import pickle
import numpy as np

# Cargar el modelo
with open("api/modelo_rf_final.pkl", "rb") as f:
    modelo_pkl = pickle.load(f)

print("=== INFORMACIÓN DEL MODELO ===")
print(f"Tipo de modelo: {type(modelo_pkl['model'])}")
print(f"Feature names: {modelo_pkl['feature_names']}")
print(f"Número de features: {len(modelo_pkl['feature_names'])}")

# Si tiene atributos del modelo
model = modelo_pkl['model']
if hasattr(model, 'n_estimators'):
    print(f"N° de árboles: {model.n_estimators}")
if hasattr(model, 'max_depth'):
    print(f"Max depth: {model.max_depth}")
if hasattr(model, 'classes_'):
    print(f"Clases: {model.classes_}")

# Cargar scaler
with open("api/minmax_scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
print(f"\n=== SCALER ===")
print(f"Tipo: {type(scaler)}")
print(f"Min values: {scaler.min_}")
print(f"Scale values: {scaler.scale_}")

# Cargar encoder
with open("api/alcohol_manual_encoder.pkl", "rb") as f:
    encoder = pickle.load(f)
print(f"\n=== ENCODER ===")
print(f"Mapeo: {encoder}")

# Hacer una predicción de prueba con valores normales
test_values = [0, 10, 2, 24.5, 7, 140, 180, 95, 115, 45]  # Low, normales
print(f"\n=== PRUEBA CON VALORES NORMALES ===")
print(f"Input: {test_values}")
x_scaled = scaler.transform(np.array(test_values).reshape(1, -1))
print(f"Después de escalar: {x_scaled}")
pred = model.predict(x_scaled)[0]
proba = model.predict_proba(x_scaled)[0]
print(f"Predicción: {pred}")
print(f"Probabilidades: {proba}")
print(f"Confianza: {max(proba)}")