import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Proyecto Integrador - Analítica de Datos",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilo Personalizado (Opcional) ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Título Principal ---
st.title("🚀 Proyecto Integrador: Analítica de Datos")
st.subheader("Analitica de casos sobre el dengue")

st.divider()

# --- 1. Introducción ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📖 Introducción")
    st.write("""
    El dengue es una enfermedad que afecta de manera significativa al departamento de Antioquia. Para comprender mejor su comportamiento, es fundamental analizar los datos disponibles.

    En este proyecto se realiza el análisis de una tabla de datos sobre casos de dengue, con el objetivo de identificar patrones, tendencias y posibles factores asociados. Esto permite obtener información útil para apoyar la toma de decisiones en la prevención y control de la enfermedad.
    """)

with col2:
    st.info("💡 **Dato Curioso:** El 80% del trabajo de un analista de datos se dedica a la limpieza y preparación de la información.")

# --- 2. Objetivos ---
st.header("🎯 Objetivos del Proyecto")

obj_gen, obj_esp = st.columns(2)

with obj_gen:
    st.subheader("Objetivo General")
    st.markdown("""
    - Analizar los datos de una tabla sobre casos de dengue en Antioquia para identificar patrones, tendencias y factores relevantes que contribuyan a la comprensión y control de la enfermedad.
    """)

with obj_esp:
    st.subheader("Objetivos Específicos")
    st.markdown("""
    - Examinar la estructura y calidad de la tabla de datos de dengue.
    - Identificar la distribución de casos según variables como tiempo, ubicación u otros factores disponibles.
    - Analizar tendencias y variaciones en los casos de dengue.
    - Presentar los resultados mediante gráficos o herramientas visuales para facilitar su interpretación
    """)

st.divider()

# --- 3. Equipo de Trabajo ---
st.header("👥 Equipo de Trabajo (Integrantes)")

# Puedes ajustar los nombres aquí
integrantes = [
    {"nombre": "Samuel Diaz Vanegas", "rol": "Analista de Datos", "emoji": "👨‍💻"},
    {"nombre": "Santiago Bohorquez Saldaña", "rol": "Ingeniero de Datos", "emoji": "👩‍🔬"},
    {"nombre": "Jhonatan Tabares Jaramillo", "rol": "Arquitecto de Soluciones", "emoji": "👨‍💼"},
    {"nombre": "Mayra Alejandra Alzate Sanchez", "rol": "Arquitecto de Soluciones", "emoji": "👨‍💼"},
]

cols = st.columns(len(integrantes))

for i, persona in enumerate(integrantes):
    with cols[i]:
        st.markdown(f"""
        ### {persona['emoji']} {persona['nombre']}
        **Roles:** {persona['rol']}
        """)

st.divider()

# --- 4. Tecnologías Utilizadas ---
st.header("🛠️ Tecnologías")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("### 🐍 Python")
    st.write("Lenguaje base para el procesamiento y lógica del proyecto.")

with tech_col2:
    st.markdown("### 🐼 Pandas")
    st.write("Librería líder para manipulación y análisis de estructuras de datos.")

with tech_col3:
    st.markdown("### 🎈 Streamlit")
    st.write("Framework para la creación de aplicaciones web interactivas de datos.")

# --- Pie de página ---
st.sidebar.success("👈 Usa el menú lateral para navegar entre las secciones del proyecto.")
st.sidebar.markdown("---")
st.sidebar.write("© 2026 - Proyecto Integrador de Analítica")

