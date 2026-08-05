import streamlit as st
from PIL import Image

# Configuración de la página en modo ancho (wide)
st.set_page_config(page_title="MentorBot Pro - SL y TP Automáticos", page_icon="📈", layout="wide")

st.title("📈 MentorBot Pro: Cálculo Automático de SL & TP (Step Index)")
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
    st.subheader("2. Ingreso Rápido y Proyección Automática")
    
    tipo_operacion = st.radio("Dirección del Trade:", ["🟢 Compra (Long)", "🔴 Venta (Short)"], horizontal=True)

    c_n1, c_n2 = st.columns(2)
    with c_n1:
        # Solo ingresas tu precio de entrada real (ej. 7828.00)
        precio_entrada = st.number_input("Precio de Entrada Real (Tu Línea en Deriv)", value=7828.0000, format="%.4f")
    with c_n2:
        # Distancia de riesgo en puntos que tú decides arriesgar (ej. 15 o 20 puntos)
        distancia_riesgo = st.slider("Puntos de Riesgo para el Stop Loss", min_value=5, max_value=50, value=15, step=1)

    if st.button("🚀 Calcular Niveles Óptimos y Auditar Riesgo", use_container_width=True):
        
        # La página calcula automáticamente el SL y el TP basados en un ratio de 1:2 (Beneficio doble al riesgo)
        ratio_beneficio = 2.0 
        distancia_ganancia = distancia_riesgo * ratio_beneficio
        
        if "Compra" in tipo_operacion:
            precio_sl = precio_entrada - distancia_riesgo
            precio_tp = precio_entrada + distancia_ganancia
        else:
            precio_sl = precio_entrada + distancia_riesgo
            precio_tp = precio_entrada - distancia_ganancia
            
        st.markdown("---")
        st.markdown("### 📊 **Proyección Automática de la Página:**")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Stop Loss Automático (SL)", value=f"{precio_sl:.4f}")
        with m2:
            st.metric(label="Take Profit Automático (TP)", value=f"{precio_tp:.4f}")
        with m3:
            st.metric(label="Ratio Beneficio / Riesgo", value=f"1 : {ratio_beneficio}")
            
        st.success(f"""
        ### 🎯 **Resumen de la Orden para tu Broker:**
        - **Dirección:** {tipo_operacion}
        - **Entrada Registrada:** `{precio_entrada:.4f}`
        - **Stop Loss Sugerido:** `{precio_sl:.4f}` ({distancia_riesgo} puntos de riesgo)
        - **Take Profit Sugerido:** `{precio_tp:.4f}` ({distancia_ganancia} puntos de beneficio)
        """)

        if apto_operar:
            st.balloons()
            st.success("🟢 **VEREDICTO FINAL: NIVELES CALCULADOS Y VALIDADOS. LISTO PARA OPERAR.**")
        else:
            st.warning("🟡 **VEREDICTO FINAL: Revisa tus filtros de disciplina antes de colocar la orden.**")
else:
    st.info("👆 Sube tus capturas en las tres temporalidades para habilitar el generador automático de niveles.")
