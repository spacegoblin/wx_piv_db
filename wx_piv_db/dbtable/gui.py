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

from dbtable import Base, getLocalSession
 

 
    
class GuiUSer(Base):
    """The user. Will also dictate what one sees."""

    __tablename__ = 'tbl_users'
    
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(255), nullable=False, unique=True)
                   # pwd = Column(Unicode(255),)
                   # windows_user = Column(Unicode(255),)
                   # role = Column(Unicode(255),)
    
    fieldnames = ['id', 'username']
 
        
    def __str__(self):
        """Return string representation"""        
        return "%s %s" % (self.username, self.username) 


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
    
    fieldnames = ['id', 'menutitle', 'tablename']
 
        
    def __str__(self):
        """Return string representation"""        
        return "%d %s" % (self.id, self.menutitle)  



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
    

def addView(session):

    n = GuiView()
    n.menutitle  =  'tbl_views'
    n.tablename  =  'tbl_views'
    n.sql =u'select * from tbl_views'
    n.view_type ='FLAT'
    n.gui_menu = 'Master data'

    session.add(n)
    
    n = GuiView()
    n.menutitle  =  'tbl_users'
    n.tablename  =  'x'
    n.sql =u'select * from tbl_users'
    n.view_type ='FLAT'    
    n.gui_menu = 'Master data'
    session.add(n)

    n = GuiView()
    n.menutitle  =  'tbl_eval'
    n.tablename  =  'tbl_eval'
    n.sql =u'select * from tbl_eval'
    n.view_type ='FLAT'    
    n.gui_menu = 'Master data'
    session.add(n)

    session.commit()
    
def addUser(session):
    n = GuiUSer()
    n.username = userName
    
    session.add(n)
    session.commit()   
    
if __name__=='__main__':

    
    import doctest

    doctest.testmod()

    
    test()
