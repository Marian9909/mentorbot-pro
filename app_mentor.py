import streamlit as st
from PIL import Image
import pandas as pd

# Configuración de la página en modo ancho (wide)
st.set_page_config(page_title="MentorBot Pro - Análisis Técnico Real", page_icon="📈", layout="wide")

st.title("📈 MentorBot Pro: Análisis Técnico y Estructural en Vivo")
st.markdown("---")

# Menú lateral para el control emocional (Mindset)
st.sidebar.header("🧠 Control Emocional (Checklist)")
st.sidebar.markdown("Antes de operar, evalúa tu disciplina:")

emocion_actual = st.sidebar.selectbox(
    "¿Cómo te sientes en este momento?",
    ["Calmo y enfocado", "Frustrado por pérdidas recientes", "Ansioso / Con ganas de recuperar rápido", "Eufórico por una buena racha"]
)

lote_adecuado = st.sidebar.checkbox("¿Mi lote respeta estrictamente la gestión de riesgo?")
plan_definido = st.sidebar.checkbox("Tengo claro mi punto de salida (Stop Loss) si el mercado se equivoca")
tendencia_alineada = st.sidebar.checkbox("He confirmado la estructura en las 3 temporalidades")

# Alerta de Mindset
if emocion_actual in ["Frustrado por pérdidas recientes", "Ansioso / Con ganas de recuperar rápido"]:
    st.sidebar.error("🚨 **ALERTA DE MINDSET:** Detectamos señales de posible operativa por venganza o ansiedad. Te sugerimos cerrar la plataforma 15 minutos.")
    permitir_operar = False
else:
    st.sidebar.success("✅ Estado mental apto para operar con disciplina.")
    permitir_operar = True

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Carga de Datos Históricos (Opcional)")
archivo_csv = st.sidebar.file_uploader("Sube tu CSV de precios (Step Index)", type=["csv"])

# Interfaz Principal: Distribución en 3 columnas para M1, M5 y M15
st.subheader("1. Sube tus 3 capturas de pantalla")
st.markdown("Carga las evidencias gráficas de tus temporalidades:")

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

# Procesamiento de datos reales si se sube el archivo CSV de precios
df_precios = None
if archivo_csv is not None:
    try:
        df_precios = pd.read_csv(archivo_csv)
        st.sidebar.success("✅ Histórico de precios cargado correctamente.")
    except Exception as e:
        st.sidebar.error(f"Error al procesar el archivo: {e}")

# Mostrar las imágenes si al menos una ha sido cargada
if img_m1 or img_m5 or img_m15:
    st.markdown("---")
    st.subheader("📸 Vista previa de tus evidencias gráficas")
    
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
    st.subheader("2. Definición de Niveles y Análisis Técnico Real")
    
    tipo_operacion = st.radio("Dirección del Trade:", ["🟢 Compra (Long)", "🔴 Venta (Short)"], horizontal=True)

    col_n1, col_n2, col_n3 = st.columns(3)
    with col_n1:
        precio_entrada = st.number_input("Precio de Entrada Real", value=7828.0000, format="%.4f")
    with col_n2:
        precio_sl = st.number_input("Stop Loss (SL) Real", value=7820.0000, format="%.4f")
    with col_n3:
        precio_tp = st.number_input("Take Profit (TP) Real", value=7845.0000, format="%.4f")

    if st.button("🚀 Ejecutar Análisis y Auditoría de Mercado", use_container_width=True):
        
        # Cálculos basados en los precios reales proporcionados
        riesgo = abs(precio_entrada - precio_sl)
        beneficio = abs(precio_tp - precio_entrada)
        rr = beneficio / riesgo if riesgo > 0 else 0
        
        st.markdown("---")
        st.markdown("### 📊 **Diagnóstico Técnico y Estructural:**")
        
        # Análisis basado en el histórico real si el usuario cargó el CSV
        if df_precios is not None and ('Close' in df_precios.columns or 'close' in df_precios.columns):
            col_c = 'Close' if 'Close' in df_precios.columns else 'close'
            ultimos_precios = df_precios[col_c].tail(20).values
            tendencia_matematica = "Alcista" if ultimos_precios[-1] > ultimos_precios[0] else "Bajista"
            st.info(f"📈 **Análisis Estadístico del CSV:** La tendencia reciente en las últimas 20 velas es **{tendencia_matematica}** (Precio actual del histórico: {ultimos_precios[-1]:,.4f}).")
        else:
            st.info("💡 **Análisis de Acción del Precio:** Evalúa la confluencia de tus temporalidades M1, M5 y M15 con los niveles ingresados.")

        m_r1, m_r2, m_r3 = st.columns(3)
        with m_r1:
            st.metric(label="Riesgo en Puntos", value=f"{riesgo:.2f}")
        with m_r2:
            st.metric(label="Beneficio en Puntos", value=f"{beneficio:.2f}")
        with m_r3:
            st.metric(label="Ratio Beneficio / Riesgo (R:R)", value=f"1 : {rr:.2f}")
            
        errores = 0
        if "Compra" in tipo_operacion:
            if precio_sl >= precio_entrada:
                st.error("❌ **Error de Lógica:** En una Compra, el Stop Loss debe estar por debajo del precio de entrada.")
                errores += 1
            if precio_tp <= precio_entrada:
                st.error("❌ **Error de Lógica:** En una Compra, el Take Profit debe estar por encima del precio de entrada.")
                errores += 1
        else:
            if precio_sl <= precio_entrada:
                st.error("❌ **Error de Lógica:** En una Venta, el Stop Loss debe estar por encima del precio de entrada.")
                errores += 1
            if precio_tp >= precio_entrada:
                st.error("❌ **Error de Lógica:** En una Venta, el Take Profit debe estar por debajo del precio de entrada.")
                errores += 1
                
        if rr < 2.0:
            st.warning(f"⚠️ **Advertencia de R:R (1:{rr:.2f}):** La academia recomienda buscar un beneficio de al menos el doble del riesgo (1:2).")
        else:
            st.success(f"✅ **Gestión Aprobada:** El ratio de 1:{rr:.2f} cumple con el estándar institucional.")
            
        if errores == 0 and rr >= 2.0 and permitir_operar and lote_adecuado and plan_definido and tendencia_alineada:
            st.success("🟢 **VEREDICTO FINAL: SETUP TÉCNICO VALIDADO Y APTO PARA EJECUTAR.**")
        else:
            st.warning("🟡 **VEREDICTO FINAL: Se detectaron observaciones en tu gestión o lógica de precios.**")
else:
    st.info("👆 Sube tus capturas en las tres temporalidades para activar la auditoría técnica y de precios.")
