#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 07:39:12 2020

@author: elena
"""

import numpy as np
import pandas as pd
import pickle
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

import calendar
from fbprophet import Prophet

import plotly.graph_objects as go
from dash.dependencies import Input, Output


def get_polarity_data2(df, blogger_id='4162441'):
    
    try:
    
        df_sub = df[df['blogger_id']==blogger_id].sort_values(by='date', ascending = True)

        if df_sub.shape[0] > 5:

            df_sub.drop('blogger_id', axis=1, inplace=True)
            df_sub.set_index('date', inplace=True)

            df_sub['MA_pos'] = df_sub['polarity_pos_posts'].rolling(window=3).mean()
            df_sub['MA_neg'] = df_sub['polarity_neg_post'].rolling(window=3).mean()

            df_sub = df_sub.iloc[2:]

            return df_sub

        else:

            print('Sorry, not enough posts yet, make it up to 6.')
    except:
        
        print('Sorry, do not see your ID in the ststem.')


def fb_profet(df, n_col=2):
    
    df_profet = df.iloc[:,n_col].reset_index()
    df_profet.rename(columns={'date':'ds', df_profet.columns[1]:'y'}, inplace=True)
    
    model = Prophet()
    model.fit(df_profet);
    
    future = model.make_future_dataframe(periods=int(np.floor(df.shape[0]*0.2)))
    forecast = model.predict(future)
    
    return model, forecast

def get_options(list_topics):
    dict_list = []
    for i in list_topics:
        dict_list.append({'label': i, 'value': i})
    return dict_list

with open('../../data/blogger_com_data_330676_polarity.pkl', 'rb') as picklefile:
    polarity = pickle.load(picklefile)
    
views = ['trace1', 'trace2', 'trace3', 'trace4']#['Positive', 'Negative', 'Positive Trend', 'Negative Trend']    
app = dash.Dash(__name__)

# Layout

app.layout = html.Div(
                 children=[
                     html.Div(className='row',
                              children=[
                                  html.Div(className='twelve columns div-user-controls', 
                                      children = [
                                          html.H2('GET BETTER BLOGGING EXPERIENCE: learn about emotions you express and people alike around you'), 
                                          html.Br(),
                                          html.Br(),
                                          dcc.Input(id='input1', type='text', placeholder='Your blogger ID'),
                                          html.Br(),
                                          html.Br(),
                                          html.Div(id="my_community")])]), 
   
                     html.Br(),
                     html.Br(),
                     html.Br(),
                     html.Br(),
 
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
                                     html.H2('MY UPS AND DOWNS'),
                                     html.P('Predicting my positivity and negativity.'),
                                     html.P('Select your view.'),
                                     html.Div(
                                         className='div-for-dropdown',
                                         children=[dcc.Dropdown(id='viewselector', options=get_options(views),
                                                          multi=True, value=views[0],#list(self.volumes["SOURCE"])[0]
                                                          placeholder="Select view",
                                                          style={'backgroundColor': '#1E1E1E'},
                                                          className='viewselector'
                                                          ),
                                         ],
                                         style={'color': '#1E1E1E'})

                                    ]
                                 ),
                             html.Div(className='eight columns div-for-charts bg-grey',
                                 children=[
                                     dcc.Graph(id='up_down2', config={'displayModeBar': False}, 
                                               animate=True,
                                               figure=px.scatter(
                                                              template='plotly_dark').update_layout(
                                                                  {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                                   'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
                                                                 )
                                              ) 
                                          ]   
                                    )
                              
                              
                              
                              
                               ]
                            )
                                                                      
                                                                      
                                                                     
                       
                            ]
                        )

#Callbacks                                                                  
@app.callback(Output('up_down2', 'figure'),
              [Input('viewselector', 'value'),
                Input("input1", "value")])
               
def update_change4(viewselector, input1):
    
    df = get_polarity_data2(polarity, blogger_id=input1)

    neg_model, neg_forecast = fb_profet(df, n_col=0)
    pos_model, pos_forecast = fb_profet(df, n_col=1)
    
    trace1 = go.Scatter(x=pos_model.history['ds'].dt.to_pydatetime(), y=pos_model.history['y'],
                    mode='markers',
                    opacity=0.8,
                    #color='#BCE0BE',
                    marker = dict(size=5, color='#BCE0BE'),
                    name='Positive')
    
    trace2 = go.Scatter(x=neg_model.history['ds'].dt.to_pydatetime(), y=neg_model.history['y'],
                    mode='markers',
                    #color='#FCB6B7',
                    marker = dict(size=5, color='#FCB6B7'),
                    opacity=0.8,
                    name='Negative')
    
    trace3 = go.Scatter(
                    x=pos_forecast['ds'],
                    y=pos_forecast['yhat_lower']+pos_forecast['yhat_upper'],
                    fill='toself',
                    fillcolor='#BCE0BE',
                    line_color='#026105',
                    name='Positive Trend',
                    showlegend=False)
    
    trace4 = go.Scatter(
                    x=neg_forecast['ds'],
                    y=neg_forecast['yhat_lower']+neg_forecast['yhat_upper'],
                    fill='toself',
                    fillcolor='#FCB6B7',
                    line_color='#590404',
                    showlegend=False,
                    name='Negative Trend' )
    # trace.append(trace1)
    # trace.append(trace2)
    # trace.append(trace3)
    # trace.append(trace4)
    
    traces_selected = []
    for trace in viewselector:
             traces_selected.append(trace)

    
 
    traces = [traces_selected]
    data = [val for sublist in traces for val in sublist]
        # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  #colorway=["#FA1117", '#045C8A', '#0F9406', '#F23D0C', '#BA8B0F', '#A85EF2', '#424141', '#179C9C'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 255)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  #height=250,
                  #hovermode='x',
                  #hoverlabel=dict(bgcolor='#FD6A37'),
                  autosize=True,
                  title={'text': 'OVER MONTHS', 'font': {'color': 'white'}, 'x': 0.5},
                  #xaxis={'showticklabels': False, 'range': [df_sub.index.min(), df_sub.index.max()]},
              )
              }

    return figure

if __name__ == '__main__':
   app.run_server(debug=True, port=4445)