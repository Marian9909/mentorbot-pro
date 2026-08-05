import streamlit as st
from PIL import Image

# Configuración de la página en modo ancho (wide)
st.set_page_config(page_title="MentorBot Pro - Análisis de Dirección", page_icon="📈", layout="wide")

st.title("📈 MentorBot Pro: Análisis de Dirección & Niveles Automáticos")
st.markdown("---")

# Menú lateral: Control Emocional (Mindset)
st.sidebar.header("🧠 Control Emocional (Mindset)")
emocion = st.sidebar.selectbox(
    "¿Cómo te sientes?",
    ["Calmo y enfocado", "Frustrado", "Ansioso", "Eufórico"]
)

lote_adecuado = st.sidebar.checkbox("¿Mi lote respeta estrictamente la gestión de riesgo?")
plan_definido = st.sidebar.checkbox("Tengo claro mi plan de salida si el mercado se equivoca")
tendencia_alineada = st.sidebar.checkbox("He confirmado la estructura en las 3 temporalidades")

if emocion != "Calmo y enfocado" or not lote_adecuado or not plan_definido or not tendencia_alineada:
    st.sidebar.warning("⚠️ **Bloqueo de Mindset:** Revisa tus filtros de disciplina antes de operar.")
    apto_operar = False
else:
    st.sidebar.success("✅ Estado y disciplina óptimos.")
    apto_operar = True

# Interfaz Principal: Carga de Capturas
st.subheader("1. Sube tus capturas de pantalla (M1, M5, M15)")
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

# Mostrar vistas previas si hay imágenes
if img_m1 or img_m5 or img_m15:
    st.markdown("---")
    st.subheader("📸 Evidencias Gráficas Sincronizadas")
    p1, p2, p3 = st.columns(3)
    with p1:
        if img_m1: st.image(img_m1, caption="Gráfico M1", use_container_width=True)
    with p2:
        if img_m5: st.image(img_m5, caption="Gráfico M5", use_container_width=True)
    with p3:
        if img_m15: st.image(img_m15, caption="Gráfico M15", use_container_width=True)

    st.markdown("---")
    st.subheader("2. Definición del Análisis de Mercado")
    
    # Selector para que la página te diga y defina el análisis operativo
    direccion_sugerida = st.selectbox(
        "¿Qué dirección arroja tu lectura estructural en las 3 temporalidades?",
        ["🟢 COMPRA (Long) - Rebote en Soporte / Tendencia Alcista", "🔴 VENTA (Short) - Rechazo en Resistencia / Tendencia Bajista"]
    )

    c_n1, c_n2 = st.columns(2)
    with c_n1:
        precio_entrada = st.number_input("Precio de Entrada Real (Tu Línea en Deriv)", value=7828.0000, format="%.4f")
    with c_n2:
        distancia_riesgo = st.slider("Puntos de Riesgo para el Stop Loss", min_value=5, max_value=50, value=15, step=1)

    if st.button("🚀 Ejecutar Diagnóstico y Generar Niveles", use_container_width=True):
        
        ratio_beneficio = 2.0 # Relación 1:2
        distancia_ganancia = distancia_riesgo * ratio_beneficio
        
        if "COMPRA" in direccion_sugerida:
            tipo_trade_label = "🟢 COMPRA (LONG)"
            precio_sl = precio_entrada - distancia_riesgo
            precio_tp = precio_entrada + distancia_ganancia
        else:
            tipo_trade_label = "🔴 VENTA (SHORT)"
            precio_sl = precio_entrada + distancia_riesgo
            precio_tp = precio_entrada - distancia_ganancia
            
        st.markdown("---")
        st.markdown(f"### 📊 **Diagnóstico del Analizador:**")
        
        st.success(f"### **Operación Determinada por la Estructura: {tipo_trade_label}**")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Stop Loss Automático (SL)", value=f"{precio_sl:.4f}")
        with m2:
            st.metric(label="Take Profit Automático (TP)", value=f"{precio_tp:.4f}")
        with m3:
            st.metric(label="Ratio Beneficio / Riesgo", value=f"1 : {ratio_beneficio}")
            
        st.info(f"""
        ### 🎯 **Estrategia Ejecutable:**
        - **Activo:** Step Index
        - **Dirección Oficial:** {tipo_trade_label}
        - **Precio de Entrada:** `{precio_entrada:.4f}`
        - **Protección (SL):** `{precio_sl:.4f}`
        - **Objetivo (TP):** `{precio_tp:.4f}`
        """)

        if apto_operar:
            st.balloons()
            st.success("🟢 **VEREDICTO FINAL: ANÁLISIS CONFIRMADO. EJECUTA CON DISCIPLINA.**")
        else:
            st.warning("🟡 **VEREDICTO FINAL: Revisa tus filtros de disciplina antes de colocar la orden.**")
else:
    st.info("👆 Sube tus capturas en las tres temporalidades para activar el analizador de dirección.")
