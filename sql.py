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

election_apidoc = Table('election_apidoc', metadata,
    Column('doc_id', Integer, primary_key=True),
    Column('content', Unicode(5000), nullable=True),
    Column('last_updated', DateTime, nullable=True),
)

election_aps = Table('election_apps', metadata,
    Column('app_id', Integer, primary_key=True),
    Column('election_id', Integer, nullable=True),
    Column('title', Unicode(1000), nullable=True),
    Column('url', Unicode(255), nullable=True),
)

election_candidates = Table('election_candidates', metadata,
    Column('candidate_id', Integer, primary_key=True),
    Column('ward', Unicode(10), nullable=True),
    Column('name', Unicode(10), nullable=True),
    Column('address', Unicode(10), nullable=True),
    Column('email', Unicode(10), nullable=True),
    Column('home_phone', Unicode(10), nullable=True),
    Column('bus_phone', Unicode(10), nullable=True),
    Column('fax_number', Unicode(10), nullable=True),
    Column('election_id', Integer, nullable=True),
    Column('website', Unicode(10), nullable=True),
    Column('gender', Unicode(10), nullable=True),
    Column('bio', Unicode(10000), nullable=True),
    Column('incumbent', Integer, nullable=True),
    Column('withdrawn', Integer, nullable=True),
)

election_questions = Table('election_questions', metadata,
    Column('question_id', Integer, primary_key=True),
    Column('question', Unicode(1000), nullable=True),
)

election_responses = Table('election_responses', metadata,
    Column('response_id', Integer, primary_key=True),
    Column('question_id', Integer, nullable=True),
    Column('candidate_id', Integer, nullable=True),
    Column('brief_response', Unicode(200), nullable=True),
    Column('full_response', Unicode(5000), nullable=True),
    Column('date_posted', DateTime, nullable=True),
)

election_types = Table('election_types', metadata,
    Column('type_id', Integer, primary_key=True),
    Column('type', Unicode(100), nullable=True),
)

metadata.create_all()
