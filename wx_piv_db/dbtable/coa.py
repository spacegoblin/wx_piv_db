#!/usr/bin/python
# -*- coding: utf-8 -*-

#===============================================================================
# Chart of Accounts
#===============================================================================

import os
import sys
import datetime


if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float, Boolean, Text

from sqlalchemy.orm import relationship

from dbtable import Base, getSession
 

 
    
class Account(Base):
    """Chart of Accounts"""

    __tablename__ = 'tbl_chart_of_accounts'
    
    id = Column(Integer, primary_key=True)
    account_datev = Column(Unicode(255), nullable=False, unique=True)
    name_datev = Column(Unicode(255),)
    zuordnung_bwa = Column(Unicode(255),)
    bwa_titel = Column(Unicode(255),)
    zuordnung_pundl = Column(Unicode(255),)
    ifrs_accounts = Column(Unicode(255),)
    accounts_aurora = Column(Unicode(255),)
    acc_description_aurora = Column(Unicode(255),)
    accounts_ssc = Column(Unicode(255),)
    acc_description_ssc = Column(Unicode(255),)
    comments = Column(Unicode(255),)
    cluster_fc = Column(Unicode(255),)
    einzelposten_fc = Column(Unicode(255),)
    acc_company = Column(Unicode(255),)
    ifrs_acc_sort_code = Column(Unicode(255),)
    comment_long = Column(Text,)
    ssc_account_class = Column(Unicode(255),)
    ssc_internal_account_x = Column(Unicode(255),)
    ssc_cost_centre = Column(Unicode(255),)
    hgb_acc_sort_code = Column(Unicode(255),)
    i_comp = Column(Unicode(255),)
    cf_acc_sort_code = Column(Unicode(255),)
    rpt_acc_sort_code = Column(Unicode(255),)

    
    fieldnames = ['id', 'account_datev', 'name_datev', 'hgb_acc_sort_code']
 

        
    def __str__(self):
        """Return string representation"""        
        return "Code: %s Acc. Name: %s \n%s\n-------------------------" % (self.account_datev, self.name_datev, self.hgb_acc_sort_code) 



       
def show():
    session = getSession()
    import wx
    from ahutils import record
    from wx_forms import Frm
    
    qry = session.query(Account)
    lst = record.loadFromAlchemy(qry, Account)
    
    app = wx.GetApp()
    frame = Frm(app.mdi_parent_frame, lst)
    frame.Show()
 
    
def test():
    session = getSession()
    
    qry = session.query(Account)
    from ahutils import record
    from wx_forms import Frm2
    
    lst = record.loadFromAlchemy(qry, Account)
    
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
