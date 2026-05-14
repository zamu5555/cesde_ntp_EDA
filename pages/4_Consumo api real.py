import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(layout="wide")

st.title("📚 Dashboard Biblioteca")

API_URL = "http://localhost:8080"

endpoint = st.sidebar.selectbox(
    "Selecciona endpoint",
    [
        "libros",
        "usuarios",
        "reservas",
        "editoriales",
        "renovaciones",
        "reserva-libro"
    ]
)

url = f"{API_URL}/{endpoint}"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    df = pd.DataFrame(data)

    if "editorial" in df.columns:

        df["editorial"] = df["editorial"].apply(
            lambda x: x.get("nombreEditorial")
            if isinstance(x, dict)
            else x
        )

    st.subheader(f"Datos de {endpoint}")

    st.dataframe(df, use_container_width=True)

    columnas = df.columns.tolist()

    columna = st.selectbox(
        "Selecciona columna para analizar",
        columnas
    )

    conteo = (
        df[columna]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    conteo.columns = [columna, "cantidad"]

    fig = px.bar(
        conteo,
        x=columna,
        y="cantidad",
        title=f"Análisis de {columna}",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

else:

    st.error("No se pudo conectar con la API")