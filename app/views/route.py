#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time, hashlib

from flask import Flask, request, redirect, url_for, render_template, jsonify, abort, Blueprint, make_response
from app import db
from app.models import User
from app.utilities import userToCookie, validPassword, signInResponse, signOutResponse

route = Blueprint('route', __name__)

APIS = ('blogs', 'users', 'comments')

@route.route('/')
def index():
    return render_template('blogs.html', blogs=db.blogs.find())

@route.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        users = db.users
        name = request.form['name']
        if users.find_one({'name': name}):
            return make_response('name is taken', 400)
        email = request.form['email']
        if users.find_one({'email': email}):
            return make_response('email is taken', 400)
        password = request.form['sha1_password']
        user = User(name=name, email=email, password=password) # self registration
        user_resp = user.__dict__
        cookie = userToCookie(user_resp)
        user_resp.update(password='******')
        user_resp.update(_id=str(user_resp['_id'])) # because value of key '_id' is a bson ObjectId
        return signInResponse(jsonify(user=user_resp), cookie)

@route.route('/auth', methods=['POST'])
def auth():
    email = request.form['email']
    password = request.form['sha1_password']
    user_resp = db.users.find_one({'email': email})
    # no such user
    if not user_resp:
        return make_response('invalid email', 400)
    # password is wrong
    if not validPassword(user_resp, password):
        return make_response('wrong password', 400)
    cookie = userToCookie(user_resp)
    user_resp.update(password='******')
    user_resp.update(_id=str(user_resp['_id']))
    return signInResponse(jsonify(user=user_resp), cookie)
    
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

@route.route('/signout')
def signout():
    return signOutResponse(redirect(url_for('route.index')))