#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time, hashlib
from flask import Flask, request, redirect, url_for, render_template, jsonify, abort, Blueprint, make_response
from app import db
from app.models import User

route = Blueprint('route', __name__)

APIS = ('blogs', 'users', 'comments')
COOKIE_NAME = "YuiSession"
SECRET_KEY = "YuiJLWebLog"

def userToCookie(user, max_age=86400):
    expire_time = str(max_age + int(time.time()))
    sha1_before = '%s-%s-%s-%s' % (user['name'], user['password'], expire_time, SECRET_KEY) # cookie key will be configured later
    L = [user['name'], expire_time, hashlib.sha1(sha1_before.encode('utf-8')).hexdigest()]
    return '-'.join(L)

def signInResponse(response, cookie, max_age=86400):
    response.set_cookie(COOKIE_NAME, cookie, max_age, httponly=True) # cookie name will be configured later
    return response

def validPassword(user, password):
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    sha1.update(user['email'].encode('utf-8'))
    sha1.update(b'the-Salt')
    return sha1.hexdigest() == user['password']

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