import datetime
import os
import pandas as pd
from streamlit_option_menu import option_menu
from plots import *


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


def calc_no_of_types(df):
    types = []
    for i in df['genre']: types += i
    types = set(types)
    return len(types)


df_top10, df_titles, df_countries = read_files()
df_top10_all_time = top_10_all_time()
df_top10_all_time_movies, df_top10_all_time_series = split_file(df_top10_all_time, 'Type')

with st.sidebar:
    selected = option_menu(
        menu_title='Zakładki',
        options=['Strona Główna', 'Netflix Daily Top 10', 'Netflix Data']
    )

if selected == 'Strona Główna':
    st.title('Wizualizacja projekt')

if selected == 'Netflix Daily Top 10':
    st.title('Netflix Daily Top 10')

    st.write('Który dzień chcesz zobaczyć?')

    date = str(st.date_input('Wybierz date',
                             value=datetime.date(2020, 4, 1),
                             min_value=datetime.date(2020, 4, 1),
                             max_value=datetime.date(2022, 3, 11)))
    ranking = df_top10[df_top10['As of'] == date]['Title']
    table_plot(['Rank', 'Title'], [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ranking])

    bar_plot(df_top10_all_time_movies.iloc[:10], 'Title', 'Days In Top 10')

    bar_plot(df_top10_all_time_series.iloc[:10], 'Title', 'Days In Top 10')

    # czego ludzie więcej oglądają czy netflix exclusive czy nie exclusive
    pie_plot(df_top10_all_time, 'Netflix Exclusive', 'Netflix Exclusive', 0.3)
    pie_plot(df_top10_all_time.Type, df_top10_all_time.Type.values, df_top10_all_time.Type.values, 0.3)

if selected == 'Netflix Data':
    st.title('Netflix Data')
    map_plot(df_countries, 'iso_alpha', 'Count', 800, 800)

    df_titles['genre'] = df_titles['listed_in'].apply(lambda x :  x.replace(' ,',',').replace(', ',',').split(','))
    df_titles_movies, df_titles_series = split_file(df_titles, 'type')
    res_movies = df_titles_movies['genre'].str.join('|').str.get_dummies()
    res_series = df_titles_series['genre'].str.join('|').str.get_dummies()

    corr_heatmap_plot(res_movies)
    corr_heatmap_plot(res_series)
