import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# Configuración inicial del Dashboard
st.set_page_config(page_title='Dashboard Agroindustria', layout='wide')

# Sidebar para navegación
st.sidebar.title("📌 Navegación")
page = st.sidebar.radio("Seleccionar Página", ["Generar Datos", "Cargar CSV"])

if page == "Generar Datos":
    # Función para generar datos aleatorios de agroindustria
    def generar_datos(filas):
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
    
    # Parámetros en la barra lateral
    total_filas = st.sidebar.slider("Número de filas", min_value=50, max_value=1000, value=200, step=50)
    
    # Generación de datos
    df = generar_datos(total_filas)
    
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

elif page == "Cargar CSV":
    st.subheader("📂 Cargar Archivo CSV")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type=['csv'])
    
    if uploaded_file is not None:
        df_csv = pd.read_csv(uploaded_file)
        st.write("📋 Vista Previa de los Datos:")
        st.dataframe(df_csv)
        
        # Gráfico dinámico con los datos cargados
        if 'Fecha' in df_csv.columns and 'Precio' in df_csv.columns:
            fig_csv = px.line(df_csv, x='Fecha', y='Precio', title='Evolución del Precio en CSV')
            st.plotly_chart(fig_csv, use_container_width=True)
        else:
            st.warning("El CSV debe contener las columnas 'Fecha' y 'Precio' para graficar.")
    
    else:
        st.info("Por favor, sube un archivo CSV para analizar los datos.")
    
# Botón de reinicio
if st.sidebar.button("🔄 Resetear Parámetros"):
    st.experimental_rerun()

st.success("Dashboard listo para análisis 🚀")
