#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:28:37 2020

@author: elena
"""

#LIBRARIES
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

#DATA IMPORTS
with open('blogger_com_data_19320_tsne3d.pkl', 'rb') as picklefile:
    df1 = pickle.load(picklefile)    
    
with open('../../data/blogger_com_data_330676_plutchik.pkl', 'rb') as picklefile:
    plutchik = pickle.load(picklefile)
    
with open('../../data/blogger_com_data_330676_polarity.pkl', 'rb') as picklefile:
    polarity = pickle.load(picklefile)
    
#FUNCTIONS
def get_polarity_data(df, blogger_id='1270648'):
    
    try:
    
        df_sub = df[df['blogger_id']==blogger_id].sort_values(by='date', ascending = True)

        if df_sub.shape[0] > 5:

            df_sub.drop('blogger_id', axis=1, inplace=True)
            df_sub.set_index('date', inplace=True)

            df_sub['MA_pos'] = df_sub['polarity_pos_posts'].rolling(window=3).mean()
            df_sub['MA_neg'] = df_sub['polarity_neg_post'].rolling(window=3).mean()

            df_sub = df_sub.iloc[2:]
            df_sub = df_sub.reset_index()
            
            df_sub['month'] =   df_sub['date'].dt.month
            
            df_sub['month'] = df_sub['month'].apply(lambda x: calendar.month_abbr[x])

            return df_sub

        else:

            print('Sorry, not enough posts yet, make it up to 6.')
    except:
        
        print('Sorry, do not see your ID in the ststem.')
    
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
        
def get_options(list_topics):
    dict_list = []
    for i in list_topics:
        dict_list.append({'label': i, 'value': i})
    return dict_list

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
 

#SELECTOR DEFINITIONS
list_topics = df1['Prime Topic'].unique()
e_list = plutchik.columns[2:]
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
views = ['Posts: Positivity', 'Posts: Negativity', 'Positivity Trend', 'Negativity Trend']  

#APP DEFINITION
app = dash.Dash(__name__)

#LAYOUT
app.layout = html.Div(
                 children=[
                     html.Div(className='row',
                              children=[
                                  html.Div(className='twelve columns div-user-controls', 
                                      children = [
                                          html.H2('GET BETTER BLOGGING EXPERIENCE: find like-minded bloggers and explore emotional blueprint of your writing'), 
                                          html.Br(),
                                          html.Br(),
                                          dcc.Input(id='input1', type='text', placeholder='Your blogger ID'),
                                          html.Br(),
                                          html.Br(),
                                          html.Div(id="my_community")])]), 
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
                                               html.P('Select one or more key topics.'),
                                               dcc.Checklist(id='topicselector',
                                                             className='topicselector',
                                                             options=get_options(list_topics), 
                                                             value=[df1['Prime Topic'].sort_values()[0]],
                                                             labelStyle={'display': 'block'},
                                                             #style={'backgroundColor': 'darkgray'},
                                                             #labelStyle={'display':'inline-block'}
                                                      ),
                                               
                                               
                                               ]),
                                 html.Div(className='eight columns div-for-charts bg-white',
                                          children=[
                                              dcc.Graph(id='topicmodel',
                                                        config={'displayModeBar': False}, 
                                                        animate=True,
                                                        figure=px.scatter( width=1000, height=800,
                                                          template='plotly_dark').update_layout(
                                                              {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                               'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
                                                              ))
                                              
                                                        
                                              
                                                              
                                              
                                              ])
                                  ]),                       
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
                                         html.H2('MY EMOTIONS'),
                                         html.P('According to a famous psychologist Robert Plutchik there are 8 primary emotions.'),
                                         html.P('Select one or more emotions. Observe the history of expressing these emotions in your blog.'),
                                         html.Div(
                                             className='div-for-dropdown',
                                             children=[dcc.Dropdown(id='emotionselector', options=get_options(e_list),
                                                              multi=True, value=[],
                                                              placeholder='Select emotions',
                                                              #style={'backgroundColor': '#1E1E1E'},
                                                              className='emotionselector', 
                                                              #labelStyle={'display': 'block'},
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
                                        html.Br(),
                                        dcc.Graph(id='change', config={'displayModeBar': False}, 
                                                   animate=True,
                                                   figure=px.scatter(
                                                                  template='plotly_dark').update_layout(
                                                                      {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
                                            ))  
                                     ])
                                  
                                  
                                  
                                  
                                    ]),
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
                                         html.H2('MY UPS and DOWNS'),
                                         html.P('Explore how negative or how positive you go from month to month in your posts.'),
                                         html.P('Find your joyful and moody time of the year.'),
                                         html.Div(
                                             className='div-for-dropdown',
                                             children=[dcc.Dropdown(id='monthselector', options=get_options(months),
                                                              multi=True, value=[],#list(self.volumes["SOURCE"])[0]
                                                              placeholder="Select months",
                                                              style={'backgroundColor': '#1E1E1E'},
                                                              className='monthselector'
                                                              ),
                                             ],
                                             style={'color': '#1E1E1E'})

                                        ]
                                     ),
                                 html.Div(className='eight columns div-for-charts bg-grey',
                                     children=[
                                         dcc.Graph(id='up_down', config={'displayModeBar': False}, 
                                                   animate=True,
                                                   figure=px.violin(
                                                                  template='plotly_dark').update_layout(
                                                                      {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
                                            )) 
                                     ])
                                  
                                  
                                  
                                  
                                    ]),
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

                                         html.H2('MY MOOD PREDICTION'),
                                         html.P('Predict future amount of positivity and negativity in your posts based on past writing.'),
                                         html.P('See if your posts are getting more positive or negative over time.'),
                                         html.P('Plan the best time to write a joyful or an empathic post.'),
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
                                                                          
                                                                     
                       
                                                            ])
                                         
#CALLBACKS
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
                                 text="I am " + df_sub['age'] + 
                                         " and " + df_sub['gender'] +
                                         ". My occupation is " + df_sub['occupation'] +
                                         ". Search me by ID " +
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
                  title={'text': 'MY BLOGGER.COM COMMUNITY', 'font': {'color': 'white'}, 'x': 0.5},
                  #xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
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
        trace.append(go.Scatter(x=df_sub[df_sub['variable'] == emotion]['date'],
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
        trace1.append(go.Scatter(x=df_sub[df_sub['variable'] == emotion]['date'],
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
                  paper_bgcolor='rgba(0, 0, 0, 255)',
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


@app.callback(Output('up_down', 'figure'),
              [Input('monthselector', 'value'),
                Input("input1", "value")])
               
def update_change3(selected_dropdown_value, input1):
    
    polarity1 = get_polarity_data(polarity, blogger_id=input1)
    trace1 = []
    # Draw and append traces for each stock
    for month in selected_dropdown_value:
        trace1.append(go.Violin(x=polarity1['month'][polarity1['month'] == month],
                                y=polarity1['polarity_compound_post'][polarity1['month'] == month],
                                name=month,
                                box_visible=True,
                                meanline_visible=True))

    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
        # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  #colorway=["#FA1117", '#045C8A', '#0F9406', '#F23D0C', '#BA8B0F', '#A85EF2', '#424141', '#179C9C'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 255)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  #margin={'t': 50},
                  height=700,
                  #hovermode='x',
                  #hoverlabel=dict(bgcolor='#FD6A37'),
                  autosize=True,
                  title={'text': 'SEASONAL SWINGS IN MY BLOG', 'font': {'color': 'white'}, 'x': 0.5},
                  #xaxis={'showticklabels': False, 'range': [df_sub.index.min(), df_sub.index.max()]},
              )
              }

    return figure

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
                      paper_bgcolor='rgba(0, 0, 0, 255)',
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      #margin={'t': 10, 'b': 50, 'l':10, 'r':0}, 
                      height=700,
                      autosize=True,
                      title={'text': 'MOOD TRENDS OF MY BLOG', 'font': {'color': 'white'}, 'x': 0.5},
                      #height=400,
                     # width=1000
                      )
    
 
    return fig

#RUN THE APP
if __name__ == '__main__':
   app.run_server(debug=False, port=5081)
#






                                        