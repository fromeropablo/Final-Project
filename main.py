import streamlit as st
import src.streamlit as dat
import pandas as pd
import streamlit.components.v1 as components
from PIL import Image

st.write("""
# No quiero mango, tampoco jalea, pero marico el que lo lea
""")

st.dataframe(dat.carga_data())

personaje = st.selectbox(

    "Selecciona un personaje", dat.lista_jugadores()

)

dat.statsbomb(personaje)
imagen = Image.open("./images/plot.png")
st.image(imagen)


st.dataframe(dat.shots_data())
player = st.selectbox(

    "Selecciona un personaje", dat.lista_tiradores()

)
dat.mapa(player)
st.pyplot()