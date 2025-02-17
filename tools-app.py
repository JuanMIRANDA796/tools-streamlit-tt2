import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# Función para generar datos aleatorios de agroindustria
def generar_datos(filas, columnas):
    cultivos = ['Maíz', 'Trigo', 'Arroz', 'Café', 'Caña de Azúcar', 'Soja', 'Papa', 'Frutas', 'Verduras']
    precios_base = np.random.uniform(50, 500, size=len(cultivos))
    
    data = []
    for i in range(filas):
        cultivo = np.random.choice(cultivos)
        precio = precios_base[list(cultivos).index(cultivo)] + np.random.uniform(-20, 20)
        tiempo = pd.Timestamp('2025-01-01') + pd.to_timedelta(i, unit='D')
        produccion = np.random.randint(100, 10000)
        
        data.append([cultivo, tiempo, precio, produccion])
    
    df = pd.DataFrame(data, columns=['Cultivo', 'Fecha', 'Precio', 'Producción'])
    return df

# Configuración inicial del Dashboard
st.set_page_config(page_title='Dashboard Agroindustria', layout='wide')

# Barra lateral con opciones
total_filas = st.sidebar.slider("Número de filas", min_value=50, max_value=1000, value=200, step=50)
mostrar_columnas = st.sidebar.multiselect("Seleccionar columnas", ['Cultivo', 'Fecha', 'Precio', 'Producción'], default=['Cultivo', 'Fecha', 'Precio', 'Producción'])

# Generación de datos
df = generar_datos(total_filas, len(mostrar_columnas))

# Filtrar columnas
if mostrar_columnas:
    df = df[mostrar_columnas]

# Mostrar la tabla de datos
st.subheader("📊 Datos Generados")
st.dataframe(df)

# Gráficos interactivos
st.subheader("📈 Visualización de Datos")

grafico_tipo = st.selectbox("Seleccionar tipo de gráfico", ['Línea', 'Barras', 'Dispersión'])

if grafico_tipo == 'Línea':
    fig = px.line(df, x='Fecha', y='Precio', color='Cultivo', title='Evolución del Precio en el Tiempo')
elif grafico_tipo == 'Barras':
    fig = px.bar(df, x='Cultivo', y='Producción', title='Producción por Cultivo', color='Cultivo')
elif grafico_tipo == 'Dispersión':
    fig = px.scatter(df, x='Producción', y='Precio', color='Cultivo', title='Relación entre Producción y Precio')

st.plotly_chart(fig, use_container_width=True)

# Simulación de serie de tiempo en vivo
st.subheader("⏳ Serie de Tiempo en Vivo")
run_live = st.checkbox("Actualizar en tiempo real")

if run_live:
    placeholder = st.empty()
    df_live = df.copy()
    for _ in range(50):
        df_live['Precio'] += np.random.uniform(-5, 5, size=len(df_live))
        fig_live = px.line(df_live, x='Fecha', y='Precio', color='Cultivo', title='Evolución del Precio en Tiempo Real')
        placeholder.plotly_chart(fig_live, use_container_width=True)
        time.sleep(1)

# Botón de reinicio
if st.button("🔄 Resetear Parámetros"):
    st.experimental_rerun()

st.success("Dashboard listo para análisis 🚀")
