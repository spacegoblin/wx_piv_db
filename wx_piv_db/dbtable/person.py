#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime


if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float, Boolean
from sqlalchemy.dialects.postgresql import NUMERIC

from sqlalchemy.orm import relationship

from dbtable import Base, getSession
from ahutils.record import RecordAlchemy, loadFromAlchemy


class Person(Base):
    """Base class for a person standing data."""

    __tablename__ = 'tbl_person_stand'
    
    id = Column(Integer, primary_key=True)
    code = Column(Unicode(255), unique=True, nullable=False)
    first_name = Column(Unicode(255),)
    last_name = Column(Unicode(255),)
    comment = Column(Unicode(255),)
    run_update = Column(Boolean,)

    fieldnames = ['code', 'first_name', 'last_name', 'comment', 'run_update']
        
    def __str__(self):
        """Return string representation"""        
        return "Class Person(): %s %s Code: %s" % (self.first_name, self.last_name, self.code)
    
class PersonAlchemy(Person, RecordAlchemy):
    session = getSession()  #this gets the session only once!
    
    fieldnames = ['name']
    
    def __init__(self):
        super(RecordAlchemy, self).__init__()
        
    def getName(self):
        return "%s - %s %s" % (self.code, self.first_name, self.last_name)
    name = property(getName)

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
               

def test():
    session = getSession()
    qry = session.query(PersonAndStdCost)
    #print qry.all()
    o = qry.get('159')
    print o
    for cost in o:
        print cost.dict()
        
def testMixInn():
    "Testing the alchemy mix inn class"
    session = PersonAlchemy.session
    qry = session.query(PersonAlchemy)

    o = qry.get('159')
    print o
    
    lst = loadFromAlchemy(qry, PersonAlchemy)

    import wx
    from wx_forms import Frm2
       
    app = wx.PySimpleApp()
        
    frame = Frm2(None, lst)
    frame.Show()

    app.MainLoop() 

if __name__=='__main__':
    import doctest
    doctest.testmod()
    testMixInn()
    
