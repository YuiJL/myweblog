#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import asyncio, os, inspect, logging, functools

from aiohttp import web

from errors import APIError

def get(path):
    '''
    Define decorator @get('/path')
    '''  
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

def post(path):
    '''
    Define decorator @post('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

class RequestHandler(object):
    
    def __init__(self, func):
        self._func = func
        
    async def __call__(self, request):
        required_args = inspect.signature(self._func).parameters
        logging.info('required args: %s' % required_args)
        
        kw = {arg: value for arg, value in request.__data__.items() if arg in required_args}
        kw.update(dict(**request.match_info))
        if 'request' in required_args:
            kw['request'] = request
            
        # inspect arguments
        for key, arg in required_args.items():
            if key == 'request' and arg.kind in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD):
                return web.HTTPBadRequest(text='Request parameter cannot be the var argument.')
            if arg.kind not in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD):
                if arg.default == arg.empty and arg.name not in kw:
                    return web.HTTPBadRequest(text='Missing argument: %s' % arg.name)
                
        logging.info('call with args: %s' % kw)
        try:
            return await self._func(**kw)
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)
        
def add_static(app):
    path = os.path.join(os.path.dirname(__path__[0]), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))
    
def add_routes(app, module_name):
    try:
        mod = __import__(module_name, fromlist=['get_submodule'])
    except ImportError as e:
        raise e
        
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        func = getattr(mod, attr)
        if callable(func):
            method = getattr(func, '__method__', None)
            path = getattr(func, '__route__', None)
            if method and path:
                func = asyncio.coroutine(func)
                args = ', '.join(inspect.signature(func).parameters.keys())
                logging.info('add route %s %s => %s(%s)' % (method, path, func.__name__, args))
                app.router.add_route(method, path, RequestHandler(func))