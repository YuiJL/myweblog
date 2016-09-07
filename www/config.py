#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

# default database config
db_config = {
    'user': 'www',
    'password': 'www',
    'db': 'test'
}

# default jinja2 config
jinja2_config = dict()

# default cookie config
COOKIE_NAME = 'BlogSession'
COOKIE_KEY = 'WeBblog'

__all__ = ['db_config', 'jinja2_config', 'COOKIE_NAME', 'COOKIE_KEY']