import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(layout="wide")

st.title("Dashboard Biblioteca")

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

response = requests.get(
    f"{API_URL}/{endpoint}"
)

reservas_response = requests.get(
    f"{API_URL}/reservas"
)

usuarios_response = requests.get(
    f"{API_URL}/usuarios"
)

libros_response = requests.get(
    f"{API_URL}/libros"
)

if (
    response.status_code == 200
    and reservas_response.status_code == 200
    and usuarios_response.status_code == 200
    and libros_response.status_code == 200
):

    data = response.json()

    df = pd.DataFrame(data)

    reservas = pd.DataFrame(
        reservas_response.json()
    )

    usuarios = pd.DataFrame(
        usuarios_response.json()
    )

    libros = pd.DataFrame(
        libros_response.json()
    )

    if "editorial" in df.columns:

        df["editorial"] = (
            df["editorial"]
            .apply(
                lambda x:
                x.get("nombreEditorial")
                if isinstance(x, dict)
                else x
            )
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Usuarios",
            len(usuarios)
        )

    with col2:

        st.metric(
            "Reservas",
            len(reservas)
        )

    with col3:

        st.metric(
            "Libros",
            len(libros)
        )

    st.divider()

    columnas = [
        col for col in df.columns
        if "id" not in col.lower()
    ]

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

    conteo.columns = [
        columna,
        "cantidad"
    ]

    fig = px.bar(
        conteo,
        x=columna,
        y="cantidad",
        title=f"Análisis de {columna}",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if "usuario" in reservas.columns:

        reservas["usuarioNombre"] = (
            reservas["usuario"]
            .apply(
                lambda x:
                x.get("nombre")
                if isinstance(x, dict)
                else "Sin nombre"
            )
        )

        reservas_usuario = (
            reservas["usuarioNombre"]
            .value_counts()
            .reset_index()
        )

        reservas_usuario.columns = [
            "usuario",
            "cantidad"
        ]

        st.subheader(
            "Reservas por usuario"
        )

        fig_usuario = px.bar(
            reservas_usuario,
            x="usuario",
            y="cantidad",
            text_auto=True,
            title="Cantidad de reservas por usuario"
        )

        st.plotly_chart(
            fig_usuario,
            use_container_width=True
        )

        top_usuarios = (
            reservas_usuario
            .sort_values(
                by="cantidad",
                ascending=False
            )
            .head(5)
        )

        st.subheader(
            "Top usuarios"
        )

        fig_top = px.pie(
            top_usuarios,
            names="usuario",
            values="cantidad",
            title="Top 5 usuarios con más reservas"
        )

        st.plotly_chart(
            fig_top,
            use_container_width=True
        )

    if "fechaReserva" in reservas.columns:

        st.subheader(
            "Reservas por fecha"
        )

        reservas["fechaReserva"] = (
            pd.to_datetime(
                reservas["fechaReserva"],
                errors="coerce"
            )
        )

        reservas_fecha = (
            reservas.groupby(
                reservas["fechaReserva"]
                .dt.date
            )
            .size()
            .reset_index(
                name="cantidad"
            )
        )

        fig_fecha = px.line(
            reservas_fecha,
            x="fechaReserva",
            y="cantidad",
            markers=True,
            title="Evolución de reservas"
        )

        st.plotly_chart(
            fig_fecha,
            use_container_width=True
        )

    if "estado" in reservas.columns:

        st.subheader(
            "Estado de reservas"
        )

        estados = (
            reservas["estado"]
            .astype(str)
            .value_counts()
            .reset_index()
        )

        estados.columns = [
            "estado",
            "cantidad"
        ]

        fig_estado = px.bar(
            estados,
            x="estado",
            y="cantidad",
            color="estado",
            text_auto=True,
            title="Distribución de estados"
        )

        st.plotly_chart(
            fig_estado,
            use_container_width=True
        )

    columnas_numericas = [
        col for col in df.select_dtypes(
            include=[
                "int64",
                "float64"
            ]
        ).columns
        if "id" not in col.lower()
    ]

    if len(columnas_numericas) > 0:

        st.subheader(
            "Distribución numérica"
        )

        numero_col = st.selectbox(
            "Selecciona columna numérica",
            columnas_numericas
        )

        fig_hist = px.histogram(
            df,
            x=numero_col,
            nbins=10,
            title=f"Distribución de {numero_col}"
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    st.subheader(
        "Usuarios vs reservas"
    )

    resumen = pd.DataFrame(
        {
            "tipo": [
                "Usuarios",
                "Reservas"
            ],
            "cantidad": [
                len(usuarios),
                len(reservas)
            ]
        }
    )

    fig_comparacion = px.bar(
        resumen,
        x="tipo",
        y="cantidad",
        text_auto=True,
        title="Comparación general"
    )

    st.plotly_chart(
        fig_comparacion,
        use_container_width=True
    )

else:

    st.error(
        "No se pudo conectar con la API"
    )