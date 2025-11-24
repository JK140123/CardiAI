# app/app.py

import streamlit as st
import requests

st.set_page_config(
    page_title="Heart Disease Predictor",
    layout="centered",
    page_icon="❤️"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    /* Fondo con imagen - usando stApp para el contenedor principal */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0, 20, 50, 0.5), rgba(0, 20, 50, 0.7)), 
                    url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><defs><linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" style="stop-color:rgb(30,41,82);stop-opacity:1" /><stop offset="100%" style="stop-color:rgb(15,23,42);stop-opacity:1" /></linearGradient></defs><rect fill="url(%23bg)" width="1024" height="1024"/><g opacity="0.3" fill="none" stroke="%2364748b" stroke-width="1"><line x1="100" y1="150" x2="200" y2="100"/><line x1="200" y1="100" x2="150" y2="250"/><line x1="300" y1="200" x2="400" y2="300"/><line x1="500" y1="150" x2="600" y2="200"/><line x1="700" y1="300" x2="800" y2="250"/><line x1="150" y1="400" x2="250" y2="500"/><line x1="400" y1="450" x2="500" y2="550"/><line x1="650" y1="500" x2="750" y2="600"/><circle cx="100" cy="150" r="3"/><circle cx="200" cy="100" r="3"/><circle cx="150" cy="250" r="3"/><circle cx="300" cy="200" r="3"/><circle cx="400" cy="300" r="3"/><circle cx="500" cy="150" r="3"/><circle cx="600" cy="200" r="3"/><circle cx="700" cy="300" r="3"/><circle cx="800" cy="250" r="3"/></g></svg>');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Contenedor principal */
    .block-container {
        padding: 2rem 1rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Título principal */
    h1 {
        color: #667eea;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* Subtítulos */
    h3 {
        color: #764ba2;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Inputs */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Botón de submit */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Tarjetas de resultado */
    .result-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #667eea;
        font-weight: 700;
    }
    
    /* Alertas personalizadas */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
    }
    </style>
""", unsafe_allow_html=True)

API_URL = "https://cardiai.onrender.com/predict"

# ---- Header ----
st.title("❤️ Heart Disease Risk Predictor")
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 1.1rem;'>"
    "Ingrese los datos del paciente para obtener una predicción del riesgo cardiovascular"
    "</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---- Formulario con columnas ----
with st.form("predict_form"):
    st.subheader("📋 Datos del Paciente")
    
    # Columna 1: Datos básicos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 👤 Información Básica")
        Age = st.number_input("Edad (años)", min_value=1, max_value=120, step=1, help="Ingrese la edad del paciente")
        BMI = st.number_input("BMI - Índice de Masa Corporal (kg/m²)", min_value=10.0, max_value=60.0, step=0.1, help="Rango normal: 18.5-24.9")
        Sleep_Hours = st.number_input("Horas de Sueño (horas/día)", min_value=0.0, max_value=24.0, step=0.5, help="Rango típico: 6-9 horas")
        Alcohol_Consumption = st.selectbox(
            "Consumo de Alcohol",
            ["Low", "Medium", "High"],
            help="Nivel de consumo de alcohol"
        )
    
    with col2:
        st.markdown("##### 🩺 Indicadores Vitales")
        Blood_Pressure = st.number_input("Presión Arterial Sistólica (mmHg)", min_value=50.0, max_value=250.0, step=1.0, help="Rango normal: 90-120 mmHg")
        Fasting_Blood_Sugar = st.number_input("Glucosa en Ayunas (mg/dL)", min_value=50.0, max_value=400.0, step=1.0, help="Rango normal: 70-100 mg/dL")
        Cholesterol_Level = st.number_input("Colesterol Total (mg/dL)", min_value=100.0, max_value=400.0, step=1.0, help="Rango normal: <200 mg/dL")
        Triglyceride_Level = st.number_input("Triglicéridos (mg/dL)", min_value=30.0, max_value=500.0, step=1.0, help="Rango normal: <150 mg/dL")
    
    st.markdown("---")
    
    # Columna 3: Marcadores avanzados
    st.markdown("##### 🧪 Marcadores Bioquímicos")
    col3, col4 = st.columns(2)
    
    with col3:
        Homocysteine_Level = st.number_input("Homocisteína (μmol/L)", min_value=1.0, max_value=50.0, step=0.1, help="Rango normal: 5-15 μmol/L")
    
    with col4:
        CRP_Level = st.number_input("Proteína C Reactiva (mg/L)", min_value=0.1, max_value=50.0, step=0.1, help="Rango normal: <3 mg/L")
    
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍 Realizar Predicción")

# ---- Procesar predicción ----
if submitted:
    # Validar que no todos los campos sean 0
    numeric_values = [Age, BMI, Sleep_Hours, Blood_Pressure, Fasting_Blood_Sugar, 
                      Cholesterol_Level, Triglyceride_Level, Homocysteine_Level, CRP_Level]
    
    if all(v == 0 for v in numeric_values):
        st.error("⚠️ **Por favor, ingrese valores válidos en todos los campos.** Los valores no pueden ser todos cero.")
    elif Age == 0:
        st.warning("⚠️ Por favor, ingrese la edad del paciente.")
    else:
        payload = {
            "Alcohol_Consumption": Alcohol_Consumption,
            "Homocysteine_Level": Homocysteine_Level,
            "BMI": BMI,
            "CRP_Level": CRP_Level,
            "Sleep_Hours": Sleep_Hours,
            "Triglyceride_Level": Triglyceride_Level,
            "Cholesterol_Level": Cholesterol_Level,
            "Fasting_Blood_Sugar": Fasting_Blood_Sugar,
            "Blood_Pressure": Blood_Pressure,
            "Age": Age
        }

    with st.spinner("🔄 Analizando datos..."):
        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()
                pred = result["prediction"]
                prob = result["confidence"] * 100

                # Debug: Mostrar respuesta completa
                with st.expander("🔍 Ver datos de respuesta (Debug)", expanded=False):
                    st.json(result)
                    st.write("**Datos enviados:**")
                    st.json(payload)

                st.markdown("---")
                st.subheader("📊 Resultado del Análisis")

                # Mostrar resultado con color según riesgo
                if pred == 1:
                    st.error("⚠️ **El modelo indica RIESGO de enfermedad cardiovascular**")
                    risk_color = "#ff4b4b"
                else:
                    st.success("✅ **El modelo indica BAJO RIESGO de enfermedad cardiovascular**")
                    risk_color = "#21c354"

                # Métrica visual
                col_metric1, col_metric2, col_metric3 = st.columns([1, 2, 1])
                
                with col_metric2:
                    st.markdown(
                        f"<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, {risk_color}15 0%, {risk_color}30 100%); "
                        f"border-radius: 15px; border: 2px solid {risk_color};'>"
                        f"<h2 style='color: {risk_color}; margin: 0;'>Confianza del Modelo</h2>"
                        f"<h1 style='color: {risk_color}; margin: 0.5rem 0; font-size: 3rem;'>{prob:.1f}%</h1>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                # Recomendaciones
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("💡 Ver Recomendaciones", expanded=True):
                    if pred == 1:
                        st.warning(
                            "**Recomendaciones importantes:**\n\n"
                            "- Consulte con un cardiólogo lo antes posible\n"
                            "- Mantenga un control regular de su presión arterial\n"
                            "- Considere modificar hábitos de estilo de vida\n"
                            "- Realice chequeos médicos periódicos"
                        )
                    else:
                        st.info(
                            "**Mantener hábitos saludables:**\n\n"
                            "- Continúe con una dieta balanceada\n"
                            "- Mantenga actividad física regular\n"
                            "- Realice chequeos médicos anuales\n"
                            "- Monitoree sus indicadores de salud"
                        )

            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error(
                "⚠️ **No se pudo conectar con la API**\n\n"
                "Asegúrese de que el servidor esté ejecutándose con:\n"
                "`uvicorn api.main:app --reload`"
            )
            