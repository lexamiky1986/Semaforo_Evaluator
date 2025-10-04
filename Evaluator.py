import streamlit as st
import pandas as pd
import joblib
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt

st.title("Lean Six Sigma Satisfaction Analyzer 🧠📊")

menu = st.sidebar.selectbox("Selecciona una opción:", 
                            ["Dashboard", "Realizar Encuesta", "Reentrenar Modelo"])

if menu == "Dashboard":
    st.header("📈 Análisis de Satisfacción")
    df = pd.read_csv("dataset_satisfaccion.csv")
    st.dataframe(df.head())
    st.bar_chart(df["Q5 - Overall"])
    
elif menu == "Realizar Encuesta":
    st.header("📝 Nueva Encuesta de Satisfacción")
    q1 = st.slider("Tiempo de respuesta", 1, 5, 3)
    q2 = st.slider("Calidad del servicio", 1, 5, 3)
    q3 = st.slider("Disponibilidad del técnico", 1, 5, 3)
    q4 = st.slider("Claridad de la comunicación", 1, 5, 3)

    if st.button("Enviar"):
        nuevo = pd.DataFrame([[q1, q2, q3, q4]], columns=["Q1", "Q2", "Q3", "Q4"])
        df = pd.read_csv("dataset_satisfaccion.csv")
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_csv("dataset_satisfaccion.csv", index=False)
        st.success("Encuesta enviada correctamente ✅")

elif menu == "Reentrenar Modelo":
    st.header("⚙️ Reentrenar modelo de IA")
    df = pd.read_csv("dataset_satisfaccion.csv")
    X = df[["Q1", "Q2", "Q3", "Q4"]]
    y = df["Etiqueta"]
    model = MLPClassifier(hidden_layer_sizes=(8, 8), max_iter=1000)
    model.fit(X, y)
    joblib.dump(model, "modelo_mlp.pkl")
    st.success("Modelo reentrenado exitosamente 🧠💾")
