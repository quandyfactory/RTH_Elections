#!/usr/local/bin/python

"""
quandyconfig - configuration file for default values used in the web application
"""

# path defaults for imports
SYSPATH = ['/home/ryan/projects/quandy']


# html defaults
SITE_DOMAIN = 'http://elections.raisethehammer.org'
SITE_NAME   = 'Raise the Hammer Elections'
CSS_PATH    = '/static/styles/'
CSS_FILES   = ['fonts.css', 'style.css']
JS_PATH     = '/static/scripts/'
JS_FILES    = ['jquery.js', 'jquery.tablesorter.js', 'scripts.js']
DOCTYPE     = 'html 4 strict' # quandy default
LANG        = 'en'            # quandy default
CHARSET     = 'UTF-8'         # quandy default
FAVICON_URL = '/static/favicon.ico'
SITE_AUTHOR = 'Ryan McGreal'

#database defaults
SQL_TYPE = 'mysql'
SQL_USERNAME = 'username'
SQL_PASSWORD = 'password'
SQL_SERVER = 'mysql_server'
SQL_SERVER = 'localhost'
SQL_DATABASE = 'database'
SQL_HASH_SALT = 'salt'
DB_CONNECTION = '%s://%s:%s@%s/%s?charset=utf8' % (
    SQL_TYPE, SQL_USERNAME, SQL_PASSWORD, SQL_SERVER, SQL_DATABASE
    )

#default admin email adddress
EMAIL = 'email@mailserver.com'
SMTP = 'smtp.mailserver.com'
MAILBOX_LOGIN = 'username'
MAILBOX_PASSWORD = 'password'
