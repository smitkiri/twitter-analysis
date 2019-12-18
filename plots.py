# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 18:24:24 2019

@author: Smit
"""

import plotly
import plotly.graph_objs as go
import json
from wordcloud import WordCloud

def timeline(tweets):
    dates = tweets.groupby(by='date').count()['text']

    data = [go.Bar(
            x = dates.index,
            y = dates
            )]
    
    layout = go.Layout(title = {'text': 'User Timeline',
                                'y': 0.9,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})
    fig = go.Figure(data = data, layout = layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def source(tweets):
    source = tweets.groupby('source').count()['text'].sort_values(ascending = False)
    
    data = [go.Bar(
        x = source.index,
        y = source
    )]
    
    layout = go.Layout(title = {'text': 'Tweet Sources',
                                'y': 0.9,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})
    fig = go.Figure(data = data, layout = layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def active_week(tweets):
    active = tweets.groupby('day').count()['text']
    active = active.reindex(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
    
    data = [go.Bar(
        x = active.index,
        y = active
    )]
    
    layout = go.Layout(title = {'text': 'Day of Week',
                                'y': 0.9,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})
    fig = go.Figure(data = data, layout = layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def active_hr(tweets):
    time = [x for x in range(24)]
    day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    z = [[tweets[(tweets['day'] == x) & (tweets['time'].apply(lambda x: x.hour) == y)].count()['text'] for y in time] for x in day]
    
    hovertext = list()
    for yi, yy in enumerate(day):
        hovertext.append(list())
        for xi, xx in enumerate(time):
            hovertext[-1].append('Hour: {}<br />Day: {}<br />Tweets: {}'.format(xx, yy, z[yi][xi]))
    
    data = [go.Heatmap(z = z, x = time, y = day, colorscale='Reds', hoverinfo='text', text=hovertext)]
    layout = go.Layout(title = {'text': 'Daily Rhythm',
                                'y': 0.9,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'}, 
                       xaxis = dict(title='Hour', 
                                    tick0 = 0, 
                                    dtick=1, 
                                    ticklen=24, 
                                    tickwidth=1), 
                       yaxis=dict(title='Day'))
    
    fig = go.Figure(data=data, layout=layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def tweet_type(tweets):
    typ = tweets.groupby('type').count()['text'].sort_values()
    
    data = [go.Bar(
            x = typ,
            y = typ.index,
            orientation = 'h')]
    
    layout = go.Layout(title = {'text': 'Types of Tweets',
                                'y': 0.9,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})
    fig = go.Figure(data=data, layout=layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def language(tweets):
    lang = tweets.groupby('language').count()['text'].sort_values()
    
    data = [go.Bar(
            x = lang,
            y = lang.index,
            orientation = 'h')]
    
    layout = go.Layout(title = {'text': 'Language of Tweets',
                                'y': 0.9,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})
    fig = go.Figure(data=data, layout=layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def wordcloud(tweets):
    text = ''
    for tweet in tweets['text']:
        text = text + tweet
    
    text = text.lower()
    clean_text = ''
    
    #removing other users' tags
    for word in text:
        if word[0] != '@':
            clean_text = clean_text + word
    
    whitelist = set('abcdefghijklmnopqrstuvwxyz 0123456789')
    clean_text = ''.join(filter(whitelist.__contains__, clean_text))
    
    wc = WordCloud(width = 512, height = 512, max_words = 100, background_color = "white").generate(clean_text)
    
    word_list=[]
    freq_list=[]
    fontsize_list=[]
    position_list=[]
    orientation_list=[]
    color_list=[]

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)
        
    # get the positions
    x=[]
    y=[]
    for i in position_list:
        x.append(i[0])
        y.append(i[1])
            
    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    
    trace = go.Scatter(x=x, 
                       y=y, 
                       textfont = dict(size=new_freq_list,
                                       color=color_list),
                       hoverinfo='text',
                       hovertext=['{0}'.format(w) for w in word_list],
                       mode='text',  
                       text=word_list
                      )
    
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}},
                       title = {'text': 'Words in Tweets',
                                'y': 0.9,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})
    
    fig = go.Figure(data=[trace], layout=layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def tweet_length(tweets):
    lengths = tweets['text'].apply(lambda x: x.split()).apply(len)
    trace = go.Histogram(x = lengths)
    layout = go.Layout(title = {'text': 'Length of Tweets',
                                'y': 0.9,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'}, 
                       xaxis = {'title': 'Number of words'}, 
                       yaxis = {'title': 'Number of tweets'})
    
    fig = go.Figure(data = [trace], layout = layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

