import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import yfinance as yf

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

# --- BLOQUE 1: CONTROL EMOCIONAL (MINDSET) ---
st.sidebar.header("🛡️ 1. Filtro de Psicología y Mindset")
emocion = st.sidebar.selectbox(
    "¿Cómo te sientes en este preciso instante?",
    ["Selecciona tu estado...", "Tranquilo, paciente y disciplinado", "Ansioso / Con FOMO", "Eufórico por una racha ganadora", "Frustrado / Queriendo recuperar pérdidas (Venganza)"]
)

mindset_apto = True
if emocion == "Selecciona tu estado...":
    st.sidebar.info("Selecciona tu estado emocional para desbloquear el análisis.")
    mindset_apto = False
elif emocion != "Tranquilo, paciente y disciplinado":
    mindset_apto = False
    st.sidebar.error("🛑 **BLOQUEO DE MINDSET ACTIVADO:** Tu estado mental actual te hará romper tu gestión. **Queda prohibido operar hoy.**")
else:
    st.sidebar.success("✅ **Mindset Aprobado:** Operando desde la disciplina.")

st.sidebar.markdown("---")
st.sidebar.header("📊 2. Parámetros de Mercado")

activo_seleccionado = st.sidebar.selectbox(
    "Selecciona el Activo", 
    ["Step Index (Deriv / Sintéticos)", "EUR/USD", "Bitcoin (BTC-USD)", "Oro (GC=X)", "S&P 500"]
)
temporalidad = st.sidebar.selectbox("Temporalidad Principal", ["M1", "M5", "M15", "H1"])

# --- OBTENCIÓN DE DATOS SEGÚN EL ACTIVO ---
@st.cache_data(ttl=300)
def cargar_datos(ticker):
    try:
        data = yf.download(ticker, period="5d", interval="1h", progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except:
        return None

# Mapeo seguro
ticker_map = {
    "EUR/USD": "EURUSD=X",
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Oro (GC=X)": "GC=X",
    "S&P 500": "^GSPC"
}

# --- PANEL CENTRAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📷 Carga tus Capturas de Operativa (Hasta 3 fotos)")
    archivos_imagenes = st.file_uploader(
        "Sube tus gráficas", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    if archivos_imagenes:
        st.success(f"¡{len(archivos_imagenes)} imágenes cargadas con éxito!")
        for i, archivo_imagen in enumerate(archivos_imagenes):
            imagen = Image.open(archivo_imagen)
            st.image(imagen, caption=f"Captura #{i+1} del alumno", use_container_width=True)

with col2:
    st.subheader(f"🔍 Diagnóstico Técnico ({activo_seleccionado})")
    
    if not mindset_apto:
        st.warning("🔒 **Diagnóstico Bloqueado:** Protege tu capital protegiendo tu mente primero.")
    else:
        if activo_seleccionado == "Step Index (Deriv / Sintéticos)":
            # Diagnóstico rápido y directo para Índices Sintéticos sin congelarse con APIs externas
            st.metric(label="Estado del Activo (Sintético)", value="Activo en Rango / Tendencia")
            st.info("ℹ️ *Nota para Step Index:* Analiza la estructura de impulsos y retrocesos de 0.5 en tu gráfica cargada.")
            st.success("✅ **Validación Estructural:** Asegúrate de operar a favor de la estructura de temporalidad mayor.")
        else:
            # Para divisas y criptos con datos reales de Yahoo Finance
            ticker_yahoo = ticker_map.get(activo_seleccionado, "EURUSD=X")
            df_mercado = cargar_datos(ticker_yahoo)
            
            if df_mercado is not None and not df_mercado.empty:
                precio_actual = float(df_mercado['Close'].iloc[-1])
                df_mercado['SMA_20'] = df_mercado['Close'].rolling(window=20).mean()
                sma_actual = float(df_mercado['SMA_20'].iloc[-1])
                
                delta = df_mercado['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                rsi_actual = float(rsi.iloc[-1]) if not rsi.empty else 50.0

                st.metric(label=f"Precio Actual ({activo_seleccionado})", value=f"${precio_actual:,.4f}")
                
                col_ind1, col_ind2 = st.columns(2)
                with col_ind1:
                    st.metric(label="Tendencia (SMA 20)", value="Alcista 🟢" if precio_actual > sma_actual else "Bajista 🔴")
                with col_ind2:
                    st.metric(label="Fuerza (RSI 14)", value=f"{rsi_actual:.1f}")
                
                if rsi_actual > 70:
                    st.error("🚨 **Sobrecompra:** Cuidado con compras en este nivel.")
                elif rsi_actual < 30:
                    st.warning("⚠️ **Sobreventa:** Vigila posibles rebotes alcistas.")
                else:
                    st.success("✅ **Zona Neutra:** Estructura técnica saludable.")
            else:
                st.warning("No se pudieron cargar los datos en vivo para este activo en este momento. Guíate estrictamente por tu análisis técnico visual.")

# --- REGLAS DE LA ACADEMIA ---
st.markdown("---")
st.subheader("⚙️ Reglas de Oro de Gestión y Psicología")
col_reg1, col_reg2, col_reg3 = st.columns(3)
with col_reg1:
    st.info("**1. Riesgo Máximo:** 1% por operación.")
with col_reg2:
    st.info("**2. Plan Mental:** 2 pérdidas seguidas y apagas.")
with col_reg3:
    st.info("**3. Proceso:** Ejecuta tu plan sin vacilar.")

st.markdown("<br><p style='text-align: center; color: gray;'>Academia de Trading Profesional - Versión Optimizada</p>", unsafe_allow_html=True)
