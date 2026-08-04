import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime

# Configuración de la página orientada a dispositivos móviles y web
st.set_page_config(
    page_title="MentorBot Pro - Mindset & Análisis Cuantitativo",
    page_icon="🧠",
    layout="wide"
)

# Estilo visual adaptado
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 MentorBot Pro: Mindset & Precisión Cuantitativa")
st.write("La regla de oro de la academia: **Primero la mente, después la técnica.**")

# --- BLOQUE OBLIGATORIO 1: CONTROL EMOCIONAL (EL FILTRO DE MINDSET) ---
st.sidebar.header("🛡️ 1. Filtro de Psicología y Mindset")
st.sidebar.markdown("Antes de tocar el mercado, evalúa tu estado mental real:")

emocion = st.sidebar.selectbox(
    "¿Cómo te sientes en este preciso instante?",
    ["Selecciona tu estado...", "Tranquilo, paciente y disciplinado", "Ansioso / Con FOMO", "Eufórico por una racha ganadora", "Frustrado / Queriendo recuperar pérdidas (Venganza)"]
)

# Evaluación estricta de mindset
mindset_apto = True
if emocion == "Selecciona tu estado...":
    st.sidebar.info("Por favor, define tu estado emocional para desbloquear el análisis.")
    mindset_apto = False
elif emocion != "Tranquilo, paciente y disciplinado":
    mindset_apto = False
    st.sidebar.error("🛑 **BLOQUEO DE MINDSET ACTIVADO:** Tu estado mental actual te llevará a romper tu gestión de riesgo. **Queda estrictamente prohibido operar hoy.** Cierra las plataformas y sal a caminar.")
else:
    st.sidebar.success("✅ **Mindset Aprobado:** Estás operando desde la disciplina y la ejecución fría del plan.")

st.sidebar.markdown("---")
st.sidebar.header("📊 2. Parámetros de Mercado")

opciones_activos = {
    "Step Index (Deriv / Sintéticos)": "EURUSD=X", # Referencia base para cálculos
    "EUR/USD": "EURUSD=X",
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Oro (GC=X)": "GC=X",
    "S&P 500": "^GSPC"
}

activo_seleccionado = st.sidebar.selectbox("Selecciona el Activo", list(opciones_activos.keys()))
ticker_yahoo = opciones_activos[activo_seleccionado]
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

df_mercado = cargar_datos_mercado(ticker_yahoo)

# --- PANEL CENTRAL: CONDICIONADO POR EL MINDSET ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📷 Carga tus Capturas de Operativa (Hasta 3 fotos)")
    st.info("Sube tu estructura macro, tu zona de ejecución y tu gestión.")
    
    archivos_imagenes = st.file_uploader(
        "Sube tus gráficas", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    if archivos_imagenes:
        st.success(f"¡{len(archivos_imagenes)} imágenes cargadas correctamente!")
        for i, archivo_imagen in enumerate(archivos_imagenes):
            imagen = Image.open(archivo_imagen)
            st.image(imagen, caption=f"Captura #{i+1} del alumno", use_container_width=True)

with col2:
    st.subheader(f"🔍 Diagnóstico Técnico ({activo_seleccionado})")
    
    if not mindset_apto:
        st.warning("🔒 **Diagnóstico Bloqueado:** El sistema no evaluará gráficos técnicos hasta que tu mente esté en un estado óptimo y libre de emociones destructivas. ¡Protege tu capital protegiendo tu mente!")
    else:
        if df_mercado is not None and not df_mercado.empty:
            precio_actual = float(df_mercado['Close'].iloc[-1])
            
            # Cálculo de indicadores técnicos (Media Móvil y RSI)
            df_mercado['SMA_20'] = df_mercado['Close'].rolling(window=20).mean()
            sma_actual = float(df_mercado['SMA_20'].iloc[-1])
            
            delta = df_mercado['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            rsi_actual = float(rsi.iloc[-1]) if not rsi.empty else 50.0

            st.metric(label=f"Precio de Referencia Actual", value=f"${precio_actual:,.4f}")
            
            col_ind1, col_ind2 = st.columns(2)
            with col_ind1:
                st.metric(label="Tendencia (SMA 20)", value="Alcista 🟢" if precio_actual > sma_actual else "Bajista 🔴")
            with col_ind2:
                st.metric(label="Fuerza (RSI 14)", value=f"{rsi_actual:.1f}")
            
            st.markdown("### 📋 Validación de Niveles")
            if rsi_actual > 70:
                st.error("🚨 **Sobrecompra:** Cuidado con compras en este nivel.")
            elif rsi_actual < 30:
                st.warning("⚠️ **Sobreventa:** Vigila posibles rebotes alcistas.")
            else:
                st.success("✅ **Zona Neutra:** Estructura técnica saludable para operar bajo plan.")
        else:
            st.info("Cargando datos del mercado...")

# --- REGLAS INQUEBRANTABLES DE LA ACADEMIA ---
st.markdown("---")
st.subheader("⚙️ Reglas de Oro de Gestión y Psicología")
col_reg1, col_reg2, col_reg3 = st.columns(3)
with col_reg1:
    st.info("**1. Riesgo Máximo:** 1% por operación sin excepciones.")
with col_reg2:
    st.info("**2. Plan Mental:** Si pierdes 2 trades seguidos, apagas la pantalla.")
with col_reg3:
    st.info("**3. Proceso > Dinero:** Concéntrate en ejecutar bien, el resultado llega solo.")

st.markdown("<br><p style='text-align: center; color: gray;'>Academia de Trading Profesional - Versión Centrada en Mindset & Precisión</p>", unsafe_allow_html=True)
