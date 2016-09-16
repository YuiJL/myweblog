#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time

from bson.objectid import ObjectId
from flask import request, redirect, url_for, render_template, jsonify, abort, Blueprint, make_response, g

from app import db
from app.models import User, Blog, Comment
from app.utilities import userToCookie, validPassword, loginResponse, signOutResponse

route = Blueprint('route', __name__)

APIS = ('blogs', 'users', 'comments')


#**************************************************************
#----------------Homepage, Blog and Manage Page----------------
#**************************************************************

@route.route('/')
def index():
    
    '''homepage'''
    
    return render_template('blogs.html', blogs=db.blogs.find())


@route.route('/blog/<blog_id>')
def single_blog(blog_id):
    
    '''blog page'''
    
    blog = db.blogs.find_one({'_id': ObjectId(blog_id)})
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
    
    if not g.__user__.get('admin'):
        abort(403)
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
        return render_template('register.html')
    else:
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
    
    return signOutResponse(redirect(url_for('route.index')))


#************************************
#----------------APIs----------------
#************************************

@route.route('/api/<collection>')
def api_get_all(collection):
    
    '''
    get all documents from a collection
    '''
    
    if collection not in APIS:
        abort(400)
    cursor = db[collection]
    a = []
    for document in cursor.find():
        if collection == 'users':
            document.update(password='******')
        document.update(_id=str(document['_id']))
        a.append(document)
    return jsonify({collection:a})


@route.route('/api/<collection>/<item_id>')
def api_get_one(collection, item_id):
    
    '''
    get one document from a collection
    '''
    
    document = db[collection].find_one({'_id': ObjectId(item_id)})
    if not document:
        abort(400)
    if collection == 'users':
        document.update(password='******')
    document.update(_id=str(document['_id']))
    return jsonify(document)


@route.route('/api/blogs/<blog_id>/comments')
def api_get_blog_comments(blog_id):
    
    '''
    get all comments from a blog
    '''
    
    comments = []
    for comment in db.comments.find({'blog_id':blog_id}).sort("created", -1):
        comment.update(_id=str(comment['_id']))
        comments.append(comment)
    return jsonify(comments=comments)


@route.route('/api/blogs', methods=['POST'])
def api_post_blog():
    
    '''
    post a new blog
    '''
    
    if not g.__user__.get('admin'):
        return make_response('Permission denied.', 403)
    title = request.form.get('title')
    tag = request.form.get('tag')
    content = request.form.get('content')
    # create a new Blog and save it to mongodb
    blog = Blog(
        user_id = g.__user__.get('_id'),
        user_name = g.__user__.get('name'),
        user_image = g.__user__.get('image'),
        title = title.strip(),
        tag = tag.split(),
        content = content.lstrip('\n').rstrip()
    )
    blog_resp = blog.__dict__
    return jsonify(blog_id=str(blog_resp['_id']))


@route.route('/api/blogs/<blog_id>', methods=['POST'])
def api_edit_blog(blog_id):
    
    '''
    edit a blog and post it
    '''
    
    if not g.__user__.get('admin'):
        return make_response('Permission denied.', 403)
    title = request.form.get('title')
    tag = request.form.get('tag')
    content = request.form.get('content')
    db.blogs.update_one(
        {'_id': ObjectId(blog_id)},
        {
            '$set': {
                'title': title.strip(),
                'tag': tag.split(),
                'content': content.lstrip('\n').rstrip(),
                'last_modified': True,
                'modified': int(time.time())
            }
        })
    return jsonify(blog_id=blog_id)
    

@route.route('/api/blogs/<blog_id>/comments', methods=['POST'])
def api_post_and_get_comment(blog_id):
    
    '''
    post a new comment
    '''
    
    if not g.__user__:
        return make_response('Please login', 403)
    content = request.form.get('content').lstrip('\n').rstrip()
    if not content:
        return make_response('Content cannot be empty.')
    # create a new Comment and save it to mongodb
    comment = Comment(
        blog_id = blog_id,
        user_id = g.__user__.get('_id'),
        user_email = g.__user__.get('name'),
        user_image = g.__user__.get('image'),
        content = content
    )
    comments = []
    for document in db.comments.find({'blog_id':blog_id}).sort("created", -1):
        document.update(_id=str(document['_id']))
        comments.append(document)
    return jsonify(comments=comments)


@route.route('/api/blogs/<blog_id>/comments/<comment_id>', methods=['POST'])
def api_pose_subcomment(blog_id, comment_id):
    
    '''
    post a subcomment
    '''
    
    if not g.__user__:
        return make_response('Please login', 403)
    content = request.form.get('content').lstrip('\n').rstrip()
    if not content:
        return make_response('Content cannot be empty')
    comment = db.comments.find_one({'_id': ObjectId(comment_id)})
    db.comments.update_one(
        {'_id': ObjectId(comment_id)},
        {
            '$set': {'subcomment': True},
            '$push': {
                'subcontent': {
                    'user_id': g.__user__.get('_id'),
                    'user_name': g.__user__.get('name'),
                    'user_email': g.__user__.get('email'),
                    'user_image': g.__user__.get('image'),
                    'content': content,
                    'created': int(time.time())
                }
            }
        })
    return jsonify(comment_id=comment_id)
    
    
@route.route('/api/<collection>/<item_id>/delete', methods=['POST'])
def api_delete_one(collection, item_id):
    
    '''
    delete one document from a certain collection
    '''
    
    if not g.__user__.get('admin'):
        return make_response('Permission denied.', 403)
    db[collection].delete_one({'_id': ObjectId(item_id)})
    if collection == 'blogs':
        db.comments.delete_many({'blog_id': ObjectId(item_id)})
    return jsonify(item_id=item_id)