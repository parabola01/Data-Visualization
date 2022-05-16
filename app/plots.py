import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def pie_plot(df, label, name, hole_size=0):
    fig = px.pie(df, labels=label, names=name, hole=hole_size, color_discrete_sequence=['#b20710', '#221f1f'])
    st.plotly_chart(fig)


def bar_plot(df, x, y):
    fig = px.bar(df, x, y, color_discrete_sequence=['#b20710'])
    st.plotly_chart(fig)


def map_plot(df, location, colors, w, h):
    fig = px.choropleth(df, locations=location, color=colors, width=w, height=h,
                        color_continuous_scale=['#221f1f', '#b20710'])
    st.plotly_chart(fig)


def corr_heatmap_plot(df):
    corr = df.corr()
    heat = go.Heatmap(z=corr, x=corr.columns.values, y=corr.columns.values, colorscale=['#221f1f', '#b20710'])
    layout = go.Layout(width=800, height=800)
    fig = go.Figure(data=heat, layout=layout)
    st.plotly_chart(fig)


def table_plot(vals, cols):
    fig = go.Figure(data=go.Table(header=dict(values=vals, fill_color='#b20710'),
                                  cells=dict(values=cols, fill_color='#221f1f')))
    # fig.update_layout(width=800, height=800)
    st.plotly_chart(fig)