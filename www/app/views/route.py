#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time, math

from bson.objectid import ObjectId
from flask import request, redirect, url_for, render_template, jsonify, abort, Blueprint, make_response, g, flash, current_app

from app import db
from app.models import User
from app.utilities import userToCookie, validPassword, loginResponse, signOutResponse, viewToCookie, checkRecaptcha

route = Blueprint('route', __name__)


#**************************************************************
#----------------Homepage, Blog and Manage Page----------------
#**************************************************************

@route.route('/')
def index():
    
    '''homepage'''
    
    blogs = db.blogs.find().sort("created", -1).limit(10)
    pages = [str(i) for i in range(1, math.ceil(db.blogs.count() / 10) + 1)]
    return render_template('blogs.html', blogs=blogs, blogs2=blogs, pages=pages, page='1')


@route.route('/blogs/<page>')
def blogs_by_page(page):
    
    '''show blogs by page'''
    
    blogs = db.blogs.find().sort("created", -1).limit(10).skip(10*(int(page)-1))
    pages = [str(i) for i in range(1, math.ceil(db.blogs.count() / 10) + 1)]
    return render_template('blogs.html', blogs=blogs, blogs2=blogs, pages=pages, page=page)


@route.route('/blog/<blog_id>')
def single_blog(blog_id):
    
    '''blog page'''
    
    blog = db.blogs.find_one({'_id': ObjectId(blog_id)})
    blog.update(_id=str(blog['_id']))
    return render_template('blog.html', blog=blog)


@route.route('/manage')
def manage_default():
    
    '''manage page'''
    
    return redirect(url_for('route.manage_collection', collection='blogs'))


@route.route('/manage/<collection>')
def manage_collection(collection):
    
    ''' manage blogs, users or comments'''
    
    return render_template('manage.html', collection=collection)


@route.route('/manage/blogs/newblog')
@route.route('/manage/blogs/edit')
def post_blog():
    
    '''blog edit page'''
    
    if not g.__user__:
        flash('Not sign in')
        return redirect(url_for('route.index'))
    
    if not g.__user__.get('admin'):
        flash('Not admin')
        return redirect(url_for('route.index'))
                        
    return render_template('edit.html')


#**************************************************************
#----------------Login, Signout, Authentication----------------
#**************************************************************

@route.route('/register', methods=['GET', 'POST'])
def register():
    
    '''
    register a new account, save it to mongodb
    '''
    
    if request.method == 'GET':
        if g.__user__:
            flash('Already sign in')
            return redirect(url_for('route.index'))
        return render_template('register.html', site_key=current_app.config['RECAPTCHA_SITE_KEY'])
    else:
        resp = request.form.get('recaptcha')
        if not checkRecaptcha(current_app.config['RECAPTCHA_SECRET_KEY'], resp):
            return make_response("You're a bot.", 403)
        users = db.users
        name = request.form.get('name')
        if users.find_one({'name': name}):
            return make_response('Username is taken, please try another.', 403)
        email = request.form.get('email')
        if users.find_one({'email': email}):
            return make_response('E-mail is taken, please try another.', 403)
        password = request.form.get('sha1_password')
        user = User(name=name, email=email, password=password) # self registration
        user_resp = user.__dict__ # an user dict
        user_resp.update(_id=str(user_resp['_id'])) # must convert the ObjectId to string first
        cookie = userToCookie(user_resp)
        user_resp.update(password='******')
        return loginResponse(jsonify(user=user_resp), cookie)


@route.route('/auth', methods=['POST'])
def auth():
    
    '''
    authenticate an user, return a login response with cookie (if success)
    '''
    
    email = request.form.get('email')
    password = request.form.get('sha1_password')
    user_resp = db.users.find_one({'email': email})
    # no such user
    if not user_resp:
        return make_response('Invalid email', 403)
    # password is wrong
    if not validPassword(user_resp, password):
        return make_response('Wrong password', 403)
    user_resp.update(_id=str(user_resp['_id']))
    cookie = userToCookie(user_resp) # must convert the ObjectId to string first
    user_resp.update(password='******')
    return loginResponse(jsonify(user=user_resp), cookie)
    
    
@route.route('/signout')
def signout():
    
    '''return a sign out response'''
    
    return signOutResponse(redirect(request.referrer or url_for('route.index')))


@route.route('/', methods=['POST'])
def view_mode():
    
    '''return a response with view mode cookie set'''
    
    view_mode = request.args.get('view')
    cookie = viewToCookie(view_mode)
    response = jsonify(view=view_mode)
    response.set_cookie(current_app.config['COOKIE_NAME'], cookie, max_age=86400, httponly=True)
    return response