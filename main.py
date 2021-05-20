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

portada = Image.open("./images/Mirotic.jpg")
st.image(portada)


st.write("""
## Choose a cluster: 
""")

cluster = st.selectbox(

    "Selecciona un cluster", dat.lista_clusters()
)
datagraf = dat.grafico_cl(cluster)
fig = px.scatter(datagraf, x="PTS", y="FG%", hover_name = "PLAYER_NAME", color = "Team", size = "MIN", width = 1200, height = 800)
st.plotly_chart(fig)


persona = st.selectbox(

    "## Choose a player from this cluster:", list(datagraf.PLAYER_NAME.unique())

)

dat.statsbomb(persona)
imagen = Image.open("./images/plot.png")
st.image(imagen)

persona = persona.split(" ")[-1]
long_names = dat.lista_tiradores()

for i in long_names:
    if persona in i:
        dat.mapa(i)
        imagen = Image.open("./images/map.png")
        imagen = imagen.rotate(90)
        st.image(imagen)
