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

    # 1️⃣ Ingreso de valores del usuario
    q1 = st.slider("Tiempo de respuesta", 1, 5, 3)
    q2 = st.slider("Calidad del servicio", 1, 5, 3)
    q3 = st.slider("Disponibilidad del técnico", 1, 5, 3)
    q4 = st.slider("Claridad de la comunicación", 1, 5, 3)

    # 2️⃣ Al presionar Enviar
    if st.button("Enviar"):
        import os

        # Asegurarse de que el archivo base exista
        csv_path = "dataset_satisfaccion.csv"
        if not os.path.exists(csv_path):
            st.warning("No se encontró el dataset. Se creará uno nuevo.")
            df = pd.DataFrame(columns=["Q1 - Courtesy", "Q2 - Technical", "Q3 - Timeliness", "Q4 - Quality", "Q5 - Overall"])
        else:
            df = pd.read_csv(csv_path)

        # 3️⃣ Crear el nuevo registro
        nuevo = pd.DataFrame(
            [[q1, q2, q3, q4, None]],
            columns=["Q1 - Courtesy", "Q2 - Technical", "Q3 - Timeliness", "Q4 - Quality", "Q5 - Overall"]
        )

        # 4️⃣ Unir al dataset existente
        df = pd.concat([df, nuevo], ignore_index=True)

        # 5️⃣ Guardar los cambios
        df.to_csv(csv_path, index=False)

        st.success("✅ Encuesta enviada correctamente y guardada en el dataset.")

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
