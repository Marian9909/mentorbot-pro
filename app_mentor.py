import streamlit as st
from PIL import Image
import pandas as pd
from streamlit_drawable_canvas import st_canvas

# Configuración de la página
st.set_page_config(
    page_title="MentorBot Pro - Dibujo y Análisis Visual",
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

st.title("🤖 MentorBot Pro: Trazado y Análisis Visual Directo")
st.write("Herramienta ágil con lienzo interactivo para marcar tus figuras chartistas en tiempo real.")

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

# --- PANEL CENTRAL: MULTICARGA DE FOTOS + LIENZO DE DIBUJO ---
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
    st.subheader(f"✏️ Trazado de Figura Chartista ({activo_seleccionado})")
    st.info("Selecciona la herramienta y dibuja el patrón (canal, línea de tendencia o soporte) sobre el recuadro:")
    
    # Controles para el lienzo de dibujo
    drawing_mode = st.selectbox(
        "Herramienta de dibujo:",
        ("line", "rect", "freedraw", "transform")
    )
    
    stroke_color = st.color_picker("Color del trazo:", "#00FF00")
    stroke_width = st.slider("Grosor de línea:", 1, 10, 2)
    
    # Lienzo interactivo donde puedes trazar encima
    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="#1e1e1e",
        height=300,
        drawing_mode=drawing_mode,
        key="canvas_patron",
    )
    
    st.markdown("### 📋 Checklist de Validación Rápida")
    st.markdown("""
    * **Estructura:** ¿El trazo coincide con los impulsos y retrocesos del Step Index?
    * **Entrada y SL:** Valida visualmente que tu Stop Loss esté protegiendo el último fractal.
    * **Ratio R:R:** Asegúrate de que el beneficio proyectado sea al menos el doble del riesgo.
    """)
    st.success("✅ **Listo para operar:** Mantén la disciplina y ejecuta de acuerdo a tu plan.")

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

st.markdown("<br><p style='text-align: center; color: gray;'>Academia de Trading Profesional - Versión Visual y de Trazado Directo</p>", unsafe_allow_html=True)
