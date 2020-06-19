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
import retrying

import calendar
from fbprophet import Prophet

import plotly.graph_objects as go
from dash.dependencies import Input, Output


def get_polarity_data2(df, blogger_id='4162441'):
    print(df.head())
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
    
    try:
    
        #print(df.head())
        
        df_profet = df.iloc[:,n_col].reset_index()
        df_profet.rename(columns={'date':'ds', df_profet.columns[1]:'y'}, inplace=True)
        
        model = Prophet()
        model.fit(df_profet);
        
        future = model.make_future_dataframe(periods=int(np.floor(df.shape[0]*0.2)))
        forecast = model.predict(future)
        return model, forecast
        
    except:
        print('This is a fix for cold start.')
        

def get_options(list_topics):
    dict_list = []
    for i in list_topics:
        dict_list.append({'label': i, 'value': i})
    return dict_list

with open('../../data/blogger_com_data_330676_polarity.pkl', 'rb') as picklefile:
    polarity = pickle.load(picklefile)
    
views = ['Posts: Positivity', 'Posts: Negativity', 'Positivity Trend', 'Negativity Trend']  
 
app = dash.Dash(__name__)

input1='1270648'

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
                                                          multi=True, 
                                                          value=[],
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
              [ Input('viewselector', 'value'),
                Input("input1", "value")])
               
def update_change4(viewselector, input1):
    
    df = get_polarity_data2(polarity, blogger_id=input1)
    

    neg_model, neg_forecast = fb_profet(df, n_col=0)
    pos_model, pos_forecast = fb_profet(df, n_col=1)

    
    fig = go.Figure()
    
    if 'Posts: Positivity' in viewselector:
        
        fig.add_trace(go.Scatter(x=pos_model.history['ds'].dt.to_pydatetime(), y=pos_model.history['y'],
                            mode='markers',
                            opacity=0.8,
                            #color='#BCE0BE',
                            marker = dict(size=5, color='#BCE0BE'),
                            name='Post Positivity'))
        
    if 'Posts: Negativity' in viewselector:
        
        fig.add_trace(go.Scatter(x=neg_model.history['ds'].dt.to_pydatetime(), y=neg_model.history['y'],
                            mode='markers',
                            #color='#FCB6B7',
                            marker = dict(size=5, color='#FCB6B7'),
                            opacity=0.8,
                            name='Post Negativity'))
    
    if 'Positivity Trend' in viewselector:
        
        fig.add_trace(go.Scatter(
            x=pos_forecast['ds'],
            y=pos_forecast['yhat_lower']+pos_forecast['yhat_upper'],
            fill='toself',
            fillcolor='#BCE0BE',
            line_color='#026105',
            name='Positivity Trend',
            showlegend=False,
        ))
    
    if 'Negativity Trend' in viewselector:
        
        fig.add_trace(go.Scatter(
            x=neg_forecast['ds'],
            y=neg_forecast['yhat_lower']+neg_forecast['yhat_upper'],
            fill='toself',
            fillcolor='#FCB6B7',
            line_color='#590404',
            showlegend=False,
            name='Negativity Trend',
        ))
        
    fig.update_layout(template='plotly_dark', 
                      #paper_bgcolor='rgba(0, 0, 0, 0)',
                      #plot_bgcolor='rgba(0, 0, 0, 0)',
                      margin={'t': 10, 'b': 50, 'l':10, 'r':10}, 
                      height=400,
                      width=800)
    
 
    return fig

if __name__ == '__main__':
   app.run_server(debug=False, port=4444)