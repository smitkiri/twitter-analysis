# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 18:46:09 2019

@author: Smit
"""
from flask import Flask, render_template,request,redirect

import tweepy
import pandas as pd
import os
import plots

app = Flask(__name__)

max_tweets = 500

consumer_key = os.getenv('twitter_consumer_key')
consumer_secret = os.getenv('twitter_consumer_secret')
access_token = os.getenv('twitter_access_token')
access_token_secret = os.getenv('twitter_access_token_secret')

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


@app.route('/<username>')
def userinfo(username):
    tweets = stats(username)
    
    if tweets.shape[0] == 0:
        return render_template('no_tweets.html')
    
    src = plots.source(tweets)
    time = plots.timeline(tweets)
    act_wk = plots.active_week(tweets)
    act_hr = plots.active_hr(tweets)
    typ = plots.tweet_type(tweets)
    lang = plots.language(tweets)
    
    wc = plots.wordcloud(tweets)
    twt_len = plots.tweet_length(tweets)
    
    num = tweets.shape[0]
    
    return render_template('userinfo.html',n_tweets = num, 
                           source=src, 
                           timeline=time, 
                           active_week=act_wk, 
                           active_hr = act_hr, 
                           name=username, 
                           tweet_type=typ, 
                           language=lang,
                           wordcloud = wc,
                           tweet_length = twt_len)


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
    