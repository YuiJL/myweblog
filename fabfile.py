import os, re

from datetime import datetime

from fabric.api import *

env.user = 'ubuntu'
env.sudo_user = 'root'
env.hosts = ['52.52.105.121']
env.key_filename = ['~/.ssh/YUIAWS.pem']

_TAR_FILE = 'dist-myweblog.tar.gz'

_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '~/srv/myweblog'

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