#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

from flask import Flask, request, redirect, url_for, render_template, jsonify, abort, Blueprint, make_response
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
        users = db.users
        name = request.form['name']
        if (users.find_one({'name': name})):
            resp = make_response('name is taken', 400)
            return resp
        email = request.form['email']
        if (users.find_one({'email': email})):
            resp = make_response('email is taken', 400)
            return resp
        password = request.form['sha1_password']
        user = User(name=name, email=email, password=password)
        user_resp = user.__dict__
        user_resp['password'] = '******'
        user_resp.update(_id=str(user_resp['_id'])) # because '_id' in a user is not a string
        return user.signInResponse(jsonify(user=user_resp))

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