#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime


if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
 
    
class CostCode(Base):
    """Base class for a cost codes and project standing data."""

    __tablename__ = 'tbl_cost_centers'
    
    id = Column(Integer, primary_key=True)
    costcenternr = Column(Unicode(255), nullable=False, unique=True)
    cc_class = Column(Unicode(255),)
    cc_funtion_a = Column(Unicode(255),)
    cc_funtion_b = Column(Unicode(255),)
    description = Column(Unicode(255),)
    project_code = Column(Unicode(255), nullable=False, unique=True)
    contract_code = Column(Unicode(255),)
    comments = Column(Unicode(255),)
    active_yn = Column(Boolean,)
    customer = Column(Unicode(255),)
    business_unit = Column(Unicode(255),)
    id_parent = Column(Integer,)
    internal_ext = Column(Unicode(255),)
    description_txt = Column(Text,)
    contract_value = Column(Float,)
    expires = Column(Unicode(255),)
    payment_terms = Column(Unicode(255),)
    cc_ssc_function = Column(Unicode(255),)
    p_mgr = Column(Unicode(255),)

    
    fieldnames = ['id', 'costcenternr', 'project_code', 'description']
        
    def __str__(self):
        """Return string representation"""        
        return "Code: %s Nr.: %s \n%s\n-------------------------" % (self.project_code, self.costcenternr, self.description) 


def getSession():
    from ahutils import pwd
    engine = create_engine("postgresql+psycopg2://ahetland:%s@/lse_fin_db?host=192.168.1.91" % pwd.pwd('hetland'))  
    
    #Base.metadata.create_all(engine)
    
    #From here we have declarations for the queries.
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session
       
def show():
    session = getSession()
    import wx
    from ahutils import record
    from wx_forms import Frm
    
    qry = session.query(CostCode)
    lst = record.loadFromAlchemy(qry, CostCode)
    
    app = wx.GetApp()
    frame = Frm(app.mdi_parent_frame, lst)
    frame.Show()
 
    
def test():
    session = getSession()
    
    qry = session.query(CostCode)
    from ahutils import record
    from wx_forms import Frm2
    
    lst = record.loadFromAlchemy(qry, CostCode)
    
    import wx

    wx.SetDefaultPyEncoding('utf-8')
    app = wx.PySimpleApp()
     
    frame = Frm2(None, lst)
    frame.Show()

    app.MainLoop() 
    

if __name__=='__main__':

    
    import doctest
    doctest.testmod()
    test()
