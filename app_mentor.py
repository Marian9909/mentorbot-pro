import streamlit as st
from PIL import Image
from google import genai

# Configuración de la página en modo ancho
st.set_page_config(page_title="MentorBot Pro - Analista IA con Visión", page_icon="📈", layout="wide")

st.title("📊 MentorBot Pro: Analista Técnico con Visión Artificial")
st.markdown("---")

# Panel lateral para la clave de API de Gemini y Mindset
st.sidebar.header("🔑 Configuración de IA")
api_key = st.sidebar.text_input("Ingresa tu Google Gemini API Key:", type="password")

st.sidebar.markdown("---")
st.sidebar.header("🧠 Control Emocional")
emocion = st.sidebar.selectbox("Estado mental:", ["Calmo y enfocado", "Frustrado", "Ansioso"])

# Interfaz Principal: Carga de Capturas
st.subheader("1. Sube tus capturas de pantalla para que el Analista las examine")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⏱️ Temporalidad M1")
    img_m1 = st.file_uploader("Subir M1", type=["png", "jpg", "jpeg"], key="m1")

with col2:
    st.markdown("### ⏱️ Temporalidad M5")
    img_m5 = st.file_uploader("Subir M5", type=["png", "jpg", "jpeg"], key="m5")

with col3:
    st.markdown("### ⏱️ Temporalidad M15")
    img_m15 = st.file_uploader("Subir M15", type=["png", "jpg", "jpeg"], key="m15")

# Si el usuario sube al menos una imagen y coloca su API Key
if (img_m1 or img_m5 or img_m15) and api_key:
    st.markdown("---")
    st.subheader("📸 Evidencias Gráficas Sincronizadas")
    
    # Lista para almacenar las imágenes cargadas para la IA
    imagenes_pil = []
    
    p1, p2, p3 = st.columns(3)
    with p1:
        if img_m1:
            im1 = Image.open(img_m1)
            st.image(im1, caption="Gráfico M1", use_container_width=True)
            imagenes_pil.append(im1)
    with p2:
        if img_m5:
            im5 = Image.open(img_m5)
            st.image(im5, caption="Gráfico M5", use_container_width=True)
            imagenes_pil.append(im5)
    with p3:
        if img_m15:
            im15 = Image.open(img_m15)
            st.image(im15, caption="Gráfico M15", use_container_width=True)
            imagenes_pil.append(im15)

    st.markdown("---")
    activo_objetivo = st.selectbox("Activo analizado en las capturas:", ["Step Index", "Oro (XAUUSD)", "Bitcoin (BTC)"])
    
    if st.button("🚀 Ejecutar Análisis con Visión de IA", use_container_width=True):
        with st.spinner("El analista de IA está examinando la estructura de tus gráficos..."):
            try:
                # Inicializar el cliente de la API de Google GenAI
                client = genai.Client(api_key=api_key)
                
                prompt_analisis = (
                    f"Eres un analista técnico institucional experto en trading de {activo_objetivo}. "
                    "Analiza las imágenes de las temporalidades proporcionadas. "
                    "Identifica la estructura de precios actual, la tendencia dominante, y determina si el sesgo técnico "
                    "es de COMPRA o de VENTA. Proporciona un informe detallado con la justificación basada en lo que ves en las gráficas."
                )
                
                # Preparar el contenido para la API (Prompt + Imágenes)
                contenido_multimodal = [prompt_analisis] + imagenes_pil
                
                # Llamada al modelo multimodal (Gemini 2.5 Flash / Pro)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contenido_multimodal
                )
                
                st.markdown("---")
                st.subheader("📑 Informe Técnico del Analista de IA")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"❌ Ocurrió un error al procesar el análisis con la IA: {e}")
elif (img_m1 or img_m5 or img_m15) and not api_key:
    st.warning("⚠️ Por favor ingresa tu **Google Gemini API Key** en el panel lateral para permitir que la IA analice tus imágenes.")
else:
    st.info("👆 Sube al menos una captura de pantalla en las temporalidades y coloca tu clave de API para activar el análisis visual.")
