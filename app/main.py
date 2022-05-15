import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime
import os

st.title('Wizualizacja projekt')


def get_path(file):
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, '..', 'data', file)
    return path


def read_files():
    netflix_top10 = pd.read_csv(get_path('netflix-daily-top-10.csv'))
    netflix_data = pd.read_csv(get_path('netflix_titles.csv'))
    netfix_countries = pd.read_csv(get_path('netflix-countries.csv'))
    return netflix_top10, netflix_data, netfix_countries


def top_10_all_time():
    df1 = df_top10.copy()
    df1.sort_values(by='Days In Top 10', ascending=False, inplace=True)
    df1['Title'] = df1['Title'].drop_duplicates(keep='first')
    df1 = df1.dropna()
    return df1


def split_file(df, col):
    df_movies = df[df[col] == 'Movie']
    df_series = df[df[col] == 'TV Show']

    return df_movies, df_series


df_top10, df_titles, df_countries = read_files()

st.write('Który dzień chcesz zobaczyć?')

date = str(st.date_input('Wybierz date',
                         value=datetime.date(2020, 4, 1),
                         min_value=datetime.date(2020, 4, 1),
                         max_value=datetime.date(2022, 3, 11)))
ranking = df_top10[df_top10['As of'] == date]['Title']

for i, title in enumerate(ranking):
    st.write(i + 1, title)


df_top10_all_time = top_10_all_time()
df_top10_all_time_movies, df_top10_all_time_series = split_file(df_top10_all_time, 'Type')

fig = px.bar(df_top10_all_time_movies.iloc[:10], x='Title', y='Days In Top 10')
st.plotly_chart(fig)

fig = px.bar(df_top10_all_time_series.iloc[:10], x='Title', y='Days In Top 10')
st.plotly_chart(fig)

# czego ludzie więcej oglądają czy netflix exclusive czy nie exclusive
fig = px.pie(
    df_top10_all_time,
    hole=0.3,
    labels='Netflix Exclusive',
    names='Netflix Exclusive')
st.plotly_chart(fig)

fig = px.pie(
    hole=0.3,
    labels=df_top10_all_time.Type.values,
    names=df_top10_all_time.Type.values
)
st.plotly_chart(fig)


fig = px.choropleth(
    df_countries,
    locations='iso_alpha',
    color='Count',
    color_continuous_scale=px.colors.sequential.Reds,
    width=800,
    height=800
)
st.plotly_chart(fig)

df_titles['genre'] = df_titles['listed_in'].apply(lambda x :  x.replace(' ,',',').replace(', ',',').split(','))
df_titles_movies, df_titles_series = split_file(df_titles, 'type')
res_movies = df_titles_movies['genre'].str.join('|').str.get_dummies()
res_series = df_titles_series['genre'].str.join('|').str.get_dummies()


def corr_heatmap(df):
    corr = df.corr()
    heat = go.Heatmap(z=corr, x=corr.columns.values, y=corr.columns.values)
    layout = go.Layout(width=800, height=800)
    figure = go.Figure(data=heat, layout=layout)
    return figure


def calc_no_of_types(df):
    types = []
    for i in df['genre']: types += i
    types = set(types)
    return len(types)


fig = corr_heatmap(res_movies)
st.plotly_chart(fig)


fig = corr_heatmap(res_series)
st.plotly_chart(fig)
