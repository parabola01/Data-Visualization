import streamlit as st
import pandas as pd
import plotly.express as px
import os


st.title('Wizualizacja projekt')


def get_path(file):
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, '..', 'data', file)
    return path


@st.cache
def read_files():
    netflix_top10 = pd.read_csv(get_path('netflix-daily-top-10.csv'))
    # netflix_data = pd.read_csv(get_path('netflix-rotten-tomatoes-metacritic-imdb.csv'))
    return netflix_top10


df_top10 = read_files()
fig = px.pie(
    labels=df_top10.Type.values,
    names=df_top10.Type.values
)
st.plotly_chart(fig)
