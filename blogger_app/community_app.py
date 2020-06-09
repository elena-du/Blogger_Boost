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



with open('blogger_com_data_19320_tsne3d.pkl', 'rb') as picklefile:
    df1 = pickle.load(picklefile)
    
list_topics = df1['prime_topic'].unique()
def get_options(list_topics):
    dict_list = []
    for i in list_topics:
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
                                 html.H2('MY COMMUNITY'),
                                 html.P('Explore what people in Blogger.com comunity write about.'),
                                 html.P('Select one or more key topics you want to dig into.'),
                                 html.Div(
                                     className='div-for-checklist',
                                     children=[
                                         dcc.Checklist(id='topicselector', options=[
                                         {'label': 'Days of My Life', 'value': 'mundane'},
                                         {'label': 'Romance', 'value': 'love_relationship'},
                                         {'label': 'Hobbies, Hobbies, Hobbies...', 'value': 'blogging'},
                                         {'label':  'Faith', 'value': 'faith'},
                                         {'label':  'Politics', 'value': 'politics'},
                                         {'label':  'Slang People', 'value': 'jargon'},
                                         {'label':  'Fun Teen Spirit', 'value': 'fun_teen_days'},
                                         ],
                                         value=[df1['prime_topic'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='topicselector'
                                                      ),
                                         html.Br(),
                                         dcc.Input(id="input1", type="text", placeholder="")
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='topicmodel', config={'displayModeBar': False}, 
                                           animate=True,
                                           figure=px.line(df1,
                                                          x='xs',
                                                          y='ys',
                                                          #z='zs',
                                                          color='prime_topic',
                                                          template='plotly_dark').update_layout(
                                                              {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                               'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
                                    )), 
                                html.Div(id="output")
                             ])
                              ])
        ]

)
                                                              
@app.callback(Output('topicmodel', 'figure'),
              [Input('topicselector', 'value'),
               Input('input1', 'value')])
def update_graph(selected_checklist_value, input1):
    trace = []
    df_sub = df1
    for topic in selected_checklist_value:
        trace.append(go.Scatter3d(x=df_sub[df_sub['prime_topic'] == topic]['xs'],
                                 y=df_sub[df_sub['prime_topic'] == topic]['ys'],
                                 z=df_sub[df_sub['prime_topic'] == topic]['zs'],
                                 mode='markers',
                                 marker = dict(size=10,  
                                               line = dict(color = '#07557D', width = 2), 
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

    trace0 = go.Scatter3d(x=df_sub[df_sub['blogger_id'] == input1]['xs'],
                          y=df_sub[df_sub['blogger_id'] == input1]['ys'],
                          z=df_sub[df_sub['blogger_id'] == input1]['zs'], 
                          mode='markers',
                          opacity=0.99,
                          name=topic,
                          text="ME",
                          hovertemplate='<b><i>%{text}</i></b>',
                          textposition='bottom center')
    
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
    Output("output", "children"),
    [Input("input1", "value")])

def update_output(input1):
    my_topic = df1[df1['blogger_id'] == input1]['prime_topic'].values
    my_topic = str(my_topic).upper()
    return u'My community is {}'.format(my_topic)
    
# def update_graph(selected_checklist_value):
#     trace = []
#     df_sub = df1
#     for topic in selected_checklist_value:
#         trace.append(go.Scatter3d(x=df_sub[df_sub['prime_topic'] == topic]['xs'],
#                                  y=df_sub[df_sub['prime_topic'] == topic]['ys'],
#                                  z=df_sub[df_sub['prime_topic'] == topic]['zs'],
#                                  mode='markers',
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

#     traces = [trace]
#     data = [val for sublist in traces for val in sublist]
#     figure = {'data': data,
#               'layout': go.Layout(
#                   colorway=[ '#81F08B', '#D7F23A', '#CF696C', '#D4D4D4', '#F0CB69', '#69F0D0', '#F26A3A'],
#                   template='plotly_dark',
#                   paper_bgcolor='rgba(0, 0, 0, 0)',
#                   plot_bgcolor='rgba(0, 0, 0, 0)',
#                   margin={'b': 15},
#                   #hovermode='x',
#                   autosize=True,
#                   title={'text': 'My BLOGGER.COM Community', 'font': {'color': 'white'}, 'x': 0.5},
#                   xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
#               ),

#               }
    
#     df_sub2 = df1[df1['blogger_id'] == '1270648']
#     trace = []
#     for topic in selected_checklist_value:
#         trace.append(go.Scatter3d(x=df_sub2[df_sub2['prime_topic'] == topic]['xs'],
#                                  y=df_sub2[df_sub2['prime_topic'] == topic]['ys'],
#                                  z=df_sub2[df_sub2['prime_topic'] == topic]['zs'],
#                                  mode='markers',
#                                  opacity=0.9,
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

    
#     return figure



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=4445)