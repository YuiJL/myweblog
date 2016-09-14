#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time, hashlib

from flask import current_app

from app import db

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
        db.users.insert_one(self.__dict__)
        
class Blog(object):
    
    def __init__(self, **kw):
        pass
    
class Comment(object):
    
    def __init__(self, **kw):
        pass