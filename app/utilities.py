#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

COOKIE_NAME = "YuiSession"
SECRET_KEY = "YuiJLWebLog"

import time, hashlib, json

from app import db

def userToCookie(user, max_age=86400):
    expire_time = str(max_age + int(time.time()))
    sha1_before = '%s-%s-%s-%s' % (user['name'], user['password'], expire_time, SECRET_KEY) # cookie key will be configured later
    L = [user['name'], expire_time, hashlib.sha1(sha1_before.encode('utf-8')).hexdigest()]
    return '-'.join(L)

def cookieToUser(cookie):
    try:
        L = cookie.split('-')
        if len(L) != 3:
            return None
        name, expire_time, sha1 = L
        # cookie expires
        if time.time() > int(expire_time):
            return None
        user = db.users.find_one({'name': name})
        if not user:
            return None
        sha1_test = '%s-%s-%s-%s' % (user['name'], user['password'], expire_time, SECRET_KEY)
        if sha1 != hashlib.sha1(sha1_test.encode('utf-8')).hexdigest():
            return None
        user.update(password='******')
        user.update(_id=str(user['_id']))
        return user
    except Exception as e:
        print(e)
        
def validPassword(user, password):
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    sha1.update(user['email'].encode('utf-8'))
    sha1.update(b'the-Salt')
    return sha1.hexdigest() == user['password']

def signInResponse(response, cookie, max_age=86400):
    response.set_cookie(COOKIE_NAME, cookie, max_age, httponly=True) # cookie name will be configured later
    return response

def signOutResponse(response):
    response.set_cookie(COOKIE_NAME, 'deleted', httponly=True)
    return response