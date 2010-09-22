#!/usr/local/bin/python
# coding: utf-8

import os, sys
sys.path.insert(0, os.path.abspath(__file__).replace('/handlers.py', ''))
import config as c
sys.path.extend(c.SYSPATH)
import datetime
import web
import quandy as quandy
html = quandy.Html()
tools = quandy.Tools()
import config as c
import functions as f
import sql as sql
import templates as t
from markdown import markdown
import simplejson as json

class Handler():
    """
    Class for taking the URL path and returning appropriate content.
    """
    def __init__(self):
        pass

    def get_content(self, path):
        """
        Generic method to load the applicable function dynamically, based on the function name.
        """
        H = Handler()
        method = path[0]
        if method == 'get_content':
            method = 'error'
        if method != '':
            # Test if method is actually a method of Handler.
            try:
                func = getattr(H, method)
            except:
                func = getattr(H, 'error')
        else:
            func = getattr(H, 'default')
        output = func(path)
        return output


    def error(self, path):
        """
        Page that loads for a 404 error
        """
        headers = {}
        headers['Content-Type'] = 'text/html; charset=utf-8'

        output = []
        addline = output.append

        contents = []
        title = 'Page Not Found'
        contents.append('<h2>%s</h2>' % title)
        contents.append('<p>Sorry, but the web page you are trying to reach does not seem to exist on this website.</p>')
        contents.append('<p>The website address (URL) is:</p>')
        contents.append('<ul><li><a href="http://elections.raisethehammer.org/%s">http://elections.raisethehammer.org/%s</a></li></ul>' % ('/'.join(path), '/'.join(path)))
        contents.append('<p>You may have followed a broken link from another site or mistyped the URL you are trying to load.</p>')
        contents.append('<p>If you believe this is an error on the site, please <a href="mailto:editor@raisethehammer.org?subject=Broken Link on RTH Elections Page&body=http://elections.raisethehammer.org/%s">send us an email</a> with the details.</p>' % ('/'.join(path)))

        template = t.default
        template = template.replace('[[date]]', f.get_date())
        template = template.replace('[[time]]', f.get_time())
        template = template.replace('[[title]]', title)
        template = template.replace('[[section]]', 'The Hall of Lost Pages')
        template = template.replace('[[description]]', 'The page you are looking for could not be found.')
        template = template.replace('[[content]]', '\n'.join(contents))
        addline(template)

        page = html.write(
            site_domain = c.SITE_DOMAIN,
            site_name = c.SITE_NAME,
            css_path = c.CSS_PATH,
            css_files = c.CSS_FILES,
            js_path = c.JS_PATH,
            js_files = c.JS_FILES,
            page_title = title,
            page_author = 'Ryan McGreal',
            favicon_url = c.FAVICON_URL,
            body_content='\n'.join(output),
            rss = 'http://raisethehammer.org/feeds/articles_blogs/'
            )
        raise web.notfound(page) # make sure page is returned with an HTTP 404 status code
        #return page, headers


    def default(self, path):
        """
        Main Page - redirects to most current election
        """
        headers = {}
        headers['Content-Type'] = 'text/html; charset=utf-8'
        output = []
        addline = output.append

        query = sql.text("""
            select max(election_id) as max_id
            from elections
            limit 1
            """, bind=sql.engine
        )
        rs = query.execute().fetchall()
        if len(rs) > 0:
            raise web.seeother('/election/%s' % (rs[0].max_id))

        raise web.seeother('/elections')


    def elections(self, path):
        """
        List of elections to access
        """
        headers = {}
        headers['Content-Type'] = 'text/html; charset=utf-8'
        output = []
        addline = output.append

        title, content = f.get_elections_page(path)

        addline(content)

        page = html.write(site_domain=c.SITE_DOMAIN, site_name=c.SITE_NAME, css_path=c.CSS_PATH,
            css_files=c.CSS_FILES, js_path=c.JS_PATH, js_files=c.JS_FILES, page_title=title,
            page_author='Ryan McGreal', favicon_url=c.FAVICON_URL, body_content='\n'.join(output),
            rss='http://elections.raisethehammer.org/feeds'
        )

        return page, headers


    def election(self, path):
        """
        Main Page
        """
        headers = {}
        headers['Content-Type'] = 'text/html; charset=utf-8'
        output = []
        addline = output.append

        title, content = f.get_election_page(path)

        addline(content)

        page = html.write(site_domain=c.SITE_DOMAIN, site_name=c.SITE_NAME, css_path=c.CSS_PATH,
            css_files=c.CSS_FILES, js_path=c.JS_PATH, js_files=c.JS_FILES, page_title=title,
            page_author='Ryan McGreal', favicon_url=c.FAVICON_URL, body_content='\n'.join(output),
            rss='http://elections.raisethehammer.org/feeds'
        )

        return page, headers


    def candidate(self, path):
        """
        Main Page
        """
        headers = {}
        headers['Content-Type'] = 'text/html; charset=utf-8'
        output = []
        addline = output.append

        title, content = f.get_candidate_page(path)

        addline(content)

        page = html.write(site_domain=c.SITE_DOMAIN, site_name=c.SITE_NAME, css_path=c.CSS_PATH,
            css_files=c.CSS_FILES, js_path=c.JS_PATH, js_files=c.JS_FILES, page_title=title,
            page_author='Ryan McGreal', favicon_url=c.FAVICON_URL, body_content='\n'.join(output),
            rss='http://elections.raisethehammer.org/feeds'
        )

        return page, headers

    def question(self, path):
        """
        Main Page
        """
        headers = {}
        headers['Content-Type'] = 'text/html; charset=utf-8'
        output = []
        addline = output.append

        title, content = f.get_question_page(path)

        addline(content)

        page = html.write(site_domain=c.SITE_DOMAIN, site_name=c.SITE_NAME, css_path=c.CSS_PATH,
            css_files=c.CSS_FILES, js_path=c.JS_PATH, js_files=c.JS_FILES, page_title=title,
            page_author='Ryan McGreal', favicon_url=c.FAVICON_URL, body_content='\n'.join(output),
            rss='http://elections.raisethehammer.org/feeds'
        )

        return page, headers


    def api(self, path):
        """
        Main Page
        """
        headers = {}
        headers['Content-Type'] = 'application/json; charset=utf-8'
        output = []
        addline = output.append

        output = f.get_api_page(path)

        page = json.dumps(output)

        return page, headers

    def wards(self, path):
        """
        Main Page
        """
        headers = {}
        headers['Content-Type'] = 'text/html; charset=utf-8'
        output = []
        addline = output.append

        title, content = f.get_wards_page(path)

        addline(content)

        page = html.write(site_domain=c.SITE_DOMAIN, site_name=c.SITE_NAME, css_path=c.CSS_PATH,
            css_files=c.CSS_FILES, js_path=c.JS_PATH, js_files=c.JS_FILES, page_title=title,
            page_author='Ryan McGreal', favicon_url=c.FAVICON_URL, body_content='\n'.join(output),
            rss='http://elections.raisethehammer.org/feeds'
        )

        return page, headers

    def apidoc(self, path):
        """
        Main Page
        """
        headers = {}
        headers['Content-Type'] = 'text/html; charset=utf-8'
        output = []
        addline = output.append

        title, content = f.get_apidoc_page(path)

        addline(content)

        page = html.write(site_domain=c.SITE_DOMAIN, site_name=c.SITE_NAME, css_path=c.CSS_PATH,
            css_files=c.CSS_FILES, js_path=c.JS_PATH, js_files=c.JS_FILES, page_title=title,
            page_author='Ryan McGreal', favicon_url=c.FAVICON_URL, body_content='\n'.join(output),
            rss='http://elections.raisethehammer.org/feeds'
        )

        return page, headers
