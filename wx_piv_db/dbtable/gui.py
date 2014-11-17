#!/usr/bin/python
# -*- coding: utf-8 -*-

#===============================================================================
# The tables that are used for the GUI
#===============================================================================

import os
import sys
import datetime


if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float, Boolean, Text
from sqlalchemy.dialects.postgresql import NUMERIC

from sqlalchemy.orm import relationship

from dbtable import Base, getSession

from ahutils.record import RecordAlchemy

    
class GuiUSer(Base):
    """The user. Will set what the user sees."""

    __tablename__ = 'tbl_users'
    
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(250), nullable=False, unique=True)
    
                   # pwd = Column(Unicode(255),)             #deprecated
                   # windows_user = Column(Unicode(255),)    #deprecated
                   # role = Column(Unicode(255),)            #deprecated
    
    fieldnames = ['id', 'username']
 
        
    def __str__(self):
        """Return string representation"""        
        return "%s %s" % (self.id, self.username) 
    
class GuiUSerAlchemy(GuiUSer, RecordAlchemy):
    session = getSession()
    
    def __init__(self):
        super(GuiUSerAlchemy, self).__init__()   
    
    def OnRecordDblClick(self, field_name, obj):
        raise


class GuiUserView(Base):
    """User and Views."""

    __tablename__ = 'tbl_users_view'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,)
    view_id = Column(Integer,)
    id_parent = Column(Integer,)

    
    fieldnames = ['id', 'user_id', 'view_id']
 
        
    def __str__(self):
        """Return string representation"""        
        return "%d %d" % (self.user_id, self.view_id)
    
class GuiUserViewAlchemy(GuiUserView, RecordAlchemy):
    session = getSession()
    
    def __init__(self):
        super(GuiUserViewAlchemy, self).__init__()   
    
    def OnRecordDblClick(self, field_name, obj):
        raise   

class GuiEval(Base):
    """User and Views."""

    __tablename__ = 'tbl_eval'
    
    id = Column(Integer, primary_key=True)
    evalcode = Column(Text,)
    description = Column(String(255),)
    view_id = Column(Integer,)
    id_parent = Column(Integer,)
    
    fieldnames = ['id', 'evalcode', 'description']
 
        
    def __str__(self):
        """Return string representation"""        
        return "%d %d" % (self.id, self.view_id) 
    
class GuiEvalAlchemy(GuiEval, RecordAlchemy):
    session = getSession()
    
    def __init__(self):
        super(GuiEvalAlchemy, self).__init__()   
    
    def OnRecordDblClick(self, field_name, obj):
        raise   
      
    
class GuiView(Base):
    """The Views."""

    __tablename__ = 'tbl_views'
    
    id = Column(Integer, primary_key=True)
    menutitle = Column(String(250), nullable=False)
    tablename = Column(String(250))
    sql  = Column(Text)
    view_type = Column(String(250))
    pivothead = Column(String(250))
    pivotrow = Column(String(250))
    pivotvalue = Column(String(250))
    gui_menu = Column(String(250), nullable=False)
    comment  = Column(Text)
    sorted = Column(Integer,)
    id_parent = Column(Integer,)
    
    alc_record = Column(String(250))
    alc_import = Column(String(250))
    alc_qry = Column(Text)
    
    incl_dblclick = Column(Boolean)
    
    fieldnames = ['id', 'menutitle', 'tablename']
 
        
    def __str__(self):
        """Return string representation"""        
        return "%d %s" % (self.id, self.menutitle)  

class GuiViewAlchemy(GuiView, RecordAlchemy):
    session = getSession()
    def __init__(self):
        super(GuiViewAlchemy, self).__init__()   
    
    def OnRecordDblClick(self, field_name, obj):
        raise   
      

class Example(Base):
    """User and Views."""

    __tablename__ = 'tbl_example'
    
    id = Column(Integer, primary_key=True)
    account = Column(String(255),)
    costcenter = Column(String(255),)
    period = Column(Integer,)
    amount = Column(Float,)
    description = Column(Text,)
    
    fieldnames = ['id', 'account', 'costcenter', 'period', 'amount', 'description']
 
 
    def exampleAccountList(self):
        return ['Flight expenses', 'Hotel costs', 'Meals', 'Entertainment', 'Other']
    
    def exampleCostCenterList(self):
        return ['100 Operations', '200 Sales', '300 Finance & Admin.', '400 Marketing']
    
    def exampleYear(self):
        for i in xrange(201401, 201413):
            yield i

class ExampleAlchemy(Example, RecordAlchemy):
    session = getSession()
    
    def __init__(self):
        super(ExampleAlchemy, self).__init__()   
    
    def OnRecordDblClick(self, field_name, obj):
        raise   
          

def test():
    session = getLocalSession()
    
    qry = session.query(GuiUSer)
    from ahutils import record
    from wx_forms import Frm2
    
    lst = record.loadFromAlchemy(qry, GuiUSer)
    
    import wx

    wx.SetDefaultPyEncoding('utf-8')
    app = wx.PySimpleApp()
     
    frame = Frm2(None, lst)
    frame.Show()

    app.MainLoop() 
    

def addView():

    n = GuiViewAlchemy()
    session = n.session
    
    n.menutitle  =  'tbl_views'
    n.tablename  =  'tbl_views'
    n.sql =u'select * from tbl_views'
    n.view_type ='FLAT'
    n.gui_menu = 'Master data'
    session.add(n)
    
    n = GuiViewAlchemy()
    n.menutitle  =  'tbl_users'
    n.tablename  =  'x'
    n.sql =u'select * from tbl_users'
    n.view_type ='FLAT'    
    n.gui_menu = 'Master data'
    session.add(n)

    n = GuiViewAlchemy()
    n.menutitle  =  'tbl_eval'
    n.tablename  =  'tbl_eval'
    n.sql =u'select * from tbl_eval'
    n.view_type ='FLAT'    
    n.gui_menu = 'Master data'
    session.add(n)

    n = GuiViewAlchemy()
    n.menutitle  =  'tbl_users_view'
    n.tablename  =  'tbl_users_view'
    n.sql =u'select * from tbl_users_view'
    n.view_type ='FLAT'    
    n.gui_menu = 'Master data'
    session.add(n)
    
    n = GuiViewAlchemy()
    n.menutitle  =  'tbl_example'
    n.tablename  =  'tbl_example'
    n.sql =u'select * from tbl_example'
    n.view_type ='PIVOT'    
    n.gui_menu = 'Data example'
    n.pivothead = 'period'
    n.pivotrow = 'costcenter, account'
    n.pivotvalue = 'amount'
    session.add(n)
    
    session.commit()
    
    
    
def addUser(userName):
    n = GuiUSerAlchemy()
    session = n.session
    
    n.username = userName
    
    session.add(n)
    session.commit()

    return n.id

def addUserToView(userId):
    n = GuiUserViewAlchemy()
    session = n.session
    
    qry = session.query(GuiViewAlchemy)
    
    for i in qry.all():
        nnn = GuiUserViewAlchemy()
        session2 = nnn.session
        nnn.user_id = userId
        nnn.view_id = i.id
        nnn.id_parent = 0
        session2.add(nnn)        
   
    session2.commit()
    

    
    
if __name__=='__main__':

    
    import doctest

    doctest.testmod()


