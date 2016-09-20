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
        self.admin = False
        self.image = kw.get('image', '/static/img/default.png')
        self.register()
    
    def register(self):
        sha1_password = self.password + self.email + 'the-Salt' # secondary encryption
        self.password = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
        db.users.insert_one(self.__dict__) # save to mongodb


class Blog(object):
    
    def __init__(self, **kw):
        self.user_id = kw.get('user_id')
        self.user_name = kw.get('user_name')
        self.user_image = kw.get('user_image')
        self.title = kw.get('title')
        self.tag = kw.get('tag', [])
        self.content = kw.get('content')
        self.summary = '%s%s' % (kw.get('content', '')[:140], '...')
        self.created = kw.get('created', int(time.time()))
        self.last_modified = False
        db.blogs.insert_one(self.__dict__) # save to mongodb


class Comment(object):
    
    def __init__(self, **kw):
        self.blog_id = kw.get('blog_id')
        self.blog_author = kw.get('blog_author')
        self.blog_title = kw.get('blog_title')
        self.user_id = kw.get('user_id')
        self.user_name = kw.get('user_name')
        self.user_image = kw.get('user_image')
        self.content = kw.get('content')
        self.created = kw.get('created', int(time.time()))
        self.subcomment = False
        db.comments.insert_one(self.__dict__) # save to mongodb