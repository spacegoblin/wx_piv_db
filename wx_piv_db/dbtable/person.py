#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime


if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float, Boolean
from sqlalchemy.dialects.postgresql import NUMERIC

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
 


class Person(Base):
    """Base class for a person standing data."""

    __tablename__ = 'tbl_person_stand'
    
    id = Column(Integer, primary_key=True)
    code = Column(Unicode(255), unique=True, nullable=False)
    first_name = Column(Unicode(255),)
    last_name = Column(Unicode(255),)
    comment = Column(Unicode(255),)
    run_update = Column(Boolean,)

    fieldnames = ['id', 'code', 'first_name', 'last_name']
        
    def __str__(self):
        """Return string representation"""        
        return "%s %s Code: %s" % (self.first_name, self.last_name, self.code) 
    

class PersonStdCost(Base):
    """Standard costing table for person"""

    __tablename__ = 'tbl_person_std_cost'
    
    id = Column(Integer, primary_key=True)
    code = Column(Unicode(255), ForeignKey('tbl_person_stand.code'), nullable=False)
    account_datev = Column(Unicode(255),)
    amount = Column(NUMERIC(20,2),)
    comment = Column(Unicode(255),)
    p_code_weight = Column(Unicode(255), )
    project_code = Column(Unicode(255),)

    fieldnames = ['id', 'code', 'account_datev', 'amount']
        
    def __str__(self):
        """Return string representation"""        
        return "Code: %s Acc.: %s Project: %s %s" % (self.code, self.account_datev, self.project_code, self.amount)
    
    def dict(self):
        return "{'pers_code': %s, 'account_datev': %s, 'soll': %f, 'project_code': %s}" % ( self.code, self.account_datev, self.amount, self.project_code)
    

class PersonAndStdCost(Person):
    related = relationship(PersonStdCost)
    
    def __str__(self):
        return "PersonAndStdCost object: %s %s %s" % (self.code, self.first_name, self.last_name) 
    
    def __iter__(self):
        for x in self.related:
            yield x
    

def getSession():
    
    from ahutils import pwd
                                                                               
    engine = create_engine("postgresql+psycopg2://ahetland:%s@/lse_fin_db?host=192.168.1.91" % pwd.pwd('hetland'))  

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    
    #Base.metadata.create_all(engine)
    
    #From here we have declarations for the queries.
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session
                   

def test():
    session = getSession()
    qry = session.query(PersonAndStdCost)
    #print qry.all()
    o = qry.get('159')
    print o
    for cost in o:
        print cost.dict()

if __name__=='__main__':
    import doctest
    doctest.testmod()
    test()
    
