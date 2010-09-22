#!/usr/local/bin/python
# coding: utf-8

__version__ = 1.0
__releasedate__ = '2010-02-16'
__author__ = 'Ryan McGreal <ryan@quandyfactory.com>'
__homepage__ = 'http://quandyfactory.com/projects/28/rth_codebase_redesign'
__repository__ = 'http://github.com/quandyfactory/rth_elections'
__copyright__ = '(C) 2009 by Ryan McGreal. Licenced under GNU GPL 2.0\nhttp://www.gnu.org/licenses/old-licenses/gpl-2.0.html'

import os, sys
sys.path.insert(0, os.path.abspath(__file__).replace('/index.py', ''))
import config as c
sys.path.extend(c.SYSPATH)

import web
web.config.debug = False
import handlers
h = handlers.Handler()
import functions as f

urls = ('/(.*)', 'Handler')

class Handler:
    def GET(self, name):
        output = []
        addline = output.append

        path = name.split('/')

        page, headers = h.get_content(path)
        addline(page)
        for k, v in headers.items():
            web.header(k,v)
        return '\n'.join(output)

    def POST(self, name):

        path = name.split('/')

        output = []
        addline = output.append
        page, headers = h.get_content(path)
        addline(page)
        for k, v in headers.items():
            web.header(k,v)
        return '\n'.join(output)

application = web.application(urls, globals()).wsgifunc()


if __name__ == "__main__":
    application.run()
