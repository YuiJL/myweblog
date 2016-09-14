#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time
from flask import Flask, request, g
from pymongo import MongoClient
from app.filters import datetime_filter

COOKIE_NAME = "YuiSession"

client = MongoClient()
db = client.test

from app.utilities import cookieToUser
from app.views.route import route

def loginStatus():
    cookie = request.cookies.get(COOKIE_NAME)
    g.__user__ = cookieToUser(cookie)

def create_app():
    app = Flask(__name__)
    app.jinja_env.filters.update(datetime=datetime_filter)
    app.before_request(loginStatus)
    app.register_blueprint(route)
    return app