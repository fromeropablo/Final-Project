import streamlit as st
import src.streamlit as dat
import pandas as pd
import streamlit.components.v1 as components
from PIL import Image

st.set_option('deprecation.showPyplotGlobalUse', False)
st.write("""
# No quiero mango, tampoco jalea, pero marico el que lo lea
""")

persona = st.selectbox(

    "Selecciona un personaje", dat.lista_tiradores()

)

dat.mapa(persona)
st.pyplot()

persona = persona[4:]
long_names = dat.lista_jugadores()

for i in long_names:
    if persona in i:
        dat.statsbomb(i)
        imagen = Image.open("./images/plot.png")
        st.image(imagen)








"""
personaje = st.selectbox(

    "Selecciona un personaje", 

)
"""