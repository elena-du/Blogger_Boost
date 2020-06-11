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


#with open('blogger_com_data_330677_11_clean_sentiment_v_pl_normalized.pkl', 'rb') as picklefile:
#    df = pickle.load(picklefile)
#df.index = pd.to_datetime(df['date'])


with open('blogger_com_data_19320_tsne3d.pkl', 'rb') as picklefile:
    df1 = pickle.load(picklefile)
    
    
with open('../../data/blogger_com_data_330676_plutchik.pkl', 'rb') as picklefile:
    plutchik = pickle.load(picklefile)
    
#df.index = pd.to_datetime(df['date'])
    
def get_plutchik_data(df, blogger_id='4162441'):
    
    try:
    
        df_sub = df[df['blogger_id']==blogger_id].sort_values(by='date', ascending = True)

        if df_sub.shape[0] > 5:

            df_sub.drop('blogger_id', axis=1, inplace=True)
            df_sub.set_index('date', inplace=True)

            df_sub['trust_change'] = df_sub['trust'] - df_sub['trust'].shift(1)
            df_sub['fear_change'] = df_sub['fear'] - df_sub['fear'].shift(1)
            df_sub['sadness_change'] = df_sub['sadness'] - df_sub['sadness'].shift(1)
            df_sub['anger_change'] = df_sub['anger'] - df_sub['anger'].shift(1)
            df_sub['surprise_change'] = df_sub['surprise'] - df_sub['surprise'].shift(1)
            df_sub['disgust_change'] = df_sub['disgust'] - df_sub['disgust'].shift(1)
            df_sub['joy_change'] = df_sub['joy'] - df_sub['joy'].shift(1)
            df_sub['anticipation_change'] = df_sub['anticipation'] - df_sub['anticipation'].shift(1)

            df_sub = df_sub.iloc[1:].reset_index()
            
            df1 = pd.melt(df_sub, id_vars=['date'], value_vars=['trust', 'fear', 'sadness',
                                                                'anger', 'surprise', 'disgust', 
                                                                'joy', 'anticipation'])
            df2 = pd.melt(df_sub, id_vars=['date'], value_vars=['trust_change', 'fear_change', 'sadness_change',
                                                                'anger_change', 'surprise_change', 'disgust_change', 
                                                                'joy_change', 'anticipation_change'], 
                          value_name='change')
            
            df1 = df1.sort_values(by=['date'])
            df2['variable'] = df2['variable'].str.replace('_change', '')
            new_df = pd.merge(df1, df2,  how='left', left_on=['date','variable'], right_on = ['date','variable'])
            new_df.dropna(axis=0, inplace=True)
            
            df_sub = new_df.sort_values('date')

            return df_sub

        else:

            print('Sorry, not enough posts yet, make it up to 6.')
    except:
        
        print('Sorry, do not see your ID in the ststem.')

test = get_plutchik_data(plutchik, blogger_id='1270648')
    
list_topics = df1['Prime Topic'].unique()

e_list = plutchik.columns[2:]

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
                                              
                                                        
                                              
                                                              
                                              
                                              ])
                                  ]),
                                                         
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
                                             children=[dcc.Dropdown(id='emotionselector', options=get_options(e_list),
                                                              multi=True, value=[],
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
                                                   figure=px.scatter(
                                                                  template='plotly_dark').update_layout(
                                                                      {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
                                            )), 
                                        dcc.Graph(id='change', config={'displayModeBar': False}, 
                                                   animate=True,
                                                   figure=px.scatter(
                                                                  template='plotly_dark').update_layout(
                                                                      {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
                                            ))  
                                     ])
                                  
                                  
                                  
                                  
                                    ])
                                                                      
                                                                      
                                                                     
                       
                                                            ])
                                         


@app.callback(Output('topicmodel', 'figure'),
              [Input('topicselector', 'value'),
               Input("input1", "value")])
def update_graph(selected_checklist_value, input1):
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
    trace_extra = go.Scatter3d(x=df_sub[df_sub['blogger_id'] == input1]['xs'],
                    y=df_sub[df_sub['blogger_id'] == input1]['ys'],
                    z=df_sub[df_sub['blogger_id'] == input1]['zs'],
                    name='ME',
                    mode='markers', 
                    marker = dict(size=20, color='#F23B0A',
                                  line = dict(color = '#6B6B6B', width = 2),
                                  opacity=0.99),
                    text="ME",

                    hovertemplate='<b><i>It is...</i></b>'
)
    trace.append(trace_extra)
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=[ '#81F08B', '#D7F23A', '#CF696C', '#D4D4D4', '#F0CB69', '#69F0D0', '#F26A3A'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'My BLOGGER.COM Community', 'font': {'color': '#545151'}, 'x': 0.5},
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

@app.callback(Output('timeseries', 'figure'),
              [Input('emotionselector', 'value'),
               Input("input1", "value")])
def update_graph1(selected_dropdown_value, input1):
    

    df_sub = get_plutchik_data(plutchik, blogger_id=input1)
    
    trace = []
    
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
                  paper_bgcolor='rgba(0, 0, 0, 255)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'EMOTIONS OF MY POSTS', 'font': {'color': 'white'}, 'x': 0.5},
                  #xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }
    return figure


@app.callback(Output('change', 'figure'),
              [Input('emotionselector', 'value'), 
               Input("input1", "value")])
def update_change(selected_dropdown_value, input1):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    trace1 = []
    
    df_sub = get_plutchik_data(plutchik, blogger_id=input1)
    
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
                  colorway=["#FA1117", '#045C8A', '#0F9406', '#F23D0C', '#BA8B0F', '#A85EF2', '#424141', '#179C9C'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=250,
                  hovermode='x',
                  #hoverlabel=dict(bgcolor='#FD6A37'),
                  autosize=True,
                  title={'text': 'PULSE OF MY BLOG', 'font': {'color': 'white'}, 'x': 0.5},
                  #xaxis={'showticklabels': False, 'range': [df_sub.index.min(), df_sub.index.max()]},
              )
              }

    return figure

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
   app.run_server(debug=False, port=5080)
#






                                        