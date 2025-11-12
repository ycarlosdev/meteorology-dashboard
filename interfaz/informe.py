import streamlit as st
import pandas as pd


# Simulamos un DataFrame de ejemplo
# Recuperar los datos guardados en la sesión
datos = st.session_state.datos

df = pd.DataFrame([datos])

# Convertir a CSV y JSON
csv_data = df.to_csv(index=False).encode("utf-8")
json_data = df.to_json(orient="records", indent=2).encode("utf-8")

st.title("🌤️ Datos Meteorológicos")

st.write("Aquí puedes descargar los datos en el formato que prefieras:")

# Separador visual
st.divider()

# Agrupamos los botones en columnas
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="📥 Descargar CSV",
        data=csv_data,
        file_name="datos_meteorologicos.csv",
        mime="text/csv",
        use_container_width=True,
    )

with col2:
    st.download_button(
        label="📥 Descargar JSON",
        data=json_data,
        file_name="datos_meteorologicos.json",
        mime="application/json",
        use_container_width=True,
    )

# Un expander para mostrar una vista previa de los datos
with st.expander("👀 Vista previa de los datos"):
    st.dataframe(df, use_container_width=True)
