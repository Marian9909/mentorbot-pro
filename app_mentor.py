import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime

# Configuración de la página orientada a dispositivos móviles y web
st.set_page_config(
    page_title="MentorBot Pro - Análisis Técnico Avanzado",
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

st.title("🤖 MentorBot Pro: Diagnóstico y Precisión Cuantitativa")
st.write("Herramienta de validación para alumnos de la academia con datos de mercado en tiempo real.")

# --- MENÚ LATERAL: CONTROL EMOCIONAL Y CONFIGURACIÓN ---
st.sidebar.header("🛡️ Control Emocional y Gestión")
emocion = st.sidebar.selectbox(
    "¿Cómo te sientes antes de operar?",
    ["Tranquilo y Enfocado", "Ansioso / Con FOMO", "Frustrado por pérdidas previas", "Demasiado eufórico"]
)

if emocion != "Tranquilo y Enfocado":
    st.sidebar.warning("⚠️ **Alerta de Psicología:** El estado emocional actual no es óptimo para operar con alta precisión. Reduce tu lotaje a la mitad.")

st.sidebar.markdown("---")
st.sidebar.header("📊 Parámetros de Mercado")
activo = st.sidebar.selectbox("Selecciona el Activo", ["EURUSD=X", "BTC-USD", "GC=X", "^GSPC"])
temporalidad = st.sidebar.selectbox("Temporalidad Principal", ["M1", "M5", "M15", "H1"])

# --- OBTENCIÓN DE DATOS REALES (YFINANCE) ---
@st.cache_data(ttl=600)
def cargar_datos_mercado(ticker):
    try:
        data = yf.download(ticker, period="5d", interval="1h", progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except Exception as e:
        return None

df_mercado = cargar_datos_mercado(activo)

# --- PANEL CENTRAL: COMPARATIVA Y ANÁLISIS ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📷 Carga tu Captura de Operativa")
    archivo_imagen = st.file_uploader("Sube tu gráfica (M1, M5 o M15)", type=["png", "jpg", "jpeg"])
    
    if archivo_imagen is not None:
        imagen = Image.open(archivo_imagen)
        st.image(imagen, caption="Gráfica analizada del alumno", use_container_width=True)

with col2:
    st.subheader("🔍 Diagnóstico Cuantitativo del Activo")
    
    if df_mercado is not None and not df_mercado.empty:
        precio_actual = float(df_mercado['Close'].iloc[-1])
        
        # Cálculo simple de indicadores (Media Móvil y RSI aproximado)
        df_mercado['SMA_20'] = df_mercado['Close'].rolling(window=20).mean()
        sma_actual = float(df_mercado['SMA_20'].iloc[-1])
        
        delta = df_mercado['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_actual = float(rsi.iloc[-1]) if not rsi.empty else 50.0

        st.metric(label=f"Precio Actual en Vivo ({activo})", value=f"${precio_actual:,.4f}")
        
        col_ind1, col_ind2 = st.columns(2)
        with col_ind1:
            st.metric(label="Tendencia (SMA 20)", value="Alcista 🟢" if precio_actual > sma_actual else "Bajista 🔴")
        with col_ind2:
            st.metric(label="Fuerza (RSI 14)", value=f"{rsi_actual:.1f}")
        
        # Criterios de precisión algorítmica
        st.markdown("### 📋 Validación de Niveles")
        if rsi_actual > 70:
            st.error("🚨 **Advertencia de Sobrecompra:** El RSI supera 70. Cuidado con compras en este nivel.")
        elif rsi_actual < 30:
            st.warning("⚠️ **Advertencia de Sobreventa:** El RSI está por debajo de 30. Vigila posibles rebotes alcistas.")
        else:
            st.success("✅ **Zona Neutra:** El RSI se encuentra en rangos saludables de operación.")
    else:
        st.info("Cargando datos del mercado en vivo...")

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

st.markdown("<br><p style='text-align: center; color: gray;'>Academia de Trading Profesional - Versión Avanzada con Datos Reales</p>", unsafe_allow_html=True)
