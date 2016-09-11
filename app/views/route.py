#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time
from flask import Flask, redirect, url_for, render_template, jsonify, abort, Blueprint
from bson.objectid import ObjectId
from app import db

route = Blueprint('route', __name__)

APIS = ['blogs', 'users', 'comments']

@route.route('/')
def index():
    return render_template('blogs.html', blogs=db.blogs.find())

@route.route('/api/<collection>')
def api_get(collection):
    if collection not in APIS:
        abort(404)
    cursor = db[collection]
    a = []
    for item in cursor.find():
        item['_id'] = str(item['_id'])
        a.append(item)
    return jsonify({collection:a})