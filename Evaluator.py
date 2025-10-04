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
        nuevo = pd.DataFrame([[q1, q2, q3, q4]], columns=X = df[["Q1 - Courtesy", "Q2 - Technical", "Q3 - Timeliness", "Q4 - Quality"]])
        df = pd.read_csv("dataset_satisfaccion.csv")
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_csv("dataset_satisfaccion.csv", index=False)
        st.success("Encuesta enviada correctamente ✅")

elif menu == "Reentrenar Modelo":
    elif menu == "Reentrenar Modelo":
    st.header("⚙️ Reentrenar modelo de IA")

    try:
        df = pd.read_csv("dataset_satisfaccion.csv")

        # Crear columna objetivo si no existe
        if "Etiqueta" not in df.columns:
            def clasificar_viabilidad(valor):
                if valor >= 4:
                    return "Viable"
                elif valor >= 3:
                    return "Por mejorar"
                else:
                    return "No viable"
            df["Etiqueta"] = df["Q5 - Overall"].apply(clasificar_viabilidad)

        # Asegurar columnas numéricas
        columnas = ["Q1 - Courtesy", "Q2 - Technical", "Q3 - Timeliness", "Q4 - Quality"]
        for c in columnas:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        df = df.dropna(subset=columnas)

        # Definir variables X e y
        X = df[columnas]
        y = df["Etiqueta"]

        from sklearn.model_selection import train_test_split
        from sklearn.neural_network import MLPClassifier
        from sklearn.preprocessing import LabelEncoder
        from sklearn.metrics import accuracy_score

        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

        modelo = MLPClassifier(hidden_layer_sizes=(8, 8), max_iter=1000, random_state=42)
        modelo.fit(X_train, y_train)

        y_pred = modelo.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        st.success(f"✅ Modelo reentrenado correctamente")
        st.info(f"Precisión del modelo: {acc:.2f}")

    except Exception as e:
        st.error(f"Error al reentrenar el modelo: {e}")
