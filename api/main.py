# api/main.py
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

# -----------------------------------------------------------
# Cargar archivos PKL (modelo, scaler, encoder)
# -----------------------------------------------------------
try:
    with open("api/modelo_rf_final.pkl", "rb") as f:
        modelo_pkl = pickle.load(f)
    model = modelo_pkl["model"]
    feature_names = modelo_pkl["feature_names"]

    with open("api/minmax_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    with open("api/alcohol_manual_encoder.pkl", "rb") as f:
        alcohol_encoder = pickle.load(f)

except Exception as e:
    raise RuntimeError(f"Error cargando los modelos/encoders PKL: {e}")

# -----------------------------------------------------------
# Orden de las columnas que espera el scaler
# IMPORTANTE: El scaler fue entrenado con estas 9 variables en este orden específico
# -----------------------------------------------------------
SCALER_COLUMN_ORDER = [
    'Age', 'Blood Pressure', 'Cholesterol Level', 'BMI',
    'Sleep Hours', 'Triglyceride Level', 'Fasting Blood Sugar',
    'CRP Level', 'Homocysteine Level'
]

# -----------------------------------------------------------
# Pydantic Input Model
# -----------------------------------------------------------
class PatientData(BaseModel):
    Alcohol_Consumption: str = Field(..., description="Low, Medium, High")
    Homocysteine_Level: float
    CRP_Level: float
    BMI: float
    Sleep_Hours: float
    Triglyceride_Level: float
    Cholesterol_Level: float
    Fasting_Blood_Sugar: float
    Blood_Pressure: float
    Age: int

    @field_validator("Alcohol_Consumption", mode="before")
    @classmethod
    def validate_alcohol(cls, v):
        if not isinstance(v, str):
            raise ValueError("Debe ser texto")
        normalized = v.strip().lower()
        mapping = {
            "low": "Low",
            "medium": "Medium",
            "high": "High",
            "bajo": "Low",
            "medio": "Medium",
            "alto": "High"
        }
        if normalized not in mapping:
            raise ValueError("Alcohol_Consumption debe ser Low/Medium/High")
        return mapping[normalized]

    @field_validator(
        "Homocysteine_Level", "CRP_Level", "BMI", "Sleep_Hours",
        "Triglyceride_Level", "Cholesterol_Level",
        "Fasting_Blood_Sugar", "Blood_Pressure",
        mode="before"
    )
    @classmethod
    def validate_numeric(cls, v, info):
        try:
            val = float(v)
        except:
            raise ValueError(f"{info.field_name} debe ser numérico")
        if val < 0:
            raise ValueError(f"{info.field_name} debe ser >= 0")
        return val

    @field_validator("Age", mode="before")
    @classmethod
    def validate_age(cls, v):
        try:
            age = int(v)
        except:
            raise ValueError("Age debe ser entero")
        if not (0 <= age <= 120):
            raise ValueError("Age debe estar entre 0 y 120")
        return age

# -----------------------------------------------------------
# FastAPI
# -----------------------------------------------------------
app = FastAPI(title="Heart Disease Prediction API", version="1.0")

@app.get("/")
def root():
    return {
        "message": "Heart Disease Prediction API",
        "version": "1.0",
        "endpoints": {
            "/predict/": "POST - Realizar predicción",
            "/health/": "GET - Health check"
        }
    }

@app.get("/health/")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "encoder_loaded": alcohol_encoder is not None,
        "expected_features": len(feature_names),
        "feature_names": feature_names
    }

