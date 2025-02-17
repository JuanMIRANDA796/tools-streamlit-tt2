import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# Configuración inicial de la página
st.set_page_config(page_title='Dashboard Agroindustria', layout='wide')

# Sidebar - Parámetros iniciales
st.sidebar.header('Configuración de Datos')
num_rows = st.sidebar.slider('Número de filas', min_value=10, max_value=500, value=100)
num_cols = st.sidebar.slider('Número de columnas', min_value=3, max_value=7, value=5)

# Columnas disponibles
def generate_data(rows, cols):
    np.random.seed(42)
    cultivos = ['Maíz', 'Trigo', 'Caña de Azúcar', 'Café', 'Algodón']
    fechas = pd.date_range(start='2023-01-01', periods=rows, freq='D')
    
    data = {
        'Fecha': np.random.choice(fechas, rows),
        'Cultivo': np.random.choice(cultivos, rows),
        'Producción (Ton)': np.random.randint(500, 5000, rows),
        'Precio Unitario ($)': np.random.uniform(10, 100, rows).round(2),
        'Demanda': np.random.randint(1000, 10000, rows),
        'Exportaciones (Ton)': np.random.randint(100, 2000, rows),
        'Costo Producción ($)': np.random.uniform(1000, 10000, rows).round(2)
    }
    df = pd.DataFrame(data)
    return df.iloc[:, :cols]

# Generar dataset dinámico
df = generate_data(num_rows, num_cols)

# Sidebar - Selección de columnas a visualizar
selected_columns = st.sidebar.multiselect('Seleccionar columnas', df.columns.tolist(), default=df.columns.tolist())

# Checkbox de reinicio
def reset_params():
    st.session_state['num_rows'] = 100
    st.session_state['num_cols'] = 5
    st.session_state['selected_columns'] = df.columns.tolist()
st.sidebar.button('Reiniciar Parámetros', on_click=reset_params)

# Filtrar dataset según selección
df_filtered = df[selected_columns]

# Sección de visualización de datos
st.title('Dashboard Agroindustria 📊')
st.write('Datos simulados de precios, producción y demanda en el sector agroindustrial.')

# Mostrar dataframe
st.dataframe(df_filtered)

# Gráficos interactivos
st.subheader('Análisis de Datos')

# Gráfico de Producción por Cultivo
if 'Producción (Ton)' in df_filtered.columns:
    fig_prod = px.bar(df_filtered, x='Cultivo', y='Producción (Ton)', color='Cultivo', title='Producción por Cultivo')
    st.plotly_chart(fig_prod, use_container_width=True)

# Gráfico de Precio en el Tiempo
if 'Fecha' in df_filtered.columns and 'Precio Unitario ($)' in df_filtered.columns:
    fig_precio = px.line(df_filtered, x='Fecha', y='Precio Unitario ($)', color='Cultivo', title='Precio Unitario en el Tiempo')
    st.plotly_chart(fig_precio, use_container_width=True)

# Gráfico de Demanda vs. Exportaciones
if 'Demanda' in df_filtered.columns and 'Exportaciones (Ton)' in df_filtered.columns:
    fig_demand = px.scatter(df_filtered, x='Demanda', y='Exportaciones (Ton)', color='Cultivo', title='Demanda vs Exportaciones')
    st.plotly_chart(fig_demand, use_container_width=True)

# Gráfico dinámico de serie de tiempo cíclica
time_series_data = pd.DataFrame({'Fecha': pd.date_range(start='2024-01-01', periods=100, freq='D'),
                                 'Valor': np.random.rand(100) * 100})

st.subheader('Serie de Tiempo Dinámica Cíclica')
chart_placeholder = st.empty()

while True:
    for i in range(50, 100):
        fig_time = px.line(time_series_data.iloc[:i], x='Fecha', y='Valor', title='Evolución en el Tiempo')
        chart_placeholder.plotly_chart(fig_time, use_container_width=True, key=f'plotly_chart_{i}')
        time.sleep(0.1)
    


# Footer
st.markdown('---')
st.markdown('📌 **Desarrollado con Streamlit y Plotly - Datos Simulados para Análisis Agroindustrial**')
