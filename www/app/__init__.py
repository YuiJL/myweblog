#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import os

from flask import Flask, request, g, current_app
from pymongo import MongoClient
from app.filters import datetime_filter, markdown_filter

client = MongoClient()
db = client.test

from app.utilities import cookie_to_user, cookie_to_view
from app.views.route import route
from app.views.api import api

def sign_in_status():
    
    '''sign in status before each request'''
    
    cookie = request.cookies.get(current_app.config['COOKIE_NAME'], 'nothing')
    g.__user__ = cookie_to_user(cookie)

def view_status():
    
    '''view mode status before each request'''
    
    cookie = request.cookies.get(current_app.config['COOKIE_NAME'], 'nothing')
    g.__view__ = cookie_to_view(cookie)
    
def create_app():
    
    '''create this application'''
    
    # create this flask app
    app = Flask(__name__)
    # configuration
    app.config.from_object('config.DevConfig')
    # add filters
    app.jinja_env.filters.update(datetime=datetime_filter, markdown=markdown_filter)
    # add before request functions
    app.before_request(sign_in_status)
    app.before_request(view_status)
    # register routes
    app.register_blueprint(route)
    app.register_blueprint(api)
    return app