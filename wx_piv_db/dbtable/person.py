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
from coa import Account

class Person(Base):
    """Base class for a person standing data."""

    __tablename__ = 'tbl_person_stand'
    
    id = Column(Integer, primary_key=True)
    code = Column(Unicode(255), unique=True, nullable=False)
    first_name = Column(Unicode(255),)
    last_name = Column(Unicode(255),)
    comment = Column(Unicode(255),)
    run_update = Column(Boolean,)
    start_stop = Column(Unicode(255),)

    def getFullName(self):
        if self.id>1:
            return "%s %s" % (self.first_name, self.last_name)
        else: return False
    full_name = property(getFullName)
    
    fieldnames = ['code', 'full_name', 'first_name', 'last_name', 'comment', 'run_update']
        
    def __str__(self):
        """Return string representation"""        
        return u"Class Person(): %s %s Code: %s" % (self.first_name, self.last_name, self.code)
    
class PersonAlchemy(Person, RecordAlchemy):
    session = getSession()
    
    def __init__(self):
        super(RecordAlchemy, self).__init__()
        
    def getName(self):
        return "%s - %s %s" % (self.code, self.first_name, self.last_name)
    name = property(getName)
    
    
    def OnRecordDblClick(self, field_name, obj):
        import wx_time_v01
        frame = wx_time_v01.FrmDev( None )
        frame.Show()



class PersonStdCost(Base):
    """Standard costing table for person"""

    __tablename__ = 'tbl_person_std_cost'
    
    id = Column(Integer, primary_key=True)
    code = Column(Unicode(255), ForeignKey('tbl_person_stand.code'), nullable=False)
    account_datev = Column(Unicode(255), ForeignKey('tbl_chart_of_accounts.account_datev'), nullable=False)
    amount = Column(NUMERIC(20,2),)
    comment = Column(Unicode(255),)
    p_code_weight = Column(Unicode(255), )
    project_code = Column(Unicode(255),)
    
    person = relationship("Person", lazy='joined')
    account = relationship("Account", lazy='joined') 
    
    def getDatevAccount(self):
        return "%s" % self.account.name_datev
    
    name_datev = property( getDatevAccount )
    
    fieldnames = ["id", "code", "account_datev", "name_datev", "amount", "comment", "p_code_weight", "project_code", "full_name"]
    

    
    def getFullName(self):
        return self.person.full_name
    full_name = property(getFullName)
    
    def getAccount(self):
        return "%s %s" % (self.account.account_datev, self.account.name_datev)
    datev_full = property(getAccount)        
            
    def __str__(self):
        """Return string representation"""        
        return "Code: %s Acc.: %s Project: %s %s" % (self.code, self.account_datev, self.project_code, self.amount)
    

class PersonAndStdCost(Person):
    related = relationship(PersonStdCost)
    
    def __str__(self):
        return "PersonAndStdCost() object: %s %s %s\n____________________" % (self.code, self.first_name, self.last_name) 
    
    def __iter__(self):
        for x in self.related:
            yield x
    
class PersonStdCostAlchemy(PersonStdCost, RecordAlchemy):
    session = getSession()
    
    def __init__(self):
        super(RecordAlchemy, self).__init__()   
    
    def OnRecordDblClick(self, field_name, obj):
        raise         

def test():
    session = getSession()
    qry = session.query(PersonStdCostAlchemy)
    #print qry.all()
    o = qry.get('159')
    print o
    for cost in o:
        print cost
        
def showPersonStdCost(persCode):
    """Show the person within the GUI"""
    session = PersonStdCostAlchemy.session
    import wx

    from wx_forms import Frm
    
    qry = session.query(PersonStdCostAlchemy).filter(PersonStdCostAlchemy.code==unicode(persCode))
    lst = loadFromAlchemy(qry, PersonStdCostAlchemy)
    #lst.pivot(['fin_statement', 'account_datev', 'name_datev'], ['period'], 'amount')
    
    app = wx.GetApp()
    frame = Frm(app.mdi_parent_frame, lst)
    frame.Show()
        
def testMixInn():
    "Testing the alchemy mix inn class"
    session = PersonAlchemy.session
    qry = session.query(PersonAlchemy)


    o = qry.get('159')
    print o
    
    lst = loadFromAlchemy(qry, PersonAlchemy)

    import wx
    from wx_forms import Frm2
       
    app = wx.App()
        
    frame = Frm2(None, lst)
    frame.Show()

    app.MainLoop() 

if __name__=='__main__':
    import doctest
    doctest.testmod()
    test()
    
