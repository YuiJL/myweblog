#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time, hashlib, json
from flask import current_app, request
from bson.objectid import ObjectId
from app import db

def userToCookie(user, max_age=86400):
    
    '''
    return cookie from an user dict
    '''
    
    expire_time = str(max_age + int(time.time()))
    sha1_before = '%s-%s-%s-%s' % (user['_id'], user['password'], expire_time, current_app.config['SECRET_KEY'])
    L = [user['_id'], expire_time, hashlib.sha1(sha1_before.encode('utf-8')).hexdigest()]
    view_cookie = request.cookies.get(current_app.config['COOKIE_NAME'], '').split('+').pop()
    return '-'.join(L) + '+' + view_cookie


def cookieToUser(cookie):
    
    '''
    return an user dict from cookie, find by '_id'
    '''
    
    try:
        L = cookie.split('+')[0].split('-')
        if len(L) != 3:
            return None
        user_id, expire_time, sha1 = L
        # cookie expires
        if time.time() > int(expire_time):
            return None
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return None
        user.update(_id=str(user['_id'])) # must convert the ObjectId to string first
        sha1_test = '%s-%s-%s-%s' % (user['_id'], user['password'], expire_time, current_app.config['SECRET_KEY'])
        if sha1 != hashlib.sha1(sha1_test.encode('utf-8')).hexdigest():
            return None
        user.update(password='******')
        return user
    except Exception as e:
        print(e)
        
        
def viewToCookie(view):
    
    '''return cookie from query string'''
    
    user_cookie = request.cookies.get(current_app.config['COOKIE_NAME'], '').split('+')[0]
    return user_cookie + '+' + view


def cookieToView(cookie):
    
    '''extract view mode from cookie'''
    
    view = cookie.split('+').pop()
    if not view:
        return None
    return view


def validPassword(user, password):
    
    '''
    verify password
    '''
    
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    sha1.update(user['email'].encode('utf-8'))
    sha1.update(b'the-Salt')
    return sha1.hexdigest() == user['password']


def allowedFile(filename):
    
    '''allowed extension for uploaded files'''
    
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


def loginResponse(response, cookie, max_age=86400):
    
    '''
    return a login response with cookie set
    '''
    
    response.set_cookie(current_app.config['COOKIE_NAME'], cookie, max_age, httponly=True)
    return response


def signOutResponse(response):
    
    '''
    return a sign out response with cookie deleted
    '''
    
    cookie = request.cookies.get(current_app.config['COOKIE_NAME']).split('+').pop()
    response.set_cookie(current_app.config['COOKIE_NAME'], '+'+cookie, httponly=True)
    return response