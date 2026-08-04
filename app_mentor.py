import streamlit as st
from PIL import Image
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="MentorBot Pro - Niveles y Plan de Trading",
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

st.title("🧠 MentorBot Pro: Gestión, Niveles y Precisión")
st.write("La regla de oro de la academia: **Mindset, Estructura Técnica y Gestión de Riesgo Perfecta.**")

# --- BLOQUE 1: CONTROL EMOCIONAL (MINDSET) ---
st.sidebar.header("🛡️ 1. Filtro de Psicología y Mindset")
emocion = st.sidebar.selectbox(
    "¿Cómo te sientes en este preciso instante?",
    ["Selecciona tu estado...", "Tranquilo, paciente y disciplinado", "Ansioso / Con FOMO", "Eufórico por una racha ganadora", "Frustrado / Queriendo recuperar pérdidas (Venganza)"]
)

mindset_apto = True
if emocion == "Selecciona tu estado...":
    st.sidebar.info("Selecciona tu estado emocional para desbloquear la herramienta.")
    mindset_apto = False
elif emocion != "Tranquilo, paciente y disciplinado":
    mindset_apto = False
    st.sidebar.error("🛑 **BLOQUEO DE MINDSET:** Tu mente no está apta para operar. **Queda prohibido abrir operaciones hoy.**")
else:
    st.sidebar.success("✅ **Mindset Aprobado:** Operando con disciplina.")

st.sidebar.markdown("---")
st.sidebar.header("📊 2. Parámetros de Mercado")

activo_seleccionado = st.sidebar.selectbox(
    "Selecciona el Activo", 
    ["Step Index (Deriv / Sintéticos)", "EUR/USD", "Bitcoin (BTC-USD)", "Oro (GC=X)", "S&P 500"]
)
temporalidad = st.sidebar.selectbox("Temporalidad Principal", ["M1", "M5", "M15", "H1"])

# --- PANEL CENTRAL: FOTOS + GESTIÓN DE NIVELES (SL, TP, ENTRADA) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📷 Carga tus Capturas de Operativa (Hasta 3 fotos)")
    archivos_imagenes = st.file_uploader(
        "Sube tus gráficas (Macro, Estructura y Ejecución)", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    if archivos_imagenes:
        st.success(f"¡{len(archivos_imagenes)} imágenes cargadas con éxito!")
        for i, archivo_imagen in enumerate(archivos_imagenes):
            imagen = Image.open(archivo_imagen)
            st.image(imagen, caption=f"Captura #{i+1} del alumno", use_container_width=True)

with col2:
    st.subheader(f"🎯 Definición de Niveles y Estructura ({activo_seleccionado})")
    
    if not mindset_apto:
        st.warning("🔒 **Panel Bloqueado:** Protege tu capital protegiendo tu mente primero.")
    else:
        # Selector de Figura Chartista
        figura_chartista = st.selectbox(
            "Selecciona la Figura / Patrón Chartista Identificado",
            [
                "Selecciona patrón...", 
                "Canal / Tendencia (Impulsos y Retrocesos)", 
                "Doble Techo / Doble Suelo", 
                "Hombro-Cabeza-Hombro (HCH)", 
                "Triángulo (Simétrico / Ascendente / Descendente)", 
                "Ruptura de Bloque de Órdenes (Order Block / FVG)"
            ]
        )
        
        tipo_operacion = st.radio("Dirección de la Operación:", ["Compra (Long)", "Venta (Short)"], horizontal=True)
        
        # Entradas numéricas para calcular el riesgo (prellenadas con los valores de tu Step Index)
        col_n1, col_n2, col_n3 = st.columns(3)
        with col_n1:
            precio_entrada = st.number_input("Precio de Entrada", value=7802.3118, format="%.4f")
        with col_n2:
            precio_sl = st.number_input("Stop Loss (SL)", value=7795.0000, format="%.4f")
        with col_n3:
            precio_tp = st.number_input("Take Profit (TP)", value=7825.0000, format="%.4f")
            
        # Validación matemática de SL y TP
        if precio_entrada > 0 and precio_sl > 0 and precio_tp > 0:
            riesgo = abs(precio_entrada - precio_sl)
            beneficio = abs(precio_tp - precio_entrada)
            
            if riesgo > 0:
                rr = beneficio / riesgo
                st.markdown("---")
                st.markdown("### 📐 Reporte de Gestión del Trade")
                
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    st.metric(label="Riesgo / Beneficio (R:R)", value=f"1 : {rr:.2f}")
                with col_r2:
                    if figura_chartista != "Selecciona patrón...":
                        st.success(f"✅ **Patrón:** {figura_chartista}")
                    else:
                        st.warning("⚠️ Selecciona la figura chartista.")
                
                # Criterio estricto de la academia (mínimo 1:2)
                if rr >= 2.0:
                    st.success("✅ **Estructura Aprobada:** La relación beneficio/riesgo cumple con el mínimo de 1:2 de la academia.")
                else:
                    st.error("🚨 **Riesgo Elevado / Beneficio Insuficiente:** El ratio R:R es menor a 1:2. No cumple con la gestión profesional.")
            else:
                st.warning("El precio de entrada y el Stop Loss no pueden ser iguales.")
        else:
            st.info("💡 Ingresa los valores numéricos de Entrada, Stop Loss y Take Profit para calcular automáticamente tu ratio.")

# --- REGLAS DE LA ACADEMIA ---
st.markdown("---")
st.subheader("⚙️ Reglas de Oro de Gestión y Psicología")
col_reg1, col_reg2, col_reg3 = st.columns(3)
with col_reg1:
    st.info("**1. Riesgo Máximo:** 1% por operación.")
with col_reg2:
    st.info("**2. Plan Mental:** 2 pérdidas seguidas y apagas.")
with col_reg3:
    st.info("**3. Proceso:** Respeta tu SL y tu estructura chartista.")

st.markdown("<br><p style='text-align: center; color: gray;'>Academia de Trading Profesional - Versión Estable</p>", unsafe_allow_html=True)
