#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import os

from flask import Flask, request, g

from pymongo import MongoClient

from app.filters import datetime_filter, markdown_filter

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/img')
COOKIE_NAME = "YuiSession"

client = MongoClient()
db = client.test

from app.utilities import cookieToUser
from app.views.route import route
from app.views.api import api

def loginStatus():
    
    '''function to be run before each request'''
    
    cookie = request.cookies.get(COOKIE_NAME, 'nothing')
    g.__user__ = cookieToUser(cookie)

    
def create_app():
    
    '''create this application'''
    
    # create this flask app
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # add filters
    app.jinja_env.filters.update(datetime=datetime_filter, markdown=markdown_filter)
    # add before request functions
    app.before_request(loginStatus)
    # register routes
    app.register_blueprint(route)
    app.register_blueprint(api)
    return app