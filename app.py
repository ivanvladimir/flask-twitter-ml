#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function  # Python 2 users only
from flask import Flask, render_template, request
import json
import config
import argparse
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

app = Flask(__name__)

def predict_dummy(text):
    return (text,0)

@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        q=request.form['querytext']
        tweets=[]
        for tweet in tweepy.Cursor(api.search,
                           q=[q.decode('unicode-escape')],
                           rpp=100,
                           result_type="recent",
                           lang='es').items(100):
                tweets.append(predict_dummy(tweet.text))
        return render_template("result.html",tweets=tweets)
    return render_template("main.html")

if __name__ == '__main__':
    p = argparse.ArgumentParser("Twitter ML")
    p.add_argument("--host",default="127.0.0.1",
            action="store", dest="host",
            help="Root url [127.0.0.1]")
    p.add_argument("--port",default=5000,type=int,
            action="store", dest="port",
            help="Port url [500]")
    p.add_argument("--debug",default=False,
            action="store_true", dest="debug",
            help="Use debug deployment [Flase]")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")

    opts = p.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    app.run(debug=opts.debug,
            host=opts.host,
            port=opts.port)
