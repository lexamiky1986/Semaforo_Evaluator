import streamlit as st

# ---- Configuración de página ----
st.set_page_config(page_title="Evaluador de Viabilidad", page_icon="🚦", layout="centered")

# ---- Título ----
st.title("🚦 Evaluador de Viabilidad de Proyectos")
st.write("Esta aplicación clasifica un proyecto como **Viable**, **Por Mejorar** o **No Viable**, según criterios simples de costo, duración, recursos y riesgo.")

# ---- Entradas ----
st.header("📋 Ingrese los datos del proyecto")

costo = st.number_input("Costo estimado (USD):", min_value=0.0, step=100.0)
duracion = st.number_input("Duración estimada (meses):", min_value=0.0, step=1.0)
complejidad = st.selectbox("Complejidad del proyecto:", ["Baja", "Media", "Alta"])
recursos = st.slider("Disponibilidad de recursos (0 = muy pocos, 10 = muchos):", 0, 10, 5)
riesgo = st.slider("Nivel de riesgo (0 = bajo, 10 = alto):", 0, 10, 5)

# ---- Evaluación ----
st.header("🔍 Evaluación")

if st.button("Evaluar Proyecto"):
    score = 0

    # Criterios simples
    if costo < 10000: score += 2
    elif costo < 50000: score += 1

    if duracion < 6: score += 2
    elif duracion < 12: score += 1

    if complejidad == "Baja": score += 2
    elif complejidad == "Media": score += 1

    score += recursos / 5
    score -= riesgo / 3

    # Clasificación final
    if score >= 6:
        resultado = "🟢 Proyecto Viable"
        color = "green"
    elif 3 <= score < 6:
        resultado = "🟡 Proyecto por Mejorar"
        color = "orange"
    else:
        resultado = "🔴 Proyecto No Viable"
        color = "red"

    st.markdown(f"## Resultado: <span style='color:{color}'>{resultado}</span>", unsafe_allow_html=True)
    st.write("**Puntaje total:**", round(score, 2))
