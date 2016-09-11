#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

from flask import Flask
from pymongo import MongoClient
from app.filters import datetime_filter

client = MongoClient()
db = client.test

def create_app():
    app = Flask(__name__)
    app.jinja_env.filters.update(datetime=datetime_filter)
    from app.views.route import route
    app.register_blueprint(route)
    return app