import streamlit as st

# Configuración de la página en modo ancho (wide)
st.set_page_config(page_title="MentorBot Pro - Analista Multiactivo", page_icon="📊", layout="wide")

st.title("📊 MentorBot Pro: Motor de Análisis Técnico Multiactivo")
st.markdown("---")

# Panel lateral: Selector de Activo y Configuración
st.sidebar.header("⚙️ Configuración del Analista")
activo = st.sidebar.selectbox(
    "Selecciona el Activo", 
    ["Step Index", "Oro (XAUUSD)", "Bitcoin (BTC)"]
)
temporalidad = st.sidebar.selectbox("Temporalidad Principal", ["M1 (Micro)", "M5 (Estructura)", "M15 (Macro)"])

st.sidebar.markdown("---")
st.sidebar.header("🧠 Control Emocional")
emocion = st.sidebar.selectbox("Estado mental:", ["Calmo y enfocado", "Frustrado", "Ansioso"])

# Valores predeterminados inteligentes según el activo seleccionado
if activo == "Step Index":
    default_precio = 7828.0000
    default_riesgo = 15.0
    formato_precio = "%.4f"
elif activo == "Oro (XAUUSD)":
    default_precio = 2350.50
    default_riesgo = 5.0
    formato_precio = "%.2f"
else:  # Bitcoin
    default_precio = 64500.00
    default_riesgo = 300.0
    formato_precio = "%.2f"

# Interfaz Principal del Analista
st.subheader(f"1. Inserción de Datos para el Análisis: {activo}")
col1, col2 = st.columns(2)

with col1:
    direccion_tesis = st.selectbox("Dirección Propuesta en tu Análisis:", ["🟢 COMPRA (Long)", "🔴 VENTA (Short)"])
    precio_entrada = st.number_input(f"Precio de Entrada Actual ({activo})", value=default_precio, format=formato_precio)

with col2:
    contexto_mercado = st.selectbox(
        "Comportamiento actual del precio en la gráfica:",
        [
            "Impulso alcista fuerte (Rompiendo máximos)",
            "Retroceso controlado hacia zona de soporte",
            "Tendencia bajista con mínimos decrecientes",
            "Rango o consolidación lateral"
        ]
    )
    distancia_sl_puntos = st.number_input(f"Riesgo estimado en puntos/dólares para el Stop Loss", value=default_riesgo)

# Botón para que el Analista emita su informe
if st.button(f"📈 Generar Informe Técnico para {activo}", use_container_width=True):
    
    st.markdown("---")
    st.subheader(f"📑 Informe Técnico del Analista: {activo}")
    
    # Lógica analítica del script para evaluar congruencia técnica
    alerta_contra_tendencia = False
    
    if "alcista" in contexto_mercado.lower() and "VENTA" in direccion_tesis:
        alerta_contra_tendencia = True
    elif "bajista" in contexto_mercado.lower() and "COMPRA" in direccion_tesis:
        alerta_contra_tendencia = True

    # Cálculos matemáticos del analista (Ratio 1:2 institucional)
    ratio_rr = 2.0
    distancia_tp_puntos = distancia_sl_puntos * ratio_rr
    
    if "COMPRA" in direccion_tesis:
        sl = precio_entrada - distancia_sl_puntos
        tp = precio_entrada + distancia_tp_puntos
    else:
        sl = precio_entrada + distancia_sl_puntos
        tp = precio_entrada - distancia_tp_puntos

    # Desglose del análisis técnico
    col_inf1, col_inf2 = st.columns(2)
    
    with col_inf1:
        st.markdown(f"**Análisis de Estructura ({temporalidad}):**")
        if "alcista" in contexto_mercado.lower():
            st.write(f"• El {activo} presenta secuencia de máximos y mínimos crecientes.")
            st.write("• Flujo de órdenes institucional orientado a la demanda.")
        elif "bajista" in contexto_mercado.lower():
            st.write(f"• El {activo} presenta secuencia de mínimos decrecientes.")
            st.write("• Flujo de órdenes institucional orientado a la oferta.")
        else:
            st.write(f"• El {activo} se encuentra en compresión o rango operativo.")
            st.write("• Riesgo de falsas rupturas elevado en zonas intermedias.")

    with col_inf2:
        st.markdown("**Evaluación de la Tesis:**")
        if alerta_contra_tendencia:
            st.error("⚠️ **ADVERTENCIA TÉCNICA:** Tu propuesta va en contra del comportamiento actual del precio descrito en el contexto del mercado.")
        else:
            st.success("✅ **CONGRUENCIA TÉCNICA:** La dirección seleccionada está respaldada por el comportamiento del precio.")

    st.markdown("---")
    st.markdown(f"### 🎯 Niveles Operativos Calculados para {activo}:")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Entrada", f"{precio_entrada:{formato_precio}}")
    with m2:
        st.metric("Stop Loss (SL)", f"{sl:{formato_precio}}")
    with m3:
        st.metric("Take Profit (TP)", f"{tp:{formato_precio}}")
    with m4:
        st.metric("Ratio R:R", f"1 : {ratio_rr}")

    st.info(f"""
    **Conclusión del Analista para {activo}:** 
    Para que esta operación en **{direccion_tesis}** mantenga validez técnica, el precio no debe invalidar la zona de control estructural ubicada en `{sl:{formato_precio}}`. El objetivo proyectado se establece en `{tp:{formato_precio}}` buscando el desequilibrio operativo.
    """)
