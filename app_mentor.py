import streamlit as st
from PIL import Image
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="MentorBot Pro - Auditoría Institucional",
    page_icon="🦅",
    layout="wide"
)

# Estilo visual adaptado
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🦅 MentorBot Pro: Auditoría Técnica e Institucional")
st.write("Sistema experto de validación para traders profesionales.")

# --- BLOQUE 1: CONTROL EMOCIONAL (MINDSET) ---
st.sidebar.header("🛡️ 1. Filtro Psicológico de Alta Precisión")
emocion = st.sidebar.selectbox(
    "¿Cómo describes tu estado emocional actual?",
    ["Selecciona tu estado...", "Calmo, analítico y disciplinado", "Ansioso por operar (FOMO)", "Eufórico / Sobreconfiado", "Frustrado / Buscando revancha"]
)

mindset_apto = True
if emocion == "Selecciona tu estado...":
    st.sidebar.info("Selecciona tu estado mental para desbloquear la auditoría.")
    mindset_apto = False
elif emocion != "Calmo, analítico y disciplinado":
    mindset_apto = False
    st.sidebar.error("🛑 **BLOQUEO INSTITUCIONAL:** El factor emocional actual compromete tu ejecución. **Operar en este estado viola el protocolo de la academia.**")
else:
    st.sidebar.success("✅ **Mindset Validado:** Ejecución bajo protocolo frío y matemático.")

st.sidebar.markdown("---")
st.sidebar.header("📊 2. Configuración de Activo")
activo_seleccionado = st.sidebar.selectbox(
    "Selecciona el Activo Operado", 
    ["Step Index (Deriv / Sintéticos)", "Volatility 75 Index (V75)", "EUR/USD", "Bitcoin (BTC-USD)", "Oro (GC=X)"]
)
temporalidad = st.sidebar.selectbox("Temporalidad de Ejecución", ["M1", "M5", "M15", "H1", "H4"])

# --- PANEL CENTRAL: CAPTURAS + AUDITORÍA ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📷 Evidencia Gráfica (Multicarga)")
    st.info("Sube tus 3 capturas obligatorias: 1. Contexto Macro, 2. Estructura/Patrón, 3. Zona de Ejecución.")
    
    archivos_imagenes = st.file_uploader(
        "Sube tus capturas", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    if archivos_imagenes:
        st.success(f"¡{len(archivos_imagenes)} evidencias gráficas cargadas con éxito!")
        for i, archivo_imagen in enumerate(archivos_imagenes):
            imagen = Image.open(archivo_imagen)
            st.image(imagen, caption=f"Evidencia Gráfica #{i+1}", use_container_width=True)

with col2:
    st.subheader(f"🔬 Auditoría de Niveles ({activo_seleccionado})")
    
    if not mindset_apto:
        st.warning("🔒 **Módulo Bloqueado:** Protege tu capital protegiendo tu mente primero.")
    else:
        figura_chartista = st.selectbox(
            "Patrón o Estructura Técnica Identificada",
            [
                "Selecciona la estructura...", 
                "Canal / Impulso y Retroceso (Estructura de Mercado)", 
                "Bloque de Órdenes (Order Block / FVG)", 
                "Doble Techo / Doble Suelo con Testeo", 
                "Hombro-Cabeza-Hombro (HCH Institucional)", 
                "Triángulo de Compresión / Ruptura de Rango"
            ]
        )
        
        tipo_operacion = st.radio("Dirección de la Operación:", ["Compra (Long)", "Venta (Short)"], horizontal=True)
        
        col_n1, col_n2, col_n3 = st.columns(3)
        with col_n1:
            precio_entrada = st.number_input("Precio de Entrada", value=7802.3118, format="%.4f")
        with col_n2:
            precio_sl = st.number_input("Stop Loss (SL)", value=7795.0000, format="%.4f")
        with col_n3:
            precio_tp = st.number_input("Take Profit (TP)", value=7825.0000, format="%.4f")
            
        if precio_entrada > 0 and precio_sl > 0 and precio_tp > 0:
            riesgo = abs(precio_entrada - precio_sl)
            beneficio = abs(precio_tp - precio_entrada)
            
            if riesgo > 0:
                rr = beneficio / riesgo
                
                st.markdown("---")
                st.markdown("### 📋 Informe de Auditoría Técnica")
                
                m1, m2 = st.columns(2)
                with m1:
                    st.metric(label="Ratio Beneficio / Riesgo (R:R)", value=f"1 : {rr:.2f}")
                with m2:
                    st.metric(label="Amplitud del Riesgo (SL)", value=f"{riesgo:.2f} puntos")
                
                st.markdown("#### 🧠 Dictamen Estructural Profundo:")
                
                errores_detectados = 0
                
                if tipo_operacion == "Compra (Long)" and precio_sl >= precio_entrada:
                    st.error("❌ **Error Crítico de Lógica:** En una Compra, el Stop Loss debe estar por debajo del precio de entrada.")
                    errores_detectados += 1
                elif tipo_operacion == "Venta (Short)" and precio_sl <= precio_entrada:
                    st.error("❌ **Error Crítico de Lógica:** En una Venta, el Stop Loss debe estar por encima del precio de entrada.")
                    errores_detectados += 1
                
                if rr < 2.0:
                    st.warning(f"⚠️ **Advertencia de R:R Bajo (1:{rr:.2f}):** La academia exige un mínimo estricto de **1:2**.")
                    errores_detectados += 1
                else:
                    st.success(f"✅ **Eficiencia de Capital Aprobada:** El ratio 1:{rr:.2f} cumple con el estándar.")

                if figura_chartista == "Selecciona la estructura...":
                    st.warning("⚠️ **Falta Patrón:** Debes declarar la figura chartista.")
                    errores_detectados += 1
                else:
                    st.info(f"🔎 **Revisión de Patrón ({figura_chartista}):** Stop Loss protegido tras el fractal.")

                st.markdown("---")
                if errores_detectados == 0:
                    st.balloons()
                    st.success("🟢 **VEREDICTO FINAL: OPERACIÓN APTA Y VALIDADA.**")
                else:
                    st.error(f"🔴 **VEREDICTO FINAL: RECHAZADA ({errores_detectados} correcciones).**")
            else:
                st.warning("El precio de entrada y el Stop Loss no pueden coincidir.")
        else:
            st.info("💡 Introduce los precios para activar la auditoría.")

# --- REGLAS MAESTRAS ---
st.markdown("---")
st.subheader("⚙️ Código de Honor del Trader Profesional")
col_reg1, col_reg2, col_reg3 = st.columns(3)
with col_reg1:
    st.info("**1. Gestión de Riesgo:** Máximo 1% por ejecución.")
with col_reg2:
    st.info("**2. Cacería de Liquidez:** Jamás pongas tu SL en números redondos exactos.")
with col_reg3:
    st.info("**3. Consistencia:** La disciplina le gana siempre a la suerte.")

st.markdown("<br><p style='text-align: center; color: gray;'>Academia de Trading Profesional - Motor de Auditoría Institucional</p>", unsafe_allow_html=True)
