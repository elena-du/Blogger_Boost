#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:28:37 2020

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



with open('blogger_com_data_19320_tsne3d.pkl', 'rb') as picklefile:
    df1 = pickle.load(picklefile)
    
list_topics = df1['Prime Topic'].unique()
def get_options(list_topics):
    dict_list = []
    for i in list_topics:
        dict_list.append({'label': i, 'value': i})
    return dict_list

app = dash.Dash(__name__)

app.layout = html.Div(
                 children=[
                     html.Div(className='row',
                              children=[
                                  html.Div(className='twelve columns div-user-controls', 
                                      children = [
                                          html.H2('GET BETTER BLOGGING EXPERIENCE: learn about emotions you express and people alike around you')])]), 
                     html.Div(className='row',
                              children=[
                                  html.Div(className='four columns div-user-controls',
                                           children=[
                                               html.Img(src='https://upload.wikimedia.org/wikipedia/commons/3/31/Blogger.svg', 
                                                        className='four columns', 
                                                        style = {'height':'25%','width':'25%', 'float':'right', 'position':'relative', 'padding-top': 0, 'padding-right': 0}),
                                               html.Br(),
                                               html.Br(),
                                               html.H2('MY COMMUNITY'),
                                               html.P('Select one or more key topics you want to dig into'),
                                               dcc.Checklist(id='topicselector',
                                                             className='topicselector',
                                                             options=get_options(list_topics),
                                                             value=[],#[df1['prime_topic'].sort_values()[0]],
                                                             labelStyle={'display': 'block'},
                                                             #style={'backgroundColor': 'darkgray'},
                                                             #labelStyle={'display':'inline-block'}
                                                      ),
                                               html.Br(),
                                               dcc.Input(id='input1', type='text'),
                                               html.Br(),
                                               html.Br(),
                                               html.Br(),
                                               html.Div(id="my_community")
                                               
                                               
                                               ]),
                                 html.Div(className='eight columns div-for-charts bg-white',
                                          children=[
                                              dcc.Graph(id='topicmodel',
                                                        config={'displayModeBar': False}, 
                                                        animate=True,
                                                        figure=px.scatter( 
                                                          template='plotly_dark').update_layout(
                                                              {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                               'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
                                                              ))
                                              
                                                        
                                              
                                                              
                                              
                                              ]),
                                  #html.Div(className='eight columns div-for-charts bg-blue'),
                                  html.Div(className='eight columns div-for-charts bg-white',
                                           id="output")
                                  ])])
                                         


@app.callback(Output('topicmodel', 'figure'),
              [Input('topicselector', 'value')])
def update_graph(selected_checklist_value):
    trace = []
    df_sub = df1
    for topic in selected_checklist_value:
        trace.append(go.Scatter3d(x=df_sub[df_sub['Prime Topic'] == topic]['xs'],
                                 y=df_sub[df_sub['Prime Topic'] == topic]['ys'],
                                 z=df_sub[df_sub['Prime Topic'] == topic]['zs'],
                                 mode='markers',
                                 marker = dict(size=10,  
                                               line = dict(color = '#4C4C4C', width = 3), 
                                               opacity=0.5),
                                 opacity=0.4,
                                 name=topic,
                                 text="My zodiac is " + 
                                         df_sub['name'].map(str) + 
                                         ". I am " + df_sub['age'] + 
                                         " and " + df_sub['gender'] +
                                         ". My occupation is " + df_sub['occupation'] +
                                         ". Search me by my ID " +
                                         df_sub['blogger_id'],
                                 hovertemplate='<b><i>%{text}</i></b>',
                                 textposition='bottom center'))
    
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=[ '#81F08B', '#D7F23A', '#CF696C', '#D4D4D4', '#F0CB69', '#69F0D0', '#F26A3A'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  #hovermode='x',
                  autosize=True,
                  title={'text': 'My BLOGGER.COM Community', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              )

              }
    return figure

@app.callback(
    Output("my_community", "children"),
    [Input("input1", "value")])

def update_output(input1):
    my_topic = df1[df1['blogger_id'] == input1]['Prime Topic'].values
    my_topic = str(my_topic).upper()
    my_topic = my_topic.replace("['", '').replace("']", '').replace("[", '').replace("]", '')
    return u'You belong to {} community!'.format(my_topic)

# @app.callback(Output('new_traces', 'figure'),
#               [Input('input1', 'value'), 
#                Input('topicmodel', 'figure'),
#                Input('topicselector', 'value')])
# def update_graph1(input1, topicmodel, selected_checklist_value):

#     df_sub2 = df1[df1['blogger_id'] == input1]
    
#     trace0 = go.Scatter3d(x=df_sub2['xs'],
#                           y=df_sub2['ys'],
#                           z=df_sub2['zs'], 
#                           mode='markers',
#                           opacity=0.99,
#                           #name=topic,
#                           text="ME",
#                           hovertemplate='<b><i>%{text}</i></b>',
#                           textposition='bottom center')

#     trace = []
#     df_sub = df1
#     for topic in selected_checklist_value:
#         trace.append(go.Scatter3d(x=df_sub[df_sub['prime_topic'] == topic]['xs'],
#                                  y=df_sub[df_sub['prime_topic'] == topic]['ys'],
#                                  z=df_sub[df_sub['prime_topic'] == topic]['zs'],
#                                  mode='markers',
#                                  marker = dict(size=10,  
#                                                line = dict(color = '#4C4C4C', width = 3), 
#                                                opacity=0.5),
#                                  opacity=0.4,
#                                  name=topic,
#                                  text="My zodiac is " + 
#                                          df_sub['name'].map(str) + 
#                                          ". I am " + df_sub['age'] + 
#                                          " and " + df_sub['gender'] +
#                                          ". My occupation is " + df_sub['occupation'] +
#                                          ". Search me by my ID " +
#                                          df_sub['blogger_id'],
#                                  hovertemplate='<b><i>%{text}</i></b>',
#                                  textposition='bottom center'))
    
    
#     traces = [trace, trace0]
#     data = [val for sublist in traces for val in sublist]
#     figure = {'data': data,
#               'layout': go.Layout(
#                   colorway=[ '#81F08B', '#D7F23A', '#CF696C', '#D4D4D4', '#F0CB69', '#69F0D0', '#F26A3A', 'white'],
#                   template='plotly_dark',
#                   paper_bgcolor='rgba(0, 0, 0, 0)',
#                   plot_bgcolor='rgba(0, 0, 0, 0)',
#                   margin={'b': 15},
#                   #hovermode='x',
#                   autosize=True,
#                   title={'text': 'My BLOGGER.COM Community', 'font': {'color': 'white'}, 'x': 0.5},
#                   xaxis={'range': [df_sub2.index.min(), df_sub2.index.max()]}
#               )

#               }

#     return figure


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=5080)







                                        