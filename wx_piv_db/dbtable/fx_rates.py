#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime


if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
 
    
class FXRate(Base):
    """Class for a FX Rates"""

    __tablename__ = 'tbl_fxrates'
    
    id = Column(Integer, primary_key=True)
    rate_descr = Column(Unicode(255),)
    rate = Column(Float, default=0)
    period = Column(Integer,)


from ahutils import pwd

                                                                                   
engine = create_engine("postgresql+psycopg2://ahetland:%s@/lse_fin_db?host=192.168.1.91" % pwd.pwd('hetland')) #, encoding='utf-8')  

 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

#From here we have declarations for the queries.
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

    

def addRate(desc, rate, period):
    fx = FXRate() 
    fx.rate_descr = unicode(desc)
    fx.rate = rate
    fx.period = period
    session.add(fx)
    session.commit()
                       

def test():
    """
    >>> qry = session.query(FXRate).filter(FXRate.rate_descr == u'PLAN2014-EUR')
    >>> x = qry[0]
    >>> print x.rate
    8.5
    """
    qry = session.query(FXRate).filter(FXRate.rate_descr == u'PLAN2014-EUR')
    

    print qry.all()
    
    print qry[0].rate
    

    
if __name__=='__main__':
    import doctest
    doctest.testmod()
    #addRate('PLAN2014-EUR', 8.5, 201400)
    
    test()