import streamlit as st
import src.streamlit as dat
import pandas as pd
import streamlit.components.v1 as components

st.write("""
# Player stats finder
""")

st.dataframe(dat.carga_data())