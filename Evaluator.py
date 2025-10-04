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

    # --- 1️⃣ Selección de metadatos ---
    st.subheader("Datos del solicitante")

    dept_options = [
        "PMO", "Information Security", "Technical Account Management", "Business Development",
        "Client Operations", "Business Continuity", "Networking", "Change Management",
        "Facilities", "Goods Strategy", "Human Resources", "Privacy", "Legal",
        "Systems", "Desktop Support", "User Admin", "Software Development"
    ]

    work_item_options = [
        "RFPs & Questionnaires",
        "Policy Controls",
        "Process Automation"
    ]

    departamento = st.selectbox("Área solicitante (Requesting Dept):", dept_options)
    tipo_servicio = st.selectbox("Tipo de servicio (Work Item Type):", work_item_options)

    # --- 2️⃣ Encuesta de satisfacción ---
    st.subheader("Calificación del servicio recibido (1 = Muy bajo, 5 = Excelente)")
    q1 = st.slider("Tiempo de respuesta", 1, 5, 3)
    q2 = st.slider("Calidad del servicio", 1, 5, 3)
    q3 = st.slider("Disponibilidad del técnico", 1, 5, 3)
    q4 = st.slider("Claridad de la comunicación", 1, 5, 3)

    # --- 3️⃣ Cálculo automático del promedio (Q5 - Overall) ---
    q5_overall = round((q1 + q2 + q3 + q4) / 4, 2)
    st.info(f"Puntuación global calculada automáticamente: **{q5_overall}**")

    # --- 4️⃣ Guardar encuesta ---
    if st.button("Enviar encuesta"):
        import os

        csv_path = "dataset_satisfaccion.csv"
        # Si el dataset no existe, se crea uno nuevo con todas las columnas
        if not os.path.exists(csv_path):
            st.warning("No se encontró el dataset. Se creará uno nuevo.")
            df = pd.DataFrame(columns=[
                "Requesting Dept", "Work Item Type",
                "Q1 - Courtesy", "Q2 - Technical", "Q3 - Timeliness", "Q4 - Quality",
                "Q5 - Overall"
            ])
        else:
            df = pd.read_csv(csv_path)

        # Crear la nueva fila con la información ingresada
        nueva_fila = pd.DataFrame([{
            "Requesting Dept": departamento,
            "Work Item Type": tipo_servicio,
            "Q1 - Courtesy": q1,
            "Q2 - Technical": q2,
            "Q3 - Timeliness": q3,
            "Q4 - Quality": q4,
            "Q5 - Overall": q5_overall
        }])

        # Agregar la nueva encuesta al dataset
        df = pd.concat([df, nueva_fila], ignore_index=True)
        df.to_csv(csv_path, index=False)

        st.success("✅ Encuesta enviada correctamente y guardada en el dataset.")
        st.balloons()
    
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