@app.post("/predict/")
def predict(data: PatientData):
    """
    Realiza predicción de riesgo de enfermedad cardíaca.
    
    Pipeline:
    1. Codificar Alcohol_Consumption (Low/Medium/High -> 0/1/2)
    2. Normalizar las 9 variables numéricas con MinMaxScaler
    3. Reconstruir vector en el orden que espera el modelo
    4. Predecir con RandomForest
    """
    
    # -------------------------------------------------------
    # PASO 1: Codificar Alcohol Consumption
    # -------------------------------------------------------
    try:
        # FIX: Usar 'mapping' dentro del encoder
        alcohol_value = alcohol_encoder['mapping'][data.Alcohol_Consumption]
    except KeyError:
        raise HTTPException(
            status_code=400, 
            detail=f"Valor inválido para Alcohol_Consumption: {data.Alcohol_Consumption}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error codificando Alcohol_Consumption: {str(e)}"
        )

    # -------------------------------------------------------
    # PASO 2: Preparar datos numéricos para normalización
    # -------------------------------------------------------
    # El scaler espera las 9 variables numéricas en un orden específico
    # SIN incluir Alcohol Consumption
    
    numeric_data = {
        'Age': float(data.Age),
        'Blood Pressure': data.Blood_Pressure,
        'Cholesterol Level': data.Cholesterol_Level,
        'BMI': data.BMI,
        'Sleep Hours': data.Sleep_Hours,
        'Triglyceride Level': data.Triglyceride_Level,
        'Fasting Blood Sugar': data.Fasting_Blood_Sugar,
        'CRP Level': data.CRP_Level,
        'Homocysteine Level': data.Homocysteine_Level
    }

    try:
        # Ordenar según el orden del scaler
        x_to_scale = np.array([numeric_data[col] for col in SCALER_COLUMN_ORDER]).reshape(1, -1)
    except KeyError as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Falta variable para scaler: {str(e)}"
        )

    # -------------------------------------------------------
    # PASO 3: Normalizar con MinMaxScaler
    # -------------------------------------------------------
    try:
        x_scaled = scaler.transform(x_to_scale)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error aplicando scaler: {str(e)}"
        )

    # -------------------------------------------------------
    # PASO 4: Reconstruir vector en el orden del modelo
    # -------------------------------------------------------
    # feature_names = ['Alcohol Consumption', 'Homocysteine Level', 'CRP Level', 
    #                  'BMI', 'Sleep Hours', 'Triglyceride Level', 
    #                  'Cholesterol Level', 'Fasting Blood Sugar', 
    #                  'Blood Pressure', 'Age']
    
    try:
        # Crear diccionario completo con valores normalizados
        complete_data = {
            'Alcohol Consumption': alcohol_value,  # NO normalizado
            'Homocysteine Level': x_scaled[0, SCALER_COLUMN_ORDER.index('Homocysteine Level')],
            'CRP Level': x_scaled[0, SCALER_COLUMN_ORDER.index('CRP Level')],
            'BMI': x_scaled[0, SCALER_COLUMN_ORDER.index('BMI')],
            'Sleep Hours': x_scaled[0, SCALER_COLUMN_ORDER.index('Sleep Hours')],
            'Triglyceride Level': x_scaled[0, SCALER_COLUMN_ORDER.index('Triglyceride Level')],
            'Cholesterol Level': x_scaled[0, SCALER_COLUMN_ORDER.index('Cholesterol Level')],
            'Fasting Blood Sugar': x_scaled[0, SCALER_COLUMN_ORDER.index('Fasting Blood Sugar')],
            'Blood Pressure': x_scaled[0, SCALER_COLUMN_ORDER.index('Blood Pressure')],
            'Age': x_scaled[0, SCALER_COLUMN_ORDER.index('Age')]
        }
        
        # Ordenar según feature_names del modelo
        final_input = np.array([complete_data[f] for f in feature_names]).reshape(1, -1)
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error construyendo vector final: {str(e)}"
        )

    # -------------------------------------------------------
    # PASO 5: Realizar Predicción
    # -------------------------------------------------------
    try:
        pred = int(model.predict(final_input)[0])
        proba = model.predict_proba(final_input)[0].tolist()
        confidence = max(proba)
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error en predicción: {str(e)}"
        )

    # -------------------------------------------------------
    # PASO 6: Formatear respuesta
    # -------------------------------------------------------
    risk_label = "Alto Riesgo" if pred == 1 else "Bajo Riesgo"
    
    return {
        "prediction": pred,
        "risk_label": risk_label,
        "probabilities": {
            "class_0_low_risk": proba[0],
            "class_1_high_risk": proba[1]
        },
        "confidence": confidence,
        "metadata": {
            "model_version": modelo_pkl.get("metadata", {}).get("version", "unknown"),
            "feature_count": len(feature_names),
            "alcohol_encoded": alcohol_value
        }
    }


# -----------------------------------------------------------
# Endpoint adicional para testing
# -----------------------------------------------------------
@app.post("/predict/debug/")
def predict_debug(data: PatientData):
    """
    Versión debug que muestra el proceso paso a paso
    """
    
    # Paso 1: Alcohol
    alcohol_value = alcohol_encoder['mapping'][data.Alcohol_Consumption]
    
    # Paso 2: Datos numéricos
    numeric_data = {
        'Age': float(data.Age),
        'Blood Pressure': data.Blood_Pressure,
        'Cholesterol Level': data.Cholesterol_Level,
        'BMI': data.BMI,
        'Sleep Hours': data.Sleep_Hours,
        'Triglyceride Level': data.Triglyceride_Level,
        'Fasting Blood Sugar': data.Fasting_Blood_Sugar,
        'CRP Level': data.CRP_Level,
        'Homocysteine Level': data.Homocysteine_Level
    }
    
    x_to_scale = np.array([numeric_data[col] for col in SCALER_COLUMN_ORDER]).reshape(1, -1)
    x_scaled = scaler.transform(x_to_scale)
    
    # Paso 3: Vector final
    complete_data = {
        'Alcohol Consumption': alcohol_value,
        'Homocysteine Level': x_scaled[0, SCALER_COLUMN_ORDER.index('Homocysteine Level')],
        'CRP Level': x_scaled[0, SCALER_COLUMN_ORDER.index('CRP Level')],
        'BMI': x_scaled[0, SCALER_COLUMN_ORDER.index('BMI')],
        'Sleep Hours': x_scaled[0, SCALER_COLUMN_ORDER.index('Sleep Hours')],
        'Triglyceride Level': x_scaled[0, SCALER_COLUMN_ORDER.index('Triglyceride Level')],
        'Cholesterol Level': x_scaled[0, SCALER_COLUMN_ORDER.index('Cholesterol Level')],
        'Fasting Blood Sugar': x_scaled[0, SCALER_COLUMN_ORDER.index('Fasting Blood Sugar')],
        'Blood Pressure': x_scaled[0, SCALER_COLUMN_ORDER.index('Blood Pressure')],
        'Age': x_scaled[0, SCALER_COLUMN_ORDER.index('Age')]
    }
    
    final_input = np.array([complete_data[f] for f in feature_names]).reshape(1, -1)
    
    # Predicción
    pred = int(model.predict(final_input)[0])
    proba = model.predict_proba(final_input)[0].tolist()
    
    return {
        "debug_info": {
            "step_1_alcohol_encoded": alcohol_value,
            "step_2_numeric_data_original": numeric_data,
            "step_3_scaler_input_order": SCALER_COLUMN_ORDER,
            "step_4_scaled_values": x_scaled.tolist()[0],
            "step_5_final_vector_order": feature_names,
            "step_6_final_vector_values": final_input.tolist()[0]
        },
        "prediction": pred,
        "probabilities": proba,
        "confidence": max(proba)
    }