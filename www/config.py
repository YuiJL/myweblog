#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
    COOKIE_NAME = "YuiSession"
    SECRET_KEY = "YuiJLWebLog"
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'app/static/img')
    RECAPTCHA_SITE_KEY = "6LcD7Qc*********************************"
    RECAPTCHA_SECRET_KEY = "6LcD7Qc*********************************"
    
    
class DevConfig(Config):
    
    DEBUG = True