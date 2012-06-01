"""
This fabric script automates the creation of a virtual environment and a Django
project. The result will be virtual environtment with the name of the project.
The folder namer where the project code will be placed is specified in
SOURCE_DIRECTORY_NAME, a static root folder will be created and settings.py
will be updated.
"""
try:
    from fabric.api import env
    from fabric.api import run
    from fabric.api import local
    from fabric.context_managers import lcd, prefix
except ImportError, e:
    print 'Python Fabric should be installed to sue this script'

import re
import sys
import os


DIRECTORY_NAME_REGEXP = r'^[a-zA-Z_].[\w_-]+$'
SOURCE_DIRECTORY_NAME = 'src'


PACKAGES_LIST = [
    'Django==1.4',
]

VALID_COMMAND = ['activate_admin', ]
COMMAND = []


def create_virtual_env():
    local('virtualenv --no-site-packages .')


def create_project_directory(name):
    if name is None:
        print 'You should provide project name to use this script'
        sys.exit()
    if not re.match(DIRECTORY_NAME_REGEXP, name):
        print 'Incorrect name, name can contain only numbers, letters, dash ' \
            'and underscore and should start with letter or underscore'
        exit(1)
    else:
        local('mkdir %s' % name)


def install_packages():
    for package in PACKAGES_LIST:
        local('pip install %s' % package)


def create_django_project(name):
    local('mkdir %s' % SOURCE_DIRECTORY_NAME)
    local('mkdir static')
    local('mkdir media')
    local('python ./bin/django-admin.py startproject %s %s' % (name, SOURCE_DIRECTORY_NAME))


def update_settings(name):
    with open(os.path.join(name, SOURCE_DIRECTORY_NAME, name, 'settings.py'), 'r') as base_settings:
        content = base_settings.read().replace('%%%project_name%%%', name)
        with open(os.path.join(name, SOURCE_DIRECTORY_NAME, name, 'settings.py'), 'w') as settings:
            settings.write(content)


def activate_admin(name):
    if 'activate_admin' not in COMMAND:
        return
    # settings.py part
    with open('%s/src/%s/settings.py' % (name, name), 'r') as base_settings:
        content = base_settings.read().replace('# \'django.contrib.admin\',', '\'django.contrib.admin\',')
        content = content.replace('django.db.backends.', 'django.db.backends.sqlite3')
        content = content.replace('\'NAME\': \'\',', '\'NAME\': \'%s.db\',' % name)
        with open(os.path.join(name, SOURCE_DIRECTORY_NAME, name, 'settings.py'), 'w') as settings:
            settings.write(content)

    # urls.py part
    with open('%s/src/%s/urls.py' % (name, name), 'r') as base_settings:
        content = base_settings.read().replace('# from django.contrib import admin', 'from django.contrib import admin')
        content = content.replace('# admin.autodiscover()', 'admin.autodiscover()')
        content = content.replace('# url(r\'^admin/\', include(admin.site.urls)),', 'url(r\'^admin/\', include(admin.site.urls)),')
        with open(os.path.join(name, SOURCE_DIRECTORY_NAME, name, 'urls.py'), 'w') as urls:
            urls.write(content)


def check_args(args):
    if args:
        for arg in args:
            if arg not in VALID_COMMAND:
                print 'Command %s does not exist' % args[0]
                sys.exit()
            COMMAND.append(arg)
            print 'Addictional command: %s' % arg


def start_project(name=None, *args):
    check_args(args)
    create_project_directory(name)
    with lcd(name):
        create_virtual_env()
        ve_activate_prefix = os.path.join(os.getcwd(), name, 'bin', 'activate')
        print ve_activate_prefix
        with prefix('. %s' % ve_activate_prefix):
            install_packages()
            create_django_project(name)
            update_settings(name)
            activate_admin(name)
            manage_py_path = os.path.join(SOURCE_DIRECTORY_NAME, 'manage.py')
            local('python %s collectstatic' % manage_py_path)
