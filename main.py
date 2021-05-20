import streamlit as st
import src.streamlit as dat
import pandas as pd
import streamlit.components.v1 as components
from PIL import Image
import plotly.express as px

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.write("""
# What happen if we apply geography knowledge to basketball?
""")

portada = Image.open("./images/gasol.jpeg")
st.image(portada)


st.write("""
## Choose a cluster: 
""")

cluster = st.selectbox(

    "Choose a cluster", dat.lista_clusters()
)

col1,col2=st.beta_columns(2)
with col1:
    datagraf = dat.grafico_cl(cluster)
    fig = px.scatter(datagraf, x="PTS", y="FG%", hover_name = "PLAYER_NAME", color = "Team", size = "MIN")
    st.plotly_chart(fig)
with col2:
    description = dat.cluster_description(cluster)
    st.table(description)

st.write("""
## Choose a player from this cluster: 
""")


persona = st.selectbox(

    "Choose a player:", list(datagraf.PLAYER_NAME.unique())

)

col3,col4=st.beta_columns(2)
with col3:
    dat.statsbomb(persona)
    imagen = Image.open("./images/plot.png")
    imagen = imagen.resize((800,1000),Image.ANTIALIAS)
    st.image(imagen)
with col4:
    persona = persona.split(" ")[-1]
    long_names = dat.lista_tiradores()

    for i in long_names:
        if persona in i:
            dat.mapa(i)
            imagen = Image.open("./images/map.png")
            imagen = imagen.rotate(90)
            st.image(imagen)
