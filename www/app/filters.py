#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time
from datetime import datetime

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def datetime_filter(t, mode):
    
    '''custom datetime filter for jinja2 templates'''
    
    if mode == 'summary':
        delta = int(time.time() - t)
        if delta <= 1:
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
    return dt.strftime('%b/%d/%Y, %I:%M:%S %p')


class HighlightRenderer(mistune.Renderer):
    
    '''
    custom renderer for mistune markdown parser
    '''
    
    def block_code(self, code, lang):
        guess = 'python3'
        
        if code.lstrip().startswith('#include'):
            guess = 'c++'
        elif code.lstrip().startswith('<'):
            guess = 'html'
        elif code.lstrip().startswith(('function', 'var', '$')):
            guess = 'javascript'
            
        lexer = get_lexer_by_name(lang or guess, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)
    
    
renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer, hard_wrap=True)

def markdown_filter(text):
    return markdown(text)