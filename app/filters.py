#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time
from datetime import datetime

def datetime_filter(t):
    delta = int(time.time() - t)
    if delta == 1:
        return u'a second ago'
    if delta < 60:
        return u'%s seconds ago' % delta
    if delta < 120:
        return u'a minute ago'
    if delta < 3600:
        return u'%s minutes ago' % (delta // 60)
    if delta < 7200:
        return u'an hour ago'
    if delta < 86400:
        return u'%s hours ago' % (delta // 3600)
    if delta < 172800:
        return u'a day ago'
    if delta < 604800:
        return u'%s days ago' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return u'%s %s, %s' % (months[dt.month-1], dt.day, dt.year)