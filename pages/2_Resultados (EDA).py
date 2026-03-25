import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Plantilla de Resultados - Proyecto Analítica",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Plantilla de Entrega: Resultados del EDA")
st.markdown("""
### Instrucciones
Utiliza esta página para documentar tus hallazgos. Completa cada sección basándote en lo que descubriste en la pestaña de **Análisis Exploratorio**.
Al finalizar, puedes previsualizar tu reporte consolidado.
""")

st.divider()

# --- Formulario de Resultados ---
with st.container():
    st.header("🔍 1. Identificación y Contexto")
    contexto = st.text_area(
        "¿De qué se trata el dataset? (Deducción del origen, tema y propósito)",
        placeholder="Este conjunto de datos constituye un registro epidemiológico del sistema SIVIGILA sobre el dengue en Colombia, cuyo origen se sitúa en instituciones de salud (EAS y EPS) con un enfoque principal en Medellín, Antioquia, según los códigos geográficos registrados; su tema central es la vigilancia de enfermedades transmitidas por vectores a través de variables demográficas, clínicas y administrativas, con el propósito fundamental de monitorear el avance del virus, identificar brotes en barrios específicos y evaluar la gravedad de los casos para orientar la toma de decisiones en salud pública.",
        height=150
    )

    st.header("❗ 2. Calidad de los Datos")
    calidad = st.text_area(
        "¿Qué encontraste sobre los datos faltantes y la limpieza?",
        placeholder="En cuanto a la interpretación de los números y categorías, las variables muestran que el dengue afecta a todos los grupos etarios con una unidad de medida predominante en años, mientras que en el ámbito geográfico se observa una moda recurrente en comunas como Belén, San Javier y Laureles; clínicamente, la mayoría de los registros presentan una moda en síntomas como fiebre y cefalea, y en la gestión hospitalaria predomina el manejo ambulatorio, aunque existe un seguimiento estricto de indicadores críticos como la caída de plaquetas y el dolor abdominal para clasificar la gravedad de cada evento.",
        height=150
    )

    st.header("📈 3. Hallazgos Estadísticos Key")
    estadisticas = st.text_area(
        "Interpretación de los números y categorías principales (Medias, modas, etc.)",
        placeholder="El mensaje principal que nos dan estos datos es la naturaleza endémica y urbana del dengue en la región, subrayando que el virus no es un fenómeno aislado sino una amenaza constante que requiere vigilancia permanente; la información revela que factores como la densidad poblacional en barrios específicos facilitan la propagación, por lo que el dataset funciona como una herramienta predictiva esencial para que las autoridades de salud identifiquen patrones históricos, anticipen brotes y enfoquen los esfuerzos de prevención en las zonas de mayor riesgo detectadas a lo largo de los años.",
        height=150
    )

    st.header("💡 4. Conclusión Final")
    conclusion = st.text_area(
        "¿Cuál es el mensaje principal que nos dan estos datos?",
        placeholder="En conclusión, el análisis estadístico del dataset revela una incidencia acumulada masiva con 54,435 casos registrados en un periodo de 11 años, donde la estructura de los datos permite identificar que el 100% de la muestra está codificada bajo la vigilancia de fiebre y síntomas relacionados. Las métricas de tendencia central indican que, aunque el dengue afecta a personas de todas las edades, la unidad de medida predominante es el año (valor 1), con una dispersión geográfica concentrada en Belén, San Javier y Laureles. Desde una perspectiva de severidad, el uso de variables binarias (donde 1 es presencia y 2 es ausencia) muestra que síntomas como fiebre, cefalea y mialgias tienen una frecuencia relativa cercana al 90% en los reportes, mientras que indicadores críticos como la caída de plaquetas (caida_plaq) y el dolor abdominal (dolor_abdo) actúan como predictores estadísticos de hospitalización, la cual, aunque es la minoría en términos de moda, representa una carga operativa constante para el sistema de salud de Medellín.",
        height=100
    )

st.divider()

# --- Generación de Reporte ---
if st.button("🚀 Generar Previsualización del Reporte"):
    if contexto and calidad and estadisticas and conclusion:
        st.success("✅ Reporte Generado Exitosamente")
        
        reporte_md = f"""
        # Reporte de Análisis Exploratorio de Datos
        
        ## 1. Identificación y Contexto
        {contexto}
        
        ## 2. Calidad de los Datos
        {calidad}
        
        ## 3. Hallazgos Estadísticos Clave
        {estadisticas}
        
        ## 4. Conclusión Final
        {conclusion}
        
        ---
        *Generado por el módulo de Reportes - Proyecto Integrador*
        """
        
        st.markdown(reporte_md)
        st.download_button(
            label="📥 Descargar Reporte (.md)",
            data=reporte_md,
            file_name="reporte_eda_estudiante.md",
            mime="text/markdown"
        )
    else:
        st.warning("⚠️ Por favor, completa todas las secciones antes de generar el reporte.")

# --- Barra Lateral ---
st.sidebar.info("Esta es tu hoja de trabajo. Asegúrate de analizar bien los datos antes de escribir tus conclusiones.")
st.sidebar.markdown("---")
st.sidebar.write("© 2026 - Plantilla de Resultados")
