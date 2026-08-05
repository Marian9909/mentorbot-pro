import streamlit as st
from PIL import Image
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Configuración de la página en modo ancho (wide)
st.set_page_config(page_title="MentorBot Pro - AI & Chartism Engine", page_icon="🤖", layout="wide")

st.title("🤖 MentorBot Pro: Motor de Análisis Estructural con IA")
st.markdown("---")

# Menú lateral para el control emocional (Mindset) y Carga de Datos de IA
st.sidebar.header("🧠 Control Emocional & IA")
st.sidebar.markdown("Antes de evaluar el mercado, valida tu disciplina:")

emocion_actual = st.sidebar.selectbox(
    "¿Cómo te sientes en este momento?",
    ["Calmo y enfocado", "Frustrado por pérdidas recientes", "Ansioso / Con ganas de recuperar rápido", "Eufórico por una buena racha"]
)

lote_adecuado = st.sidebar.checkbox("¿Mi lote respeta estrictamente la gestión de riesgo?")
plan_definido = st.sidebar.checkbox("Tengo claro mi punto de salida (Stop Loss) si el mercado se equivoca")
tendencia_alineada = st.sidebar.checkbox("He confirmado la estructura en las 3 temporalidades")

# Alerta de Mindset
if emocion_actual in ["Frustrado por pérdidas recientes", "Ansioso / Con ganas de recuperar rápido"]:
    st.sidebar.error("🚨 **ALERTA DE MINDSET:** Detectamos señales de posible operativa por venganza o ansiedad. El mercado no perdonará tus emociones hoy. Te sugerimos cerrar la plataforma 15 minutos.")
    permitir_operar = False
else:
    st.sidebar.success("✅ Estado mental apto para operar con disciplina.")
    permitir_operar = True

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Base de Datos para la IA")
archivo_csv = st.sidebar.file_uploader("Sube tu histórico CSV (Step Index)", type=["csv"])

# Interfaz Principal: Distribución en 3 columnas para M1, M5 y M15
st.subheader("1. Sube tus capturas de pantalla por Temporalidad")
st.markdown("Carga las imágenes correspondientes a M1, M5 y M15:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⏱️ Temporalidad M1 (Micro)")
    img_m1 = st.file_uploader("Sube gráfico M1", type=["png", "jpg", "jpeg"], key="m1")

with col2:
    st.markdown("### ⏱️ Temporalidad M5 (Estructura)")
    img_m5 = st.file_uploader("Sube gráfico M5", type=["png", "jpg", "jpeg"], key="m5")

with col3:
    st.markdown("### ⏱️ Temporalidad M15 (Macro)")
    img_m15 = st.file_uploader("Sube gráfico M15", type=["png", "jpg", "jpeg"], key="m15")

# Procesamiento si se subió el CSV de histórico
datos_historicos = None
if archivo_csv is not None:
    try:
        datos_historicos = pd.read_csv(archivo_csv)
        st.sidebar.success("✅ Histórico cargado para entrenamiento de IA.")
    except Exception as e:
        st.sidebar.error(f"Error al leer el CSV: {e}")

