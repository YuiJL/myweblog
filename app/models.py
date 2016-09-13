#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time, hashlib

from flask import current_app

from app import db

COOKIE_NAME = "YuiSession"
SECRET_KEY = "YuiJLWebLog"

class User(object):
    
    def __init__(self, **kw):
        self.name = kw.get('name')
        self.email = kw.get('email')
        self.password = kw.get('password')
        self.created = kw.get('created', int(time.time()))
        self.admin = kw.get('admin', False)
        self.image = kw.get('image', '/static/img/default.png')
        self.register()
    
    def register(self):
        sha1_password = self.password + self.email + 'the-Salt'
        self.password = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
        user = self.__dict__
        db.users.insert_one(user)
        
    def signInResponse(self, resp, max_age=86400):
        expire_time = str(max_age + int(time.time()))
        sha1_before = '%s-%s-%s-%s' % (self.name, self.password, expire_time, SECRET_KEY) # cookie key will be adjusted later
        L = [self.name, expire_time, hashlib.sha1(sha1_before.encode('utf-8')).hexdigest()]
        resp.set_cookie(COOKIE_NAME, '-'.join(L), max_age, httponly=True)
        return resp
        
class Blog(object):
    
    def __init__(self, **kw):
        pass
    
class Comment(object):
    
    def __init__(self, **kw):
        pass