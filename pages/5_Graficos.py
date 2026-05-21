import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Graficos Dengue")

df = pd.read_csv("data/sivigila_dengue.csv", low_memory=False)

df = df.fillna("SIN RESPUESTA")

df = df.replace([
    '', ' ', 'NA', 'N/A',
    'SIN DATO', 'SIN INFORMACION',
    'NO REGISTRA', 'NO APLICA'
], 'SIN RESPUESTA')

df = df.loc[
    (df['sexo_'] != 'SIN RESPUESTA') &
    (df['edad_'] != 'SIN RESPUESTA') &
    (df['year_'] != 'SIN RESPUESTA') &
    (df['comuna'] != 'SIN RESPUESTA') &
    (df['semana'] != 'SIN RESPUESTA')
]

# ✅ Renombrar todas las columnas de una vez
df.rename(columns={
    'year_': 'año',
    'sexo_': 'sexo',
    'edad_': 'edad'
}, inplace=True)

df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
df = df.loc[df['edad'].notna()]

df_hombres = df.loc[df['sexo'] == 'M']
df_mayores = df.loc[df['edad'] >= 60]

col1, col2, col3 = st.columns(3)
col1.metric("Total Casos", len(df))
col2.metric("Hombres", len(df_hombres))
col3.metric("Mayores de 60", len(df_mayores))

casos = df.groupby('año').size().reset_index(name='Casos')
casos = casos.sort_values(by='año')

fig = px.bar(
    casos,
    x='año', y='Casos',
    color='Casos', text='Casos',
    title='Casos por Año'
)
st.plotly_chart(fig, use_container_width=True)

sexo = df.groupby('sexo').size().reset_index(name='Cantidad')
sexo = sexo.loc[sexo['sexo'].isin(['M', 'F'])]

fig2 = px.pie(
    sexo,
    names='sexo', values='Cantidad',
    hole=0.5,
    title='Contagios según el sexo'
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(
    df_mayores,
    x='edad', nbins=20,
    title='Incidencia de casos en Mayores de 60 Años',
    range_x=[60, 100]
)
st.plotly_chart(fig3, use_container_width=True)

semana = df.groupby('semana').size().reset_index(name='Casos')
semana = semana.sort_values(by='semana')

fig4 = px.line(
    semana,
    x='semana', y='Casos',
    markers=True,
    title='Casos por Semana'
)
st.plotly_chart(fig4, use_container_width=True)

comuna = df.groupby('comuna').size().reset_index(name='Casos')
comuna = comuna.sort_values(by='Casos', ascending=False).head(10)

fig5 = px.bar(
    comuna,
    x='comuna', y='Casos',
    color='Casos', text='Casos',
    title='Top 10 Comunas con Más Casos'
)
st.plotly_chart(fig5, use_container_width=True)

grupo_semana_sexo = df.groupby(['semana', 'sexo']).size().reset_index(name='Casos')

fig6 = px.scatter(
    grupo_semana_sexo,
    x='semana', y='Casos',
    color='sexo', size='Casos',
    hover_data=['sexo'],
    title='Casos semanales según el género'
)
st.plotly_chart(fig6, use_container_width=True)

promedio_edad = df.groupby('sexo')['edad'].mean().reset_index()
promedio_edad['edad'] = promedio_edad['edad'].round(0).astype(int)

fig7 = px.bar(
    promedio_edad,
    x='sexo', y='edad',
    color='sexo', text='edad',
    title='Edad promedio de contagiados según el sexo'
)
st.plotly_chart(fig7, use_container_width=True)

year_sexo = df.groupby(['año', 'sexo']).size().reset_index(name='Casos')

fig8 = px.bar(
    year_sexo,
    x='año', y='Casos',
    color='sexo', barmode='group',
    text='Casos',
    title='Casos anuales en hombres y mujeres'
)
st.plotly_chart(fig8, use_container_width=True)