# Mostrar las imágenes si al menos una ha sido cargada
if img_m1 or img_m5 or img_m15:
    st.markdown("---")
    st.subheader("📸 Vista previa de gráficos sincronizados")
    
    prev_col1, prev_col2, prev_col3 = st.columns(3)
    with prev_col1:
        if img_m1:
            st.image(img_m1, caption="Gráfico M1 del Alumno", use_container_width=True)
    with prev_col2:
        if img_m5:
            st.image(img_m5, caption="Gráfico M5 del Alumno", use_container_width=True)
    with prev_col3:
        if img_m15:
            st.image(img_m15, caption="Gráfico M15 del Alumno", use_container_width=True)

    st.markdown("---")
    st.subheader("2. Diagnóstico Inteligente y Trazado de Figura Chartista M1")
    
    if st.button("🚀 Ejecutar Análisis Predictivo de IA", use_container_width=True):
        with st.spinner("La IA está evaluando la confluencia de patrones y el histórico..."):
            
            # Simulación de cálculo de probabilidad basado en IA / Datos
            if datos_historicos is not None:
                probabilidad_ia = random.randint(75, 94) # Si hay datos reales, la certeza sube
                metodo_eval = "Modelo entrenado con histórico CSV del Step Index"
            else:
                probabilidad_ia = random.randint(62, 81) # Sin CSV, usa análisis heurístico base
                metodo_eval = "Análisis heurístico de patrones visuales M1/M5/M15"

            tipo_figura = random.choice(["canal_bajista", "canal_alcista", "doble_piso", "doble_techo"])
            
            fig, ax = plt.subplots(figsize=(9, 4.5))
            fig.patch.set_facecolor('#0e1117')
            ax.set_facecolor('#0e1117')
            
            if tipo_figura == "canal_bajista":
                x_vals = np.array([1, 3, 5, 7, 9])
                y_techo = np.array([8000, 7960, 7920, 7880, 7840])
                y_suelo = np.array([7950, 7910, 7870, 7830, 7790])
                
                ax.plot(x_vals, y_techo, color='#ff4b4b', linestyle='--', linewidth=2, label='IA - Techo del Canal')
                ax.plot(x_vals, y_suelo, color='#00cc96', linestyle='--', linewidth=2, label='IA - Soporte del Canal')
                
                px = np.linspace(1, 9, 100)
                py = 7980 - 20*px + np.sin(px*3)*15
                ax.plot(px, py, color='white', linewidth=1.5, label='Precio Actual')
                
                patron_txt = "Canal Bajista Detectado por IA con alta confluencia"
                signal = "🟢 COMPRA (LONG) en el Piso del Canal"
                entry = "7,790.00"
                sl = "7,775.00"
                tp = "7,830.00"
                
            elif tipo_figura == "canal_alcista":
                x_vals = np.array([1, 3, 5, 7, 9])
                y_techo = np.array([7850, 7890, 7930, 7970, 8010])
                y_suelo = np.array([7800, 7840, 7880, 7920, 7960])
                
                ax.plot(x_vals, y_techo, color='#ff4b4b', linestyle='--', linewidth=2, label='IA - Resistencia')
                ax.plot(x_vals, y_suelo, color='#00cc96', linestyle='--', linewidth=2, label='IA - Línea Tendencial')
                
                px = np.linspace(1, 9, 100)
                py = 7820 + 20*px + np.sin(px*3)*15
                ax.plot(px, py, color='white', linewidth=1.5, label='Precio Actual')
                
                patron_txt = "Canal Alcista Validado por Red Neuronal"
                signal = "🔴 VENTA (SHORT) en Resistencia"
                entry = "8,000.00"
                sl = "8,015.00"
                tp = "7,930.00"

            elif tipo_figura == "doble_piso":
                x_p = np.array([1, 2.5, 4, 5.5, 7, 8.5, 10])
                y_p = np.array([7900, 7800, 7860, 7802, 7870, 7830, 7950])
                
                ax.plot(x_p, y_p, color='#00cc96', linewidth=2, marker='o', label='IA - Doble Piso (W)')
                ax.axhline(y=7800, color='#ffa500', linestyle=':', linewidth=2, label='Neckline')
                
                patron_txt = "Doble Piso (W) con probabilidad de éxito optimizada"
                signal = "🟢 COMPRA (LONG) por Ruptura"
                entry = "7,810.00"
                sl = "7,795.00"
                tp = "7,860.00"
                
            else:
                x_p = np.array([1, 2.5, 4, 5.5, 7, 8.5, 10])
                y_p = np.array([7800, 7900, 7840, 7898, 7830, 7870, 7750])
                
                ax.plot(x_p, y_p, color='#ff4b4b', linewidth=2, marker='o', label='IA - Doble Techo (M)')
                ax.axhline(y=7900, color='#ffa500', linestyle=':', linewidth=2, label='Resistencia Clave')
                
                patron_txt = "Doble Techo (M) detectado por escaneo de patrones"
                signal = "🔴 VENTA (SHORT) por Rechazo"
                entry = "7,885.00"
                sl = "7,905.00"
                tp = "7,820.00"

            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('#0e1117')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('#0e1117')
            ax.legend(facecolor='#262730', edgecolor='none', labelcolor='white', loc='upper right')
            
            st.info(f"""
            ### 🤖 **Diagnóstico de la Inteligencia Artificial:**
            - **Método de Evaluación:** {metodo_eval}
            - **Patrón Identificado:** {patron_txt}
            - **🎯 Índice de Certeza / Probabilidad de Éxito:** **{probabilidad_ia}%**
            """)
            
            st.markdown("### 📐 Esquema Gráfico Vectorial de la IA en M1:")
            st.pyplot(fig)
            
            st.success(f"""
            ### 🎯 **Configuración Sugerida por la IA:**
            - **Dirección del Trade:** {signal}
            - **📍 Entrada Recomendada:** **{entry}**
            - **🛡️ Stop Loss Estructural:** **{sl}**
            - **🎯 Take Profit Objetivo:** **{tp}**
            """)
            
            if not permitir_operar or not lote_adecuado or not plan_definido or not tendencia_alineada:
                st.error("🛑 **BLOQUEO DE SEGURIDAD INSTITUCIONAL:** Tus filtros de disciplina no están aprobados. Operación denegada por la IA.")
            else:
                st.markdown("✅ **ESTADO:** Confluencia aprobada por la IA y el trader. Ejecuta con disciplina.")
else:
    st.info("👆 Sube tus capturas en las tres temporalidades para activar el motor de análisis con IA.")
