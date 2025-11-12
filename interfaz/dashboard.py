import streamlit as st
import sys

sys.path.append("d:\\Trabajo\\Web Scraping\\meteorology-dashboard")
from spider import obtener_html_localizacion,extraer_datos

# Iniciando datos y almacenandolos en la session_state
if "datos" not in st.session_state:
    with st.spinner("Iniciando..."):
        html = obtener_html_localizacion("miami")
        st.session_state.datos = extraer_datos(html)
        # Mostrar las claves disponibles en el diccionario
        st.markdown(f"<h1 style='text-align: left; color: #1E90FF;'>Tiempo</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: left; color: #FFA500;'>Miami</h3>", unsafe_allow_html=True)

# Barra de búsqueda
col1, col2 = st.columns([4,1])  # Una columna más grande para el input
with col1:
    ubicacion = st.text_input("Escribe una ciudad", placeholder="Ej. Madrid, España",label_visibility="collapsed")
with col2:
    buscar = st.button("🔍", use_container_width=True)
    
with st.container():
    if "datos" not in st.session_state:
        with st.spinner("Buscando..."):
            html = obtener_html_localizacion(ubicacion)
            st.session_state.datos = extraer_datos(html)
            # Mostrar las claves disponibles en el diccionario
            st.markdown(f"<h1 style='text-align: left; color: #1E90FF;'>Tiempo</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: left; color: #FFA500;'>{ubicacion.capitalize()}</h3>", unsafe_allow_html=True)

        
# Obteniendo los datos meteorológicos
with st.container():
    if buscar:
        if ubicacion.strip() == "":
            st.info("Escribe el nombre de la ciudad que deseas buscar")
        else:
            with st.spinner("Buscando..."):
                html = obtener_html_localizacion(ubicacion)
                st.session_state.datos = extraer_datos(html)
                # Mostrar las claves disponibles en el diccionario
                st.markdown(f"<h1 style='text-align: left; color: #1E90FF;'>Tiempo</h1>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: left; color: #FFA500;'>{ubicacion.capitalize()}</h3>", unsafe_allow_html=True)


# Datos meteorológicos
col1, col2 = st.columns(2)

with col1:
    st.metric(label="☁️ Clima", value=st.session_state.datos["clima"])
    st.metric(label="🌡️ Temperatura", value=st.session_state.datos["temperatura"])
    st.metric(label="🌫️ Viento", value=st.session_state.datos["viento"])

with col2:
    st.metric(label="🌬️ Calidad del aire", value=st.session_state.datos["calidad_viento"])
    st.metric(label="🤒 Sensación Térmica", value=st.session_state.datos["sensacion_termica"])
    st.metric(label="💨 Ráfagas de Viento", value=st.session_state.datos["rafagas"])
 
 

# Estilo adicional.
st.markdown(
    """
    <style>
        .stMetric {
            text-align: center !important;
            background-color: #F0F8FF;
            padding: 12px;
            border-radius: 12px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        }
    </style>
    """,
    unsafe_allow_html=True
)

