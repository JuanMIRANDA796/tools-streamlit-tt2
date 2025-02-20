import streamlit as st
import pandas as pd
import sqlite3

# Configurar el título de la aplicación
st.title("📊 Visualizador de Datos Ambientales en Colombia")

# Subida de archivo SQL
uploaded_file = st.file_uploader("Sube un archivo SQL de SQLite", type=["sqlite", "db"])

if uploaded_file is not None:
    # Guardar el archivo temporalmente
    db_path = "database.sqlite"
    with open(db_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Conectarse a la base de datos SQLite
    conn = sqlite3.connect(db_path)

    # Obtener nombres de las tablas
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
    st.write("Tablas disponibles en la base de datos:", tables)

    # Selección de tabla
    table_name = st.selectbox("Selecciona una tabla para visualizar:", tables["name"])

    if table_name:
        # Leer los datos de la tabla seleccionada
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

        # Mostrar el DataFrame en Streamlit
        st.dataframe(df)

        # Exportar a CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV", csv, "datos.csv", "text/csv")

    # Cerrar la conexión
    conn.close()
