import datetime
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
# fig = px.pie(
#     labels=df_top10.Type.values,
#     names=df_top10.Type.values
# )
# st.plotly_chart(fig)


st.write('Który dzień chcesz zobaczyć?')

date = str(st.date_input('Wybierz date',
                     value=datetime.date(2020, 4, 1),
                     min_value=datetime.date(2020, 4, 1),
                     max_value=datetime.date(2022, 3, 11)))
ranking = df_top10[df_top10['As of'] == date]['Title']

for i, title in enumerate(ranking):
    st.write(i+1, title)
