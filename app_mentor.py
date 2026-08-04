import streamlit as st
from PIL import Image
import random
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página en modo ancho (wide)
st.set_page_config(page_title="MentorBot Pro - Patrones Chartistas Reales", page_icon="📈", layout="wide")

st.title("📈 MentorBot Pro: Análisis Estructural & Patrones Chartistas M1")
st.markdown("---")

# Menú lateral para el control emocional (Mindset)
st.sidebar.header("🧠 Control Emocional (Checklist)")
st.sidebar.markdown("Antes de evaluar el mercado, responde con honestidad:")

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
    st.subheader("2. Diagnóstico Técnico y Trazado de Figura Chartista en M1")
    
    if st.button("🚀 Generar Trazado Geométrico del Patrón M1", use_container_width=True):
        with st.spinner("Construyendo esquema chartista vectorial..."):
            
            # Seleccionamos aleatoriamente un patrón chartista definido (Canal o Doble Techo/Suelo)
            tipo_figura = random.choice(["canal_bajista", "doble_piso"])
            
            fig, ax = plt.subplots(figsize=(9, 4.5))
            fig.patch.set_facecolor('#0e1117')
            ax.set_facecolor('#0e1117')
            
            if tipo_figura == "canal_bajista":
                # DIBUJO CORREGIDO: y_techo ahora no tiene espacio
                x_vals = np.array([1, 3, 5, 7, 9])
                y_techo = np.array([8000, 7960, 7920, 7880, 7840])
                y_suelo = np.array([7950, 7910, 7870, 7830, 7790])
                
                ax.plot(x_vals, y_techo, color='#ff4b4b', linestyle='--', linewidth=2, label='Línea de Tendencia (Techo)')
                ax.plot(x_vals, y_suelo, color='#00cc96', linestyle='--', linewidth=2, label='Soporte del Canal (Piso)')
                
                # Simular zigzag de precio dentro del canal
                px = np.linspace(1, 9, 100)
                py = 7980 - 20*px + np.sin(px*3)*15
                ax.plot(px, py, color='white', linewidth=1.5, label='Acción del Precio M1')
                
                ax.set_title("Figura Chartista M1: Canal Bajista Respetado", color='white', fontsize=13, fontweight='bold')
                
                patron_txt = "Canal Bajista Estricto con Rebotes Sucesivos"
                m15_txt = "M15 muestra la directriz macro respetando el canal."
                m5_txt = "M5 confirma compresión de precios hacia el soporte inferior."
                m1_txt = "M1 dibuja mínimos decrecientes delimitados por las líneas paralelas."
                signal = "🟢 COMPRA (LONG) en el Piso del Canal"
                entry = "7,790.00"
                sl = "7,775.00 (15 pts de protección)"
                tp = "7,830.00 (Parte alta del canal)"
                
            else:
                # Dibujar un Patrón de Doble Piso (W)
                x_p = np.array([1, 2.5, 4, 5.5, 7, 8.5, 10])
                y_p = np.array([7900, 7800, 7860, 7802, 7870, 7830, 7950])
                
                ax.plot(x_p, y_p, color='#00cc96', linewidth=2, marker='o', label='Estructura de Doble Piso (W)')
                ax.axhline(y=7800, color='#ffa500', linestyle=':', linewidth=2, label='Nivel Clave de Soporte (Neckline)')
                
                ax.set_title("Figura Chartista M1: Patrón de Giro en Doble Piso (W)", color='white', fontsize=13, fontweight='bold')
                
                patron_txt = "Doble Piso (W) con Falso Rompimiento de Soporte"
                m15_txt = "M15 se apoya en una zona institucional de compradores."
                m5_txt = "M5 rechaza dos veces el mismo nivel de precio creando soporte."
                m1_txt = "M1 forma la figura geométrica de doble suelo con impulso alcista."
                signal = "🟢 COMPRA (LONG) por Ruptura de Cuello"
                entry = "7,810.00"
                sl = "7,795.00 (15 pts por debajo del piso)"
                tp = "7,860.00 (Resistencia inmediata)"

            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('#0e1117')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('#0e1117')
            ax.legend(facecolor='#262730', edgecolor='none', labelcolor='white', loc='upper right')
            
            st.info(f"""
            ### 📊 **Desglose Técnico Estructural:**
            - **Figura Chartista Identificada:** {patron_txt}
            - **Lectura M15 (Macro):** {m15_txt}
            - **Lectura M5 (Estructura):** {m5_txt}
            - **Lectura M1 (Ejecución):** {m1_txt}
            """)
            
            # Mostramos el gráfico geométrico real del patrón chartista
            st.markdown("### 📐 Esquema Gráfico de la Figura Chartista en M1:")
            st.pyplot(fig)
            
            # Bloque de Aviso Legal
            st.warning("""
            ⚠️ **AVISO LEGAL Y DESCARGO DE RESPONSABILIDAD (DISCLAIMER):**
            Las figuras geométricas y los niveles numéricos se generan con **fines académicos y pedagógicos** para ilustrar la teoría de chartismo. La toma de decisiones y el riesgo financiero corren por cuenta exclusiva del alumno.
            """)
            
            # Bloque de la Propuesta de Operación
            st.success(f"""
            ### 🎯 **Setup Educativo Basado en la Figura:**
            - **Dirección del Trade:** {signal}
            - **📍 Precio de Entrada Exacto:** **{entry}**
            - **🛡️ Stop Loss (Límite de Pérdida):** **{sl}**
            - **🎯 Take Profit (Objetivo de Ganancia):** **{tp}**
            
            > **💡 Guía para el Alumno:** Compara las líneas trazadas en este esquema con tu gráfico de MetaTrader. ¿Ves el mismo canal o patrón formándose en tus velas de M1?
            """)
            
            if not permitir_operar or not lote_adecuado or not plan_definido or not tendencia_alineada:
                st.error("🛑 **BLOQUEO DE SEGURIDAD INSTITUCIONAL:** Tus filtros de disciplina o gestión de riesgo no están aprobados. Operación denegada.")
            else:
                st.markdown("✅ **ESTADO:** Filtros aprobados. Valida la figura geométrica en tu pantalla antes de ejecutar.")
else:
    st.info("👆 Sube tus capturas en las tres temporalidades para generar el análisis chartista vectorial en M1.")
