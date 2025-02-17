import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# Configuración inicial de la página
st.set_page_config(page_title='Dashboard Agroindustria', layout='wide')

# Gráfico dinámico de serie de tiempo cíclica
time_series_data = pd.DataFrame({'Fecha': pd.date_range(start='2024-01-01', periods=100, freq='D'),
                                 'Valor': np.random.rand(100) * 100})

st.title('Serie de Tiempo Dinámica Cíclica 📈')
chart_placeholder = st.empty()

while True:
    for i in range(50, 100):
        fig_time = px.line(time_series_data.iloc[:i], x='Fecha', y='Valor', title='Evolución en el Tiempo')
        chart_placeholder.plotly_chart(fig_time, use_container_width=True)
        time.sleep(0.1)
    
    for i in range(100, 50, -1):
        fig_time = px.line(time_series_data.iloc[:i], x='Fecha', y='Valor', title='Evolución en el Tiempo')
        chart_placeholder.plotly_chart(fig_time, use_container_width=True)
        time.sleep(0.1)

# Footer
st.markdown('---')
st.markdown('📌 **Desarrollado con Streamlit y Plotly - Datos Simulados para Análisis Agroindustrial**')
