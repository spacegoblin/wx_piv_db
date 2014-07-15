#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime


if '..//..//' not in sys.path:
    sys.path.append('..//..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
 
    
class Person(Base):
    """Base class for a person standing data."""

    __tablename__ = 'tbl_person_stand'
    
    id = Column(Integer, primary_key=True)
    code = Column(Unicode(255),)
    first_name = Column(Unicode(255),)
    last_name = Column(Unicode(255),)


    fieldnames = ['id', 'code', 'first_name', 'last_name']
        
    def __str__(self):
        """Return string representation"""        
        return "%s %s Code: %s" % (self.first_name, self.last_name, self.code) 




from ahutils import pwd

                                                                                    
engine = create_engine("postgresql+psycopg2://ahetland:%s@/lse_fin_db?host=192.168.1.91" % pwd.pwd('hetland'))  

 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

#From here we have declarations for the queries.
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()


                   

def test():
    qry = session.query(CRM)
    print qry.all()

if __name__=='__main__':
    import doctest
    doctest.testmod()

