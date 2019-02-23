# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 18:46:09 2019

@author: Smit
"""
from flask import Flask, render_template,request,redirect
import plotly

import tweepy
import pandas as pd
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

max_tweets = 500

consumer_key = '...'
consumer_secret = '...'
access_token = '...'
access_token_secret = '...'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
   
api = tweepy.API(auth)


def stats(username):
    
    tweets = pd.DataFrame(columns = ['text', 'source', 'date', 'type', 'language'])
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username).items(max_tweets):
        typ = 'Tweet'
        if tweet.retweeted:
            typ = 'Retweeted'
        elif tweet.is_quote_status:
            typ = 'Quote'
        elif tweet.in_reply_to_screen_name != None:
            typ = 'Reply'
        else:
            typ = 'Tweet'
        tweets = tweets.append(pd.Series([tweet.text, tweet.source, tweet.created_at, typ, tweet.lang], index = tweets.columns), ignore_index=True)
    
    tweets['time'] = tweets['date'].apply(lambda x: x.time())
    tweets['date'] = tweets['date'].apply(lambda x: x.date())
    
    day_of_week = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    tweets['day'] = tweets['date'].apply(lambda x: day_of_week[x.weekday()])
    
    return tweets

def timeline(tweets):
    dates = tweets.groupby(by='date').count()['text']

    data = [go.Bar(
            x = dates.index,
            y = dates
            )]
    
    layout = go.Layout(title = 'User Timeline')
    fig = go.Figure(data = data, layout = layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def source(tweets):
    source = tweets.groupby('source').count()['text'].sort_values(ascending = False)
    
    data = [go.Bar(
        x = source.index,
        y = source
    )]
    
    layout = go.Layout(title = 'Tweet Sources')
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
    
    layout = go.Layout(title = 'Day of week')
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
    layout = go.Layout(title = 'Daily rhythm', xaxis = dict(title='Hour', tick0 = 0, dtick=1, ticklen=24, tickwidth=1), yaxis=dict(title='Day'))
    
    fig = go.Figure(data=data, layout=layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def tweet_type(tweets):
    typ = tweets.groupby('type').count()['text'].sort_values()
    
    data = [go.Bar(
            x = typ,
            y = typ.index,
            orientation = 'h')]
    
    layout = go.Layout(title = 'Types of tweets')
    fig = go.Figure(data=data, layout=layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def language(tweets):
    lang = tweets.groupby('language').count()['text'].sort_values()
    
    data = [go.Bar(
            x = lang,
            y = lang.index,
            orientation = 'h')]
    
    layout = go.Layout(title = 'Language of tweets')
    fig = go.Figure(data=data, layout=layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/<username>')
def userinfo(username):
    tweets = stats(username)
    
    if tweets.shape[0] == 0:
        return render_template('no_tweets.html')
    
    src = source(tweets)
    time = timeline(tweets)
    act_wk = active_week(tweets)
    act_hr = active_hr(tweets)
    typ = tweet_type(tweets)
    lang = language(tweets)
    
    num = tweets.shape[0]
    
    return render_template('userinfo.html',n_tweets = num, source=src, timeline=time, active_week=act_wk, active_hr = act_hr, name=username, tweet_type=typ, language=lang)



@app.route('/')
def index():
    #bar = source('SmitKiri')
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    username = request.args.get('username', '')
    if username[0] == '@':
        username = username[1:]
    try:
        usr = api.get_user(screen_name=username)
    except:
        return render_template('error.html')
    return redirect('/'+username)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)