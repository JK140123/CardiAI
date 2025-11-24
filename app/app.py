import streamlit as st
import base64


st.set_page_config(
    page_title="Landing – CardiAI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Cargar fondo como base64
# ---------------------------------------------------------
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image = get_base64("assets/images/fondo.jpg")

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------
st.markdown(
    f"""
    <style>

    /* Fondo global */
    [data-testid="stAppViewContainer"] {{
        background:
            linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)),
            url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Contenedor del contenido */
    .block-container {{
        background: rgba(255,255,255,0.92);
        padding: 2rem 2.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        backdrop-filter: blur(5px);
        max-width: 850px;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }}

    /* Título */
    h1 {{
        text-align: center;
        color: black;
        font-size: 2.6rem;
        font-weight: 700;
    }}

    /* Línea decorativa */
    h1::after {{
        content: "";
        display: block;
        width: 120px;
        height: 4px;
        background: #3b62f0;
        margin: 10px auto 0 auto;
        border-radius: 5px;
        animation: fadeIn 1.2s ease-out;
    }}

    /* Slogan */
    .slogan {{
        text-align: center;
        font-size: 1.35rem;
        font-weight: 500;
        color: #374151;
        margin-top: -10px;
        margin-bottom: 1.5rem;
    }}

    /* Animación */
    @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(10px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Íconos */
    .icon-title {{
        font-size: 4.2rem;
        text-align: center;
        animation: fadeIn 1s ease-in-out;
    }}

    /* Subtítulos */
    .section-title {{
        background: rgba(59, 98, 240, 0.15);
        padding: 6px 14px;
        border-left: 5px solid #3b62f0;
        border-radius: 8px;
        font-weight: 700;
        display: inline-block;
    }}

    /* BOTÓN — selector actualizado */
    div.btn-enter button[kind="primary"] {{
        background-color: #3b62f0 !important;
        color: white !important;
        border-radius: 12px;
        padding: 0.9rem 2.2rem;
        font-size: 1.3rem;
        font-weight: bold;
        width: 100%;
        border: none;
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        transition: 0.3s;
    }}

    div.btn-enter button[kind="primary"]:hover {{
        background-color: #2748c7 !important;
        transform: scale(1.06);
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# CONTENIDO
# ---------------------------------------------------------

st.title("CardiAI – Predictive Health Assistant")

st.markdown(
    "<div class='slogan'>Transformando la salud con inteligencia y precisión</div>",
    unsafe_allow_html=True
)

st.write(
    """
Hoy en día, la inteligencia artificial está integrada en múltiples ámbitos de nuestra vida,
permitiendo resolver problemas complejos de manera más eficiente.  
En la medicina, surge la necesidad de herramientas que apoyen la detección temprana de enfermedades
y faciliten el trabajo de los profesionales de la salud.

Nuestra API fue diseñada con ese propósito: ofrecer un soporte predictivo para evaluar 
riesgos cardíacos de forma **rápida, confiable y accesible**.
"""
)

st.write("---")

# ÍCONOS
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='icon-title'>🫀</div>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>Predicción cardíaca</h3>", unsafe_allow_html=True)
    st.write("Modelos diseñados para apoyar la evaluación clínica del riesgo.")

with col2:
    st.markdown("<div class='icon-title'>📊</div>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>Análisis inteligente</h3>", unsafe_allow_html=True)
    st.write("Resultados claros, interpretables y basados en datos reales.")

with col3:
    st.markdown("<div class='icon-title'>🔒</div>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>Datos seguros</h3>", unsafe_allow_html=True)
    st.write("Procesamiento responsable y alineado con buenas prácticas de privacidad.")

st.write("---")

# BOTÓN
with st.container():
    st.markdown("<div class='btn-enter'>", unsafe_allow_html=True)
    if st.button("Entrar a la aplicación"):
        st.switch_page("pages/1_App.py")
    st.markdown("</div>", unsafe_allow_html=True)

# DISCLAIMER / ADVERTENCIA MÉDICA
st.markdown(
    """
    <div style="
        margin-top: 1rem;
        font-size: 0.82rem;
        color: #4b5563;
        text-align: center;
        background: rgba(255,255,255,0.65);
        padding: 8px 14px;
        border-radius: 8px;
        border-left: 4px solid #d97706;
    ">
        ⚠️ <b>Advertencia:</b> Esta herramienta es un soporte de análisis y 
        <b>no constituye un diagnóstico médico definitivo</b>.  
        Su función es complementar la evaluación profesional y ayudar a orientar la conversación con su médico.
    </div>
    """,
    unsafe_allow_html=True
)

st.write("---")

# QUIÉNES SOMOS
st.markdown("<h2 class='section-title'>¿Quiénes somos?</h2>", unsafe_allow_html=True)
st.write(
    """
Somos estudiantes de último semestre de Ingeniería Industrial comprometidos con la creación
de soluciones tecnológicas que aporten valor real a la salud.  
Nuestro objetivo es integrar **inteligencia artificial** en procesos médicos para facilitar
la detección temprana, apoyar la toma de decisiones y mejorar la calidad de vida de los pacientes.
"""
)

# FOOTER
st.markdown(
    """
    <br><br>
    <div style="background:rgba(255,255,255,0.55); 
                padding:15px; 
                border-radius:10px; 
                text-align:center;
                backdrop-filter: blur(4px);">
        <b>Desarrollado por:</b><br>
        Juan Agredo – juanaggi@unisabana.edu.co<br>
        Alejandro Barrera – luisbarsi@unisabana.edu.co<br>
        Sergio Rodriguez – sergioro@unisabana.edu.co
    </div>
    """,
    unsafe_allow_html=True
)
