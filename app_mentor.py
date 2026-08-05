import streamlit as st
from PIL import Image

# Configuración de la página en modo ancho (wide)
st.set_page_config(page_title="MentorBot Pro - Auditoría Real", page_icon="📈", layout="wide")

st.title("📈 MentorBot Pro: Auditoría Técnica y Gestión de Riesgo (Step Index)")
st.markdown("---")

# Menú lateral: Control Emocional (Mindset)
st.sidebar.header("🧠 Control Emocional (Mindset)")
emocion = st.sidebar.selectbox(
    "¿Cómo te sientes?",
    ["Calmo y enfocado", "Frustrado", "Ansioso", "Eufórico"]
)

lote_adecuado = st.sidebar.checkbox("¿Mi lote respeta estrictamente la gestión de riesgo?")
plan_definido = st.sidebar.checkbox("Tengo claro mi punto de salida (Stop Loss) si el mercado se equivoca")
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
    st.subheader("2. Calibración de Niveles en Vivo (Basado en tu pantalla de Deriv)")
    
    tipo_operacion = st.radio("Dirección del Trade:", ["🟢 Compra (Long)", "🔴 Venta (Short)"], horizontal=True)

    c_n1, c_n2, c_n3 = st.columns(3)
    with c_n1:
        # Precio actual que el usuario ve en su gráfica (ej. 7828.00)
        precio_entrada = st.number_input("Precio de Entrada Real (Línea Azul)", value=7828.0000, format="%.4f")
    with c_n2:
        precio_sl = st.number_input("Stop Loss (SL) Exacto", value=7820.0000, format="%.4f")
    with c_n3:
        precio_tp = st.number_input("Take Profit (TP) Exacto", value=7845.0000, format="%.4f")

    if st.button("🚀 Ejecutar Auditoría Estructural y de Riesgo", use_container_width=True):
        
        # Cálculos matemáticos exactos sin inventar nada
        riesgo = abs(precio_entrada - precio_sl)
        beneficio = abs(precio_tp - precio_entrada)
        rr = beneficio / riesgo if riesgo > 0 else 0
        
        st.markdown("---")
        st.markdown("### 📊 **Resultado de la Auditoría Técnica:**")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Riesgo en Puntos", value=f"{riesgo:.2f}")
        with m2:
            st.metric(label="Beneficio en Puntos", value=f"{beneficio:.2f}")
        with m3:
            st.metric(label="Ratio Beneficio / Riesgo (R:R)", value=f"1 : {rr:.2f}")
            
        # Validaciones de lógica de mercado
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
            st.warning(f"⚠️ **Advertencia de Gestión (1:{rr:.2f}):** La academia sugiere buscar un objetivo de beneficio de al menos el doble del riesgo.")
        else:
            st.success(f"✅ **Gestión Excelente:** El ratio de 1:{rr:.2f} cumple perfectamente con el plan institucional.")

        if errores == 0 and rr >= 2.0 and apto_operar:
            st.balloons()
            st.success("🟢 **VEREDICTO FINAL: SETUP VALIDADO. LISTO PARA EJECUTAR CON DISCIPLINA.**")
        else:
            st.warning("🟡 **VEREDICTO FINAL: Revisa los parámetros o la disciplina antes de abrir la operación.**")
else:
    st.info("👆 Sube tus capturas en las tres temporalidades para habilitar los campos de calibración de precios.")
