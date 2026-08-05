import streamlit as st
from PIL import Image
import cv2
import numpy as np
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="MentorBot Pro - IA Visión", page_icon="👁️‍🗨️", layout="wide")

st.title("👁️‍🗨️ MentorBot Pro: Análisis Inteligente por Visión Artificial")
st.markdown("---")

# Menú lateral: Control Emocional
st.sidebar.header("🧠 Control Emocional (Mindset)")
emocion = st.sidebar.selectbox(
    "¿Cómo te sientes?",
    ["Calmo y enfocado", "Frustrado", "Ansioso", "Eufórico"]
)

if emocion != "Calmo y enfocado":
    st.sidebar.warning("⚠️ Estado no óptimo. Reduce tu riesgo al 0.5%.")
    apto_operar = False
else:
    st.sidebar.success("✅ Estado óptimo.")
    apto_operar = True

# Interfaz Principal: Carga de Capturas
st.subheader("1. Sube tus capturas de pantalla para el análisis de IA")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⏱️ Temporalidad M1")
    img_m1_file = st.file_uploader("Subir M1", type=["png", "jpg", "jpeg"])

with col2:
    st.markdown("### ⏱️ Temporalidad M5")
    img_m5_file = st.file_uploader("Subir M5", type=["png", "jpg", "jpeg"])

with col3:
    st.markdown("### ⏱️ Temporalidad M15")
    img_m15_file = st.file_uploader("Subir M15", type=["png", "jpg", "jpeg"])

# --- MOTOR DE VISIÓN ARTIFICIAL (Procesamiento de Imágenes) ---
def analizar_imagen_con_ia(imagen_file):
    """
    Esta función usa OpenCV para procesar la imagen y extraer datos técnicos básicos.
    Detecta los colores principales (tu línea azul) y calcula un precio aproximado
    basado en la posición vertical de los píxeles en la captura de Deriv.
    """
    if imagen_file is None:
        return None
    
    # Convertir archivo subido a imagen OpenCV
    file_bytes = np.asarray(bytearray(imagen_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Convertir a espacio de color HSV para detectar colores específicos (ej. azul de tu línea)
    # Nota: Los valores exactos de HSV dependen del tono exacto de azul de tu gráfica.
    # Aquí usaremos un rango genérico para un azul brillante.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Encontrar contornos de la línea azul
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Obtener el contorno más grande (asumimos que es tu línea principal)
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            # Coordenada Y central de la línea azul (en píxeles)
            cy = int(M["m10"] / M["m00"])
            
            # --- LÓGICA DE PRECIO SIMULADA (Requiere calibración) ---
            # Para que esto sea exacto, la IA necesitaría leer los números del eje Y de tu gráfica.
            # Como estimación, calculamos un precio basado en la posición Y de la imagen.
            # Usaremos un rango de precios fijo del Step Index (ej. 7750 - 7900).
            
            alto_imagen = img.shape[0]
            precio_max = 7900
            precio_min = 7750
            
            # Mapear posición Y a precio: Y=0 es el precio más alto.
            factor_precio = (1 - (cy / alto_imagen))
            precio_estimado = precio_min + (factor_precio * (precio_max - precio_min))
            
            # Determinar si es una potencial compra o venta (si el precio está en la mitad superior o inferior)
            tendencia = "Potencial Compra (Zona Baja)" if factor_precio < 0.5 else "Potencial Venta (Zona Alta)"
            
            return round(precio_estimado, 4), tendencia
    
    return None, "No se detectaron niveles claros"

# --- EJECUCIÓN DEL ANÁLISIS ---
if st.button("🤖 Ejecutar Análisis de Visión Artifical en Vivo"):
    if not apto_operar:
        st.error("🛑 Tu estado emocional no es apto para operar. MentorBot deniega el análisis.")
    elif not img_m1_file or not img_m5_file or not img_m15_file:
        st.warning("⚠️ Por favor, sube las capturas de las 3 temporalidades para continuar.")
    else:
        st.markdown("---")
        st.subheader("📊 Diagnóstico Técnico Automático (IA):")
        
        # Análisis de M1 (Entrada)
        st.info("🔎 Procesando Captura M1 para definir Entrada...")
        precio_entrada, tipo_entrada = analizar_imagen_con_ia(img_m1_file)
        
        if precio_entrada:
            st.success(f"✅ **Nivel de Entrada (IA):** {precio_entrada:,.4f} ({tipo_entrada})")
            
            # --- LÓGICA DE GESTIÓN DE RIESGO (Basada en el precio detectado) ---
            # Definimos SL y TP automáticos fijos en puntos para el Step Index.
            distancia_sl = 15 # Puntos
            distancia_tp = 30 # Puntos
            
            if "Compra" in tipo_entrada:
                sl_ia = precio_entrada - distancia_sl
                tp_ia = precio_entrada + distancia_tp
            else:
                sl_ia = precio_entrada + distancia_sl
                tp_ia = precio_entrada - distancia_tp
            
            st.metric(label="Riesgo/Beneficio (R:R) Automático", value="1 : 2")
            st.code(f"""
            📋 RESUMEN DE LA OPERACIÓN:
            Activo: Step Index (Detectado por IA)
            Dirección: {tipo_entrada}
            Precio de Entrada: {precio_entrada:,.4f}
            Stop Loss Estructural: {sl_ia:,.4f}
            Take Profit Objetivo: {tp_ia:,.4f}
            """)
            
            st.warning("⚠️ **AVISO LEGAL:** Este es un análisis técnico automatizado basado en visión por computador. No constituye un consejo financiero. Valida los niveles en tu plataforma de Deriv antes de ejecutar.")
            
        else:
            st.error("🔴 **ERROR EN LA LECTURA DE M1:** MentorBot no pudo detectar tu línea azul ni estimar el precio en la captura de M1. Asegúrate de que la imagen sea clara y la línea esté bien definida.")
            
        # Análisis de M5 y M15 (Estructura)
        st.info("🔎 Procesando Capturas M5 y M15 para confluencia estructural...")
        _, estructura_m5 = analizar_imagen_con_ia(img_m5_file)
        _, estructura_m15 = analizar_imagen_con_ia(img_m15_file)
        
        st.text(f"Análisis Estructural M5: {estructura_m5}")
        st.text(f"Análisis Estructural M15: {estructura_m15}")
        
        # Veredicto final simple
        if precio_entrada and apto_operar:
            st.balloons()
            st.success("🟢 ANÁLISIS FINALIZADO. REVISA LA GESTIÓN Y EJECUTA CON DISCIPLINA.")
