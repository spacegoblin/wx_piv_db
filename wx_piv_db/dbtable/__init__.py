#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from ahconfig import const

def getSession():
    from ahutils import pwd
    engine = create_engine("postgresql+psycopg2://%s:%s@/%s?host=%s" % (const.gui_user, const.windows_pwd, const.db_lst_dsn, const.host))  
    
    #This will create the database table if not created already
    #Base.metadata.create_all(engine)
    
    #From here we have declarations for the queries.
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session


def getLocalSession():
    from ahutils import pwd
    engine = create_engine("postgresql+psycopg2://%s:%s@/%s?host=%s" % (const.gui_user, const.windows_pwd, 'ah_db', 'localhost'))  
    
    #This will create the database table if not created already
    #Base.metadata.create_all(engine)
    
    #From here we have declarations for the queries.
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session