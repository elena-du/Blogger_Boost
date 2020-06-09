#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 22:30:47 2020

@author: elena
"""
import pandas as pd
import pickle
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

import plotly.graph_objects as go
from dash.dependencies import Input, Output



with open('blogger_1270648_long.pkl', 'rb') as picklefile:
    df = pickle.load(picklefile)
    
df.index = pd.to_datetime(df['date'])

def get_options(list_emotions):
    dict_list = []
    for i in list_emotions:
        dict_list.append({'label': i, 'value': i})
    return dict_list


# Initialise the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
#app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

# Define the app

app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                    
                                 html.Img(src='https://upload.wikimedia.org/wikipedia/commons/3/31/Blogger.svg', 
                                          className='four columns', 
                                          style = {
                                              'height':'20%',
                                              'width':'20%', 
                                              'float':'right', 
                                              'position':'relative', 
                                              'padding-top': 0,
                                              'padding-right': 0}),
                                 html.Br(),
                                 html.Br(),
                                 html.H2('MY EMOTIONS'),
                                 html.P('The way we right may reflect the way we feel.'),
                                 html.P('Select one or more pimary emotions and see how they change from post to post.'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[dcc.Dropdown(id='emotionselector', options=get_options(df['variable'].unique()),
                                                      multi=True, value=[df['variable'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='emotionselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='timeseries', config={'displayModeBar': False}, 
                                           animate=True,
                                           figure=px.line(df,
                                                          x='date',
                                                          y='value',
                                                          color='variable',
                                                          template='plotly_dark').update_layout(
                                                              {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                               'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
                                    )), 
                                dcc.Graph(id='change', config={'displayModeBar': False}, 
                                           animate=True,
                                           figure=px.line(df,
                                                          x='date',
                                                          y='change',
                                                          color='variable',
                                                          template='plotly_dark').update_layout(
                                                              {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                               'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
                                    ))  
                             ])
                              ])
        ]

)
                                                              
@app.callback(Output('timeseries', 'figure'),
              [Input('emotionselector', 'value')])
def update_graph(selected_dropdown_value):
    trace = []
    df_sub = df
    for emotion in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['variable'] == emotion].index,
                                 y=df_sub[df_sub['variable'] == emotion]['value'],
                                 mode='lines',
                                 opacity=0.4,
                                 name=emotion,
                                 textposition='bottom center'))
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#CBE5F2", '#81F08B', '#D7F23A', '#CF696C', '#D4D4D4', '#F0CB69', '#69F0D0', '#F26A3A'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'EMOTIONS OF MY POSTS', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }
    return figure


@app.callback(Output('change', 'figure'),
              [Input('emotionselector', 'value')])
def update_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    trace1 = []
    df_sub = df
    # Draw and append traces for each stock
    for emotion in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['variable'] == emotion].index,
                                 y=df_sub[df_sub['variable'] == emotion]['change'],
                                 mode='lines',
                                 opacity=0.4,
                                 name=emotion,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#CBE5F2", '#81F08B', '#D7F23A', '#CF696C', '#D4D4D4', '#F0CB69', '#69F0D0', '#F26A3A'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=250,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'PULSE OF MY BLOG', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'showticklabels': False, 'range': [df_sub.index.min(), df_sub.index.max()]},
              ),
              }

    return figure


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=4444)