import streamlit as st
import pandas as pd
import requests

# Configuración de la página
st.set_page_config(page_title="Gestión Corporativa Colombia - MockAPI", layout="wide")

st.title("🏢 Gestión Corporativa: Usuarios y Reservas de Libros")
st.markdown("""
### Objetivo
En esta sección, consumiremos **dos entidades** personalizadas creadas en **MockAPI**.
Los datos incluyen información sobre **usuarios** y **reservas de libros** del proyecto integrador.
""")

# --- Configuración de la API ---
MOCK_API_ID = "69d7adf69c5ebb0918c82d05"
MOCK_API_BASE_URL = f"https://{"69d7adf69c5ebb0918c82d05"}.mockapi.io"

# --- Botón para Limpiar Caché ---
if st.button("🔄 Refrescar Datos (Limpiar Caché)"):
    st.cache_data.clear()
    st.rerun()

# --- Función para obtener datos de MockAPI ---
@st.cache_data
def get_mockapi_data(entity):
    paths_to_try = [
        f"{MOCK_API_BASE_URL}/{entity}",
        f"{MOCK_API_BASE_URL}/api/v1/{entity}"
    ]
    last_error = ""
    for url in paths_to_try:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return pd.DataFrame(data)
                else:
                    return pd.DataFrame([data])
            else:
                last_error = f"Status {response.status_code} en {url}"
        except Exception as e:
            last_error = f"Error: {e} en {url}"

    st.error(f"No se pudo conectar con '{entity}'. Último intento: {last_error}")
    return pd.DataFrame()

# --- Carga de Datos ---
with st.spinner("Conectando con MockAPI..."):
    df_users = get_mockapi_data("Users")
    df_reservas = get_mockapi_data("ReservaLibro")

# ============================================================
# SECCIÓN 1: USUARIOS
# ============================================================
st.header("👥 Usuarios")
st.markdown("Consulta y filtro del listado de usuarios registrados.")

if not df_users.empty:
    col1, col2 = st.columns(2)

    with col1:
        # Filtro por nombre (búsqueda de texto)
        search_nombre = st.text_input("🔍 Buscar por Nombre:", "", key="search_nombre")

    with col2:
        # Filtro por documento
        documentos = ["Todos"] + sorted(df_users['documento'].dropna().unique().tolist())
        sel_documento = st.selectbox("Filtrar por Documento:", documentos, key="sel_documento")

    # Aplicar filtros
    df_users_filtrado = df_users.copy()
    if search_nombre:
        df_users_filtrado = df_users_filtrado[
            df_users_filtrado['nombre'].str.contains(search_nombre, case=False, na=False)
        ]
    if sel_documento != "Todos":
        df_users_filtrado = df_users_filtrado[
            df_users_filtrado['documento'] == sel_documento
        ]

    # Métricas
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Usuarios", len(df_users))
    with m2:
        st.metric("Usuarios Filtrados", len(df_users_filtrado))
    with m3:
        st.metric("Campos por Usuario", len(df_users.columns))

    # Mostrar columnas relevantes
    cols_mostrar = [c for c in ['UsuarioId', 'nombre', 'documento', 'telefono', 'correo'] if c in df_users_filtrado.columns]
    st.dataframe(df_users_filtrado[cols_mostrar], use_container_width=True)

else:
    st.info("💡 No se encontraron datos de 'Users'. Verifica la API.")

st.divider()

# ============================================================
# SECCIÓN 2: RESERVAS DE LIBROS
# ============================================================
st.header("📚 Reservas de Libros")
st.markdown("Consulta y filtro de las reservas de libros registradas.")

if not df_reservas.empty:
    col3, col4 = st.columns(2)

    with col3:
        # Filtro por nombre del libro
        search_libro = st.text_input("🔍 Buscar por Libro:", "", key="search_libro")

    with col4:
        # Filtro por cantidad (rango)
        if 'cantidad' in df_reservas.columns:
            cantidades = pd.to_numeric(df_reservas['cantidad'], errors='coerce').dropna()
            if not cantidades.empty:
                min_cant = int(cantidades.min())
                max_cant = int(cantidades.max())
                rango_cantidad = st.slider(
                    "Filtrar por Cantidad:",
                    min_value=min_cant,
                    max_value=max_cant,
                    value=(min_cant, max_cant),
                    key="rango_cantidad"
                )

    # Aplicar filtros
    df_reservas_filtrado = df_reservas.copy()

    if search_libro and 'libro' in df_reservas_filtrado.columns:
        df_reservas_filtrado = df_reservas_filtrado[
            df_reservas_filtrado['libro'].str.contains(search_libro, case=False, na=False)
        ]

    if 'cantidad' in df_reservas_filtrado.columns and not cantidades.empty:
        df_reservas_filtrado['cantidad_num'] = pd.to_numeric(df_reservas_filtrado['cantidad'], errors='coerce')
        df_reservas_filtrado = df_reservas_filtrado[
            (df_reservas_filtrado['cantidad_num'] >= rango_cantidad[0]) &
            (df_reservas_filtrado['cantidad_num'] <= rango_cantidad[1])
        ]

    # Métricas
    mr1, mr2, mr3 = st.columns(3)
    with mr1:
        st.metric("Total Reservas", len(df_reservas))
    with mr2:
        st.metric("Reservas Filtradas", len(df_reservas_filtrado))
    with mr3:
        total_libros = pd.to_numeric(df_reservas_filtrado.get('cantidad', pd.Series()), errors='coerce').sum()
        st.metric("Total Libros Reservados", f"{int(total_libros):,}")

    # Mostrar columnas relevantes
    cols_reservas = [c for c in ['ReservaId', 'libro', 'cantidad', 'libroId'] if c in df_reservas_filtrado.columns]
    st.dataframe(df_reservas_filtrado[cols_reservas], use_container_width=True)

else:
    st.info("💡 No se encontraron datos de 'ReservaLibro'. Verifica la API.")

# --- Información Técnica ---
st.divider()
st.info(f"""
**Detalles de la API (MockAPI):**
- **Base URL:** `{MOCK_API_BASE_URL}`
- **Entidades:** `/Users` y `/ReservaLibro`
- **Nota:** Los nombres de los recursos son sensibles a mayúsculas. Usa exactamente `Users` y `ReservaLibro`.
""")