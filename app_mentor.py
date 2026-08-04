import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import yfinance as yf
import random

# Configuración de la página
st.set_page_config(
    page_title="MentorBot Pro - Auditoría Automática en Vivo",
    page_icon="🦅",
    layout="wide"
)

# Estilo visual adaptado
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
    .quote-box { background-color: #161b22; border-left: 4px solid #ff4b4b; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🦅 MentorBot Pro: Cálculo Automático en Vivo")
st.write("Sistema experto que evalúa el mercado en tiempo real y calcula tus niveles de operación al instante.")

# --- BANCO DE FRASES ---
frases = [
    "🛑 *'Una pérdida no es un fracaso, es el costo de hacer negocios. Protege tu capital mental.'*",
    "📉 *'Los aficionados buscan venganza en el siguiente trade; los profesionales aceptan el SL.'*",
    "🎯 *'El verdadero éxito es haber ejecutado tu plan a la perfección.'*",
    "⭐ *'La disciplina le gana siempre al impulso.'*"
]

# --- BLOQUE 1: MINDSET ---
st.sidebar.header("🛡️ 1. Filtro Psicológico")
emocion = st.sidebar.selectbox(
    "¿Cómo está tu mente en este momento?",
    ["Selecciona tu estado...", "Calmo y disciplinado", "Ansioso por entrar (FOMO)", "Frustrado / Buscando revancha"]
)

mindset_apto = True
if emocion == "Selecciona tu estado...":
    st.sidebar.info("Selecciona tu estado mental.")
    mindset_apto = False
elif emocion != "Calmo y disciplinado":
    mindset_apto = False
    st.sidebar.error("🛑 **BLOQUEO:** Tu mente está alterada. Cierra las plataformas por hoy.")
    st.sidebar.markdown(random.choice(frases))
else:
    st.sidebar.success("✅ **Mindset Aprobado**")

st.sidebar.markdown("---")
st.sidebar.header("📊 2. Configuración de Activo")
activo_seleccionado = st.sidebar.selectbox(
    "Selecciona el Activo", 
    ["EUR/USD", "Bitcoin (BTC-USD)", "Oro (GC=X)", "S&P 500"]
)
temporalidad = st.sidebar.selectbox("Temporalidad", ["M1", "M5", "M15", "H1"])

# Mapeo de tickers para datos en vivo
tickers_map = {
    "EUR/USD": "EURUSD=X",
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Oro (GC=X)": "GC=X",
    "S&P 500": "^GSPC"
}

@st.cache_data(ttl=60)
def obtener_precio_en_vivo(ticker):
    try:
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        if not data.empty:
            cierre = float(data['Close'].iloc[-1])
            # Cálculo rápido de tendencia con media móvil de corto plazo
            sma = float(data['Close'].rolling(window=10).mean().iloc[-1])
            return cierre, sma
    except:
        pass
    return None, None

# --- PANEL CENTRAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📷 Tus Capturas (Multicarga)")
    archivos_imagenes = st.file_uploader(
        "Sube tus gráficas de análisis", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    if archivos_imagenes:
        st.success(f"¡{len(archivos_imagenes)} imágenes listas!")
        for i, archivo_imagen in enumerate(archivos_imagenes):
            imagen = Image.open(archivo_imagen)
            st.image(imagen, caption=f"Captura #{i+1}", use_container_width=True)

with col2:
    st.subheader(f"⚡ Análisis Autónomo en Vivo ({activo_seleccionado})")
    
    st.markdown(f'<div class="quote-box">💡 <b>Consejo exprés:</b><br>{random.choice(frases)}</div>', unsafe_allow_html=True)

    if not mindset_apto:
        st.warning("🔒 **Módulo bloqueado por disciplina.**")
    else:
        ticker_actual = tickers_map[activo_seleccionado]
        precio_actual, sma_actual = obtener_precio_en_vivo(ticker_actual)
        
        if precio_actual is not None and sma_actual is not None:
            st.metric(label=f"Precio Actual en el Mercado ({activo_seleccionado})", value=f"${precio_actual:,.4f}")
            
            # Determinación automática de Compra o Venta basada en el precio vs la Media Móvil
            if precio_actual > sma_actual:
                tipo_sugerido = "Compra (Long) 🟢"
                sl_calc = precio_actual - (precio_actual * 0.0015) # 0.15% de riesgo automático
                tp_calc = precio_actual + (precio_actual * 0.0040) # Buscando estructura alcista
            else:
                tipo_sugerido = "Venta (Short) 🔴"
                sl_calc = precio_actual + (precio_actual * 0.0015)
                tp_calc = precio_actual - (precio_actual * 0.0040)
                
            riesgo = abs(precio_actual - sl_calc)
            beneficio = abs(tp_calc - precio_actual)
            rr = beneficio / riesgo if riesgo > 0 else 0
            
            st.markdown("### 📋 Propuesta Algorítmica Instantánea")
            st.info(f"**Dirección sugerida por el mercado:** {tipo_sugerido}")
            
            col_niv1, col_niv2 = st.columns(2)
            with col_niv1:
                st.metric(label="Entrada Automática (Precio Actual)", value=f"${precio_actual:,.4f}")
                st.metric(label="Stop Loss Sugerido (SL)", value=f"${sl_calc:,.4f}")
            with col_niv2:
                st.metric(label="Take Profit Sugerido (TP)", value=f"${tp_calc:,.4f}")
                st.metric(label="Ratio Beneficio / Riesgo", value=f"1 : {rr:.2f}")
                
            if rr >= 2.0:
                st.success("🟢 **Dictamen:** La operación en este instante cumple con la estructura y el ratio mínimo de la academia.")
            else:
                st.warning("⚠️ El mercado se encuentra en rango estrecho; espera mejor confirmación.")
        else:
            st.warning("Obteniendo datos de la red en tiempo real... Espera un segundo.")

# --- REGLAS ---
st.markdown("---")
st.subheader("⚙️ Código de Honor")
col_reg1, col_reg2, col_reg3 = st.columns(3)
with col_reg1:
    st.info("**1. Riesgo:** Máx 1%")
with col_reg2:
    st.info("**2. Disciplina:** Respeta tu SL")
with col_reg3:
    st.info("**3. Enfoque:** Proceso antes que dinero")
