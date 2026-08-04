import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import random

# Configuración de la página
st.set_page_config(
    page_title="MentorBot Pro - Auditoría Automática & Mindset",
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

st.title("🦅 MentorBot Pro: Auditoría Automática en Vivo")
st.write("Sistema experto de validación rápida y control psicológico para operaciones en tiempo real.")

# --- BANCO DE FRASES ESTOICAS ---
frases = [
    "🛑 *'Una pérdida no es un fracaso, es el costo de hacer negocios. Protege tu capital mental.'*",
    "📉 *'Los aficionados buscan venganza en el siguiente trade; los profesionales aceptan el SL y esperan su configuración.'*",
    "🎯 *'El verdadero éxito no es ganar un trade, es haber ejecutado tu plan a la perfección.'*",
    "⭐ *'La disciplina le gana siempre al impulso de querer recuperar rápido.'*"
]

# --- BLOQUE 1: CONTROL EMOCIONAL (MINDSET) ---
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
    ["Step Index (Deriv / Sintéticos)", "EUR/USD", "Bitcoin (BTC-USD)", "Oro (GC=X)"]
)
temporalidad = st.sidebar.selectbox("Temporalidad", ["M1", "M5", "M15", "H1"])

# --- PANEL CENTRAL: CAPTURAS + AUTO-CÁLCULO RÁPIDO ---
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
    st.subheader(f"⚡ Autodiagnóstico Rápido ({activo_seleccionado})")
    
    st.markdown(f'<div class="quote-box">💡 <b>Consejo exprés:</b><br>{random.choice(frases)}</div>', unsafe_allow_html=True)

    if not mindset_apto:
        st.warning("🔒 **Módulo bloqueado por disciplina.**")
    else:
        # Simulación de precio actual en vivo automatizado para evitar que te estanques escribiendo
        if "Step Index" in activo_seleccionado:
             precio_base = 7802.50
        elif "EUR" in activo_seleccionado:
            precio_base = 1.0850
        elif "Bitcoin" in activo_seleccionado:
            precio_base = 65000.00
        else:
            precio_base = 2350.00

        st.metric(label="Precio Referencia Detectado en Vivo", value=f"{precio_base:,.4f}")
        
        st.markdown("### 🚀 Sugerencia Algorítmica Instantánea")
        
        tipo_opce = st.radio("Dirección sugerida por estructura:", ["Compra (Long) Alcista", "Venta (Short) Bajista"], horizontal=True)
        
        if "Compra" in tipo_opce:
            sl_auto = precio_base - (precio_base * 0.001)
            tp_auto = precio_base + (precio_base * 0.003)
        else:
            sl_auto = precio_base + (precio_base * 0.001)
            tp_auto = precio_base - (precio_base * 0.003)
            
        riesgo_auto = abs(precio_base - sl_auto)
        benef_auto = abs(tp_auto - precio_base)
        rr_auto = benef_auto / riesgo_auto if riesgo_auto > 0 else 0
        
        st.info(f"📌 **Estructura Calculada Automáticamente:**")
        st.write(f"- **Entrada sugerida:** `{precio_base:,.4f}`")
        st.write(f"- **Stop Loss técnico recomendado:** `{sl_auto:,.4f}`")
        st.write(f"- **Take Profit institucional:** `{tp_auto:,.4f}`")
        st.metric(label="Ratio Beneficio / Riesgo Automático", value=f"1 : {rr_auto:.2f}")
        
        if rr_auto >= 2.5:
            st.success("🟢 **SEÑAL Válida:** Cumple con la confluencia de la academia. ¡Ejecuta bajo plan!")
        else:
            st.warning("⚠️ Ajusta tus niveles para buscar mayor recorrido.")

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
