#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

from flask import Flask, request, redirect, url_for, render_template, jsonify, abort, Blueprint
from app import db
from app.models import User

route = Blueprint('route', __name__)

APIS = ['blogs', 'users', 'comments']

@route.route('/')
def index():
    return render_template('blogs.html', blogs=db.blogs.find())

@route.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['sha1_password']
        user = dict(name=name, email=email, password=password)
        db.users.insert_one(user)
        return redirect(url_for('route.index'))

@route.route('/api/<collection>')
def api_get(collection):
    if collection not in APIS:
        abort(400)
    cursor = db[collection]
    a = []
    for item in cursor.find():
        item['_id'] = str(item['_id'])
        a.append(item)
    return jsonify({collection:a})