#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import time, os, re

from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from flask import request, redirect, url_for, jsonify, abort, Blueprint, make_response, g, flash, current_app

from app import db
from app.models import User, Blog, Comment
from app.filters import markdown_filter
from app.utilities import allowed_file, cookie_to_user

api = Blueprint('api', __name__, url_prefix='/api')

APIS = ('blogs', 'users', 'comments')


#************************************
#----------------APIs----------------
#************************************

@api.route('/<collection>')
def api_get_all(collection):
    
    '''
    get all documents from a collection
    '''
    
    if collection not in APIS:
        abort(400)
    cursor = db[collection]
    a = []
    for document in cursor.find().sort("created", -1):
        if collection == 'users':
            document.update(password='******')
        document.update(_id=str(document['_id']))
        a.append(document)
    return jsonify({collection:a})


@api.route('/<collection>/<item_id>')
def api_get_one(collection, item_id):
    
    '''
    get a single document from a collection
    '''
    
    document = db[collection].find_one({'_id': ObjectId(item_id)})
    if not document:
        abort(400)
    if collection == 'users':
        document.update(password='******')
    document.update(_id=str(document['_id']))
    return jsonify(document)


@api.route('/blogs/<blog_id>/comments')
def api_get_blog_comments(blog_id):
    
    '''
    get all comments from a blog
    '''
    
    comments = []
    for comment in db.comments.find({'blog_id':blog_id}).sort("created", -1):
        comment.update(_id=str(comment['_id']))
        comment.update(content=markdown_filter(comment['content']))
        if comment.get('subcomment'):
            for subcomment in comment.get('subcontent'):
                subcomment.update(content=markdown_filter(subcomment['content']))
        comments.append(comment)
    return jsonify(comments=comments)


@api.route('/blogs', methods=['POST'])
def api_post_blog():
    
    '''
    post a new blog
    '''
    
    if not g.__user__.get('admin'):
        return make_response('Permission denied.', 403)
    title = request.form.get('title')
    tag = request.form.get('tag').lstrip(r'/\;,. ').rstrip(r'/\;,. ')
    content = request.form.get('content')
    # create a new Blog and save it to mongodb
    blog = Blog(
        user_id = g.__user__.get('_id'),
        user_name = g.__user__.get('name'),
        user_image = g.__user__.get('image'),
        title = title.strip(),
        tag = re.split(r'[\s\;\,\.\\\/]+', tag),
        content = content.lstrip('\n').rstrip()
    )
    blog_resp = blog.__dict__
    return jsonify(blog_id=str(blog_resp['_id']))


@api.route('/blogs/<blog_id>', methods=['POST'])
def api_edit_blog(blog_id):
    
    '''
    edit a blog and post it
    '''
    
    if not g.__user__.get('admin'):
        return make_response('Permission denied.', 403)
    title = request.form.get('title')
    tag = request.form.get('tag').lstrip(r'/\;,. ').rstrip(r'/\;,. ')
    content = request.form.get('content')
    content = content.lstrip('\n').rstrip()
    db.blogs.update_one(
        {'_id': ObjectId(blog_id)},
        {
            '$set': {
                'title': title.strip(),
                'tag': re.split(r'[\s\;\,\.\\\/]+', tag),
                'content': content,
                'summary': '%s%s' % (content[:140], '...'),
                'last_modified': True,
                'modified': int(time.time())
            }
        })
    return jsonify(blog_id=blog_id)
    

@api.route('/blogs/<blog_id>/comments', methods=['POST'])
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
    blog = db.blogs.find_one({'_id': ObjectId(blog_id)})
    comment = Comment(
        blog_id = blog_id,
        blog_author = blog.get('user_name'),
        blog_title = blog.get('title'),
        user_id = g.__user__.get('_id'),
        user_name = g.__user__.get('name'),
        user_image = g.__user__.get('image'),
        content = content
    )
    comments = []
    for document in db.comments.find({'blog_id':blog_id}).sort("created", -1):
        document.update(_id=str(document['_id']))
        document.update(content=markdown_filter(document['content']))
        if document.get('subcomment'):
            for subcomment in document.get('subcontent'):
                subcomment.update(content=markdown_filter(subcomment['content']))
        comments.append(document)
    return jsonify(comments=comments)


