#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import os, re

from datetime import datetime

from fabric.api import *

env.user = 'ubuntu'
env.sudo_user = 'root'
env.hosts = ['***.***.***.***'] # remote host ip
env.key_filename = ['~/.ssh/***.pem'] # ssh public key

_TAR_FILE = 'dist-myweblog.tar.gz'

_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '~/srv/myweblog'

RE_FILES = re.compile('\r?\n')

def build():
    '''
    build dist package
    '''
    includes = ['app', '*.py']
    excludes = ['test', '.*', '*.pyc', '*.pyo', '__pycache__']
    local('rm -f dist/%s' % _TAR_FILE)
    with lcd(os.path.join(os.path.abspath('.'), 'www')):
        cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))
        
        
def deploy():
    '''
    auto deploy script
    '''
    newdir = 'www-%s' % datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    run('rm -f %s' % _REMOTE_TMP_TAR)
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s %s www' % newdir)
        sudo('chown www-data:www-data www')
        sudo('chown -R www-data:www-data %s' % newdir)
    with settings(warn_only=True):
        sudo('supervisorctl stop myweblog')
        sudo('supervisorctl start myweblog')
        sudo('/etc/init.d/nginx reload')
        
        
def rollback():
    '''
    rollback to previous version
    '''
    with cd(_REMOTE_BASE_DIR):
        r = run('ls -p -1')
        files = [s[:-1] for s in RE_FILES.split(r) if s.startswith('www-') and s.endswith('/')]
        files.sort(cmp=lambda s1, s2: 1 if s1 < s2 else -1) # cmp for Python2
        r = run('ls -l www')
        ss = r.split(' -> ')
        if len(ss) != 2:
            print("ERROR: 'www' is not a symbol link.")
            return
        current = ss[1]
        print("Found current symbol link points to: %s\n" % current)
        try:
            index = files.index(current)
        except ValueError as e:
            print("ERROR: symbol link is invalid.")
            return
        if len(files) == index + 1:
            print("ERROR: already the oldest version.")
        old = files[index + 1]
        print ("==================================================")
        for f in files:
            if f == current:
                print ("      Current ---> %s" % current)
            elif f == old:
                print ("  Rollback to ---> %s" % old)
            else:
                print ("                   %s" % f)
        print ("==================================================")
        print ('')
        yn = raw_input("continue? y/N ")
        if yn != 'y' and yn != 'Y':
            print ('Rollback cancelled.')
            return
        print ('Start rollback...')
        sudo('rm -f www')
        sudo('ln -s %s www' % old)
        sudo('chown www-data:www-data www')
        with settings(warn_only=True):
            sudo('supervisorctl stop awesome')
            sudo('supervisorctl start awesome')
            sudo('/etc/init.d/nginx reload')
        print('ROLLBACKED OK.')