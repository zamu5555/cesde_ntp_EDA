import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Graficos Dengue")

df = pd.read_csv("data/sivigila_dengue.csv", low_memory=False)

df = df.fillna("SIN RESPUESTA")

df = df.replace([
    '',
    ' ',
    'NA',
    'N/A',
    'SIN DATO',
    'SIN INFORMACION',
    'NO REGISTRA',
    'NO APLICA'
], 'SIN RESPUESTA')

df = df.loc[
    (df['sexo_'] != 'SIN RESPUESTA') &
    (df['edad_'] != 'SIN RESPUESTA') &
    (df['year_'] != 'SIN RESPUESTA') &
    (df['comuna'] != 'SIN RESPUESTA') &
    (df['semana'] != 'SIN RESPUESTA')
]

df['edad_'] = pd.to_numeric(df['edad_'], errors='coerce')

df = df.loc[df['edad_'].notna()]

df_hombres = df.loc[df['sexo_'] == 'M']

df_mayores = df.loc[df['edad_'] >= 60]

col1, col2, col3 = st.columns(3)

col1.metric("Total Casos", len(df))

col2.metric("Hombres", len(df_hombres))

col3.metric("Mayores de 60", len(df_mayores))

casos = df.groupby('year_').size().reset_index(name='Casos')

casos = casos.sort_values(by='year_')

fig = px.bar(
    casos,
    x='year_',
    y='Casos',
    color='Casos',
    text='Casos',
    title='Casos por Año'
)

st.plotly_chart(fig, use_container_width=True)

sexo = df.groupby('sexo_').size().reset_index(name='Cantidad')

sexo = sexo.loc[sexo['sexo_'].isin(['M', 'F'])]

fig2 = px.pie(
    sexo,
    names='sexo_',
    values='Cantidad',
    hole=0.5,
    title='Contagios según el sexo'
)

st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(
    df_mayores,
    x='edad_',
    nbins=20,
    title='Incidencia de casos en Mayores de 60 Años',
    range_x=[60, 100]
)

st.plotly_chart(fig3, use_container_width=True)

semana = df.groupby('semana').size().reset_index(name='Casos')

semana = semana.sort_values(by='semana')

fig4 = px.line(
    semana,
    x='semana',
    y='Casos',
    markers=True,
    title='Casos por Semana'
)

st.plotly_chart(fig4, use_container_width=True)

comuna = df.groupby('comuna').size().reset_index(name='Casos')

comuna = comuna.sort_values(by='Casos', ascending=False).head(10)

fig5 = px.bar(
    comuna,
    x='comuna',
    y='Casos',
    color='Casos',
    text='Casos',
    title='Top 10 Comunas con Más Casos'
)

st.plotly_chart(fig5, use_container_width=True)

grupo_semana_sexo = df.groupby(['semana', 'sexo_']).size().reset_index(name='Casos')

fig6 = px.scatter(
    grupo_semana_sexo,
    x='semana',
    y='Casos',
    color='sexo_',
    size='Casos',
    hover_data=['sexo_'],
    title='Casos semanales según el género'
)

st.plotly_chart(fig6, use_container_width=True)

promedio_edad = df.groupby('sexo_')['edad_'].mean().reset_index()

fig7 = px.bar(
    promedio_edad,
    x='sexo_',
    y='edad_',
    color='sexo_',
    text='edad_',
    title='Edad promedio de contagiados según el sexo'
)

st.plotly_chart(fig7, use_container_width=True)

year_sexo = df.groupby(['year_', 'sexo_']).size().reset_index(name='Casos')

fig8 = px.bar(
    year_sexo,
    x='year_',
    y='Casos',
    color='sexo_',
    barmode='group',
    text='Casos',
    title='Casos anuales en hombres y mujeres'
)

st.plotly_chart(fig8, use_container_width=True)