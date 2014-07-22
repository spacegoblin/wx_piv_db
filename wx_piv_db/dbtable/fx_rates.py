#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime


if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float
from sqlalchemy.orm import relationship

 
from dbtable import Base, getSession
 
    
class FXRate(Base):
    """Class for a FX Rates"""

    __tablename__ = 'tbl_fxrates'
    
    id = Column(Integer, primary_key=True)
    rate_descr = Column(Unicode(255),)
    rate = Column(Float, default=0)
    period = Column(Integer,)




    

def addRate(desc, rate, period):
    fx = FXRate() 
    fx.rate_descr = unicode(desc)
    fx.rate = rate
    fx.period = period
    session.add(fx)
    session.commit()
                       

def test():
    """
    >>> session = getSession()
    >>> qry = session.query(FXRate).filter(FXRate.rate_descr == u'PLAN2014-EUR')
    >>> x = qry[0]
    >>> print x.rate
    8.5
    """
    session = getSession()
    qry = session.query(FXRate).filter(FXRate.rate_descr == u'PLAN2014-EUR')
    

    print qry.all()
    
    print qry[0].rate
    

    
if __name__=='__main__':
    import doctest
    doctest.testmod()
    #addRate('PLAN2014-EUR', 8.5, 201400)
    
    test()