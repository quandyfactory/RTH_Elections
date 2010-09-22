#!/usr/local/bin/python
# coding: utf-8

import os, sys
sys.path.insert(0, os.path.abspath(__file__).replace(__file__, ''))
import config as c
sys.path.extend(c.SYSPATH)

from sqlalchemy import *
from sqlalchemy import exceptions
import config as c

engine = create_engine(c.DB_CONNECTION,
    pool_size = 100,
    pool_recycle=7200,
    )
metadata = MetaData(bind=engine)

articles = Table('articles', metadata,
    Column('id', Integer, primary_key=True),
    Column('auth_id', Integer, nullable=True),
    Column('title', Unicode(255), nullable=True),
    Column('section', Unicode(255), nullable=True),
    Column('description', Unicode(1000), nullable=True),
    Column('date_issued', Unicode(10), nullable=True),
    Column('content', UnicodeText, nullable=True),
    Column('lede', Integer, nullable=True),
    Column('print', Integer, nullable=True),
    Column('page_order', Integer, nullable=True),
    )

authors = Table('authors', metadata,
    Column('auth_id', Integer, primary_key=True),
    Column('auth_name', Unicode(255), nullable=True),
    Column('auth_email', Unicode(255), nullable=True),
    Column('auth_bio', Unicode(1000), nullable=True),
    Column('username', Unicode(40), nullable=True),
    )

blog = Table('blog', metadata,
    Column('blog_id', Integer, primary_key=True),
    Column('auth_id', Integer, nullable=True),
    Column('title', Unicode(255), nullable=True),
    Column('section', Unicode(255), nullable=True),
    Column('date_issued', Unicode(10), nullable=True),
    Column('content', UnicodeText, nullable=True),
    )

comments = Table('comments', metadata,
    Column('comment_id', Integer, primary_key=True),
    Column('parent_id', Integer, nullable=True),
    Column('orig_id', Integer, nullable=True),
    Column('doctype', Unicode(255), nullable=True),
    Column('username', Unicode(255), nullable=True),
    Column('date_posted', DateTime, nullable=True),
    Column('comment', UnicodeText, nullable=True),
    Column('spamflag', Integer, nullable=True),
    )

comment_edits = Table('comment_edits', metadata,
    Column('edit_id', Integer, primary_key=True),
    Column('comment_id', Integer, nullable=True),
    Column('username', Unicode(255), nullable=True),
    Column('timestamp', DateTime, nullable=True),
    )

comment_votes = Table('comment_votes', metadata,
    Column('vote_id', Integer, primary_key=True),
    Column('username', Unicode(255), nullable=True),
    Column('vote', Integer, nullable=True),
    Column('comment_id', Integer, nullable=True),
    )

quotes = Table('quotes', metadata,
    Column('quote_id', Integer, primary_key=True),
    Column('quote_text', Unicode(1000), nullable=True),
    Column('quote_attribution', Unicode(255), nullable=True),
    Column('date_issued', Unicode(10), nullable=True),
    )

sections = Table('sections', metadata,
    Column('section_id', Integer, primary_key=True),
    Column('section', Unicode(255), nullable=True),
    Column('banner', Unicode(255), nullable=True),
    )

spamwords = Table('spamwords', metadata,
    Column('spamword', Unicode(100), nullable=True),
    )

traffic = Table('traffic', metadata,
    Column('traffic_id', Integer, primary_key=True),
    Column('date_time', DateTime, nullable=True),
    Column('url', Unicode(255), nullable=True),
    Column('query_string', Unicode(255), nullable=True),
    Column('remote_host', Unicode(1000), nullable=True),
    Column('http_referer', Unicode(255), nullable=True),
    )

users = Table('users', metadata,
    Column('username', Unicode(40), primary_key=True),
    Column('password_hashed', Unicode(80), nullable=True),
    Column('email', Unicode(255), nullable=True),
    Column('homepage', Unicode(255), nullable=True),
    Column('showemail', SmallInteger, nullable=True),
    Column('receivemail', SmallInteger, nullable=True),
    Column('sigfile', Unicode(255), nullable=True),
    Column('confirmationstring', Unicode(255), nullable=True),
    Column('confirmed', SmallInteger, nullable=True),
    Column('date_created', DateTime, nullable=True),
    Column('comment_threshold', Integer, nullable=True),
    Column('comment_threshold_enable', SmallInteger, nullable=True),
    Column('show_scores', SmallInteger, nullable=True),
    Column('fade', SmallInteger, nullable=True),
    Column('admin', SmallInteger, nullable=True),
    )

wots = Table('wots', metadata,
    Column('wots_id', Integer, primary_key=True),
    Column('title', Unicode(255), nullable=True),
    Column('date', Unicode(10), nullable=True),
    Column('time', Unicode(255), nullable=True),
    Column('location', Unicode(255), nullable=True),
    Column('address', Unicode(255), nullable=True),
    Column('contact_name', Unicode(255), nullable=True),
    Column('contact_phone', Unicode(255), nullable=True),
    Column('contact_ext', Unicode(255), nullable=True),
    Column('contact_email', Unicode(255), nullable=True),
    Column('details', UnicodeText, nullable=True),
    Column('website', Unicode(255), nullable=True),
    Column('username', Unicode(40), nullable=True),
    Column('date_posted', DateTime, nullable=True),
    )

metadata.create_all()