@api.route('/blogs/<blog_id>/comments/<comment_id>', methods=['POST'])
def api_pose_subcomment(blog_id, comment_id):
    
    '''
    post a subcomment
    '''
    
    if not g.__user__:
        return make_response('Please login', 403)
    content = request.form.get('content').lstrip('\n').rstrip()
    if not content:
        return make_response('Content cannot be empty', 403)
    comment = db.comments.find_one({'_id': ObjectId(comment_id)})
    db.comments.update_one(
        {'_id': ObjectId(comment_id)},
        {
            '$set': {'subcomment': True},
            '$push': {
                'subcontent': {
                    '_id': str(ObjectId()),
                    'user_id': g.__user__.get('_id'),
                    'user_name': g.__user__.get('name'),
                    'user_image': g.__user__.get('image'),
                    'content': content,
                    'created': int(time.time())
                }
            }
        })
    comments = []
    for document in db.comments.find({'blog_id': blog_id}).sort("created", -1):
        document.update(_id=str(document['_id']))
        document.update(content=markdown_filter(document['content']))
        if document.get('subcomment'):
            for subcomment in document.get('subcontent'):
                subcomment.update(content=markdown_filter(subcomment['content']))
        comments.append(document)
    return jsonify(comments=comments)
    
    
@api.route('/<collection>/<item_id>/delete', methods=['POST'])
def api_delete_one(collection, item_id):
    
    '''
    delete one document from a certain collection
    '''
    
    if not g.__user__.get('admin'):
        return make_response('Permission denied.', 403)
    
    if collection == 'comments':
        blog_id = db.comments.find_one({'_id': ObjectId(item_id)}).get('blog_id')
        
    db[collection].delete_one({'_id': ObjectId(item_id)})
    
    if collection == 'blogs':
        db.comments.delete_many({'blog_id': ObjectId(item_id)})
    if collection == 'comments':
        return redirect(url_for('api.api_get_blog_comments', blog_id=blog_id))
    return jsonify(item_id=item_id)


@api.route('/comments/<comment_id>/delete/<own_id>', methods=['POST'])
def api_delete_subcomment(comment_id, own_id):
    
    '''
    delete a subcomment from a certain comment
    '''
    
    if not g.__user__.get('admin'):
        return make_response('Permission denied.', 403)
    db.comments.update_one(
        {'_id': ObjectId(comment_id)},
        {
            '$pull': {'subcontent': {'_id': own_id}}
        })
    if not db.comments.find_one({'_id': ObjectId(comment_id)}).get('subcontent'):
        db.comments.update_one(
            {'_id': ObjectId(comment_id)},
            {
                '$set': {'subcomment': False}
            })
    blog_id = db.comments.find_one({'_id': ObjectId(comment_id)}).get('blog_id')
    return redirect(url_for('api.api_get_blog_comments', blog_id=blog_id))


@api.route('/image/<user_id>', methods=['POST'])
def api_upload(user_id):
    
    '''
    upload image files for user avatar
    '''
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.referrer)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.referrer)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        # update users
        db.users.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {'image': '/static/img/' + filename}
            })
        
        # update blogs
        db.blogs.update_many(
            {'user_id': user_id},
            {
                '$set': {'user_image': '/static/img/' + filename}
            })
        
        # update comments
        db.comments.update_many(
            {'user_id': user_id},
            {
                '$set': {'user_image': '/static/img/' + filename}
            })
        
        # update subcomments in comments
        for comment in db.comments.find():
            if comment.get('subcomment'):
                for subcomment in comment['subcontent']:
                    # find one match and update one
                    if user_id in subcomment.values():
                        db.comments.update_one(
                            {
                                '_id': comment['_id'],
                                'subcontent': {'$elemMatch': {'_id': subcomment['_id']}}
                            },
                            {
                                '$set': {
                                    'subcontent.$.user_image': '/static/img/' + filename
                                }
                            })
    else:
        flash('File not allowed')
    return redirect(request.referrer)