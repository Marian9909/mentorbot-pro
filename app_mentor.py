import streamlit as st
from PIL import Image
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="MentorBot Pro - Esencial & Directo",
    page_icon="📈",
    layout="wide"
)

# Estilo visual adaptado
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 MentorBot Pro: Análisis Directo y Esencial")
st.write("Herramienta ágil y estable para la validación rápida de tu operativa.")

# --- MENÚ LATERAL: CONTROL EMOCIONAL Y CONFIGURACIÓN ---
st.sidebar.header("🛡️ Control Emocional")
emocion = st.sidebar.selectbox(
    "¿Cómo te sientes antes de operar?",
    ["Tranquilo y Enfocado", "Ansioso / Con FOMO", "Frustrado por pérdidas previas", "Demasiado eufórico"]
)

if emocion != "Tranquilo y Enfocado":
    st.sidebar.warning("⚠️ **Alerta de Psicología:** El estado emocional no es óptimo. Reduce tu lotaje a la mitad.")

st.sidebar.markdown("---")
st.sidebar.header("📊 Parámetros de Mercado")

activo_seleccionado = st.sidebar.selectbox(
    "Selecciona el Activo", 
    ["Step Index (Deriv)", "EUR/USD", "Bitcoin (BTC-USD)", "Oro (GC=X)", "S&P 500"]
)

temporalidad = st.sidebar.selectbox("Temporalidad Principal", ["M1", "M5", "M15", "H1"])

# --- PANEL CENTRAL: MULTICARGA DE FOTOS Y GUÍA RÁPIDA ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📷 Carga tus Capturas")
    st.info("Sube hasta 3 capturas de tu análisis en TradingView o Deriv.")
    
    archivos_imagenes = st.file_uploader(
        "Sube tus gráficas", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    if archivos_imagenes:
        st.success(f"¡Se han cargado {len(archivos_imagenes)} imágenes correctamente!")
        for i, archivo_imagen in enumerate(archivos_imagenes):
            imagen = Image.open(archivo_imagen)
            st.image(imagen, caption=f"Captura #{i+1} del alumno", use_container_width=True)

with col2:
    st.subheader(f"🔍 Diagnóstico Rápido ({activo_seleccionado})")
    
    st.info("💡 **Guía de Validación Visual:** Observa directamente tu gráfica en TradingView / Deriv:")
    
    st.markdown("""
    * **Estructura y Patrón:** Valida el comportamiento del precio en tu pantalla.
    * **Punto de Entrada:** Respeta el nivel exacto que marcaste (ej. tu línea azul en Step Index).
    * **Stop Loss (SL):** Asegúrate de colocarlo protegido tras el último fractal.
    * **Take Profit (TP):** Valida que tu objetivo cumpla con una relación de beneficio/riesgo mínima de **1:2**.
    """)
    
    st.success("✅ **Checklist Operativo:** Si tus capturas muestran confluencia y tu gestión de riesgo es correcta, ejecuta con disciplina.")

# --- PLAN DE ACCIÓN Y RIESGO ---
st.markdown("---")
st.subheader("⚙️ Estructura de Operación Recomendada")
col_reg1, col_reg2, col_reg3 = st.columns(3)
with col_reg1:
    st.info("**Riesgo Permitido:** Máx. 1% de la cuenta")
with col_reg2:
    st.info("**Gestión:** Relación Beneficio/Riesgo mínima 1:2")
with col_reg3:
    st.info("**Disciplina:** Respetar Stop Loss sin excepciones")

st.markdown("<br><p style='text-align: center; color: gray;'>Academia de Trading Profesional - Versión Esencial</p>", unsafe_allow_html=True)
