#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime


if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.orm import relationship
from sqlalchemy import or_

from dbtable import Base, getSession
from coa import Account
from person import Person
from costcode import CostCode

from ahutils.record import RecordAlchemy, loadFromAlchemy, GUICodeNotExisting

from wx_datev_v02 import showForm


 
    
class Datev(Base):
    """Base class for a DATEV Data."""

    __tablename__ = 'tbl_susa'
    
    id = Column(Integer, primary_key=True)
    account_datev = Column(Unicode(255), ForeignKey('tbl_chart_of_accounts.account_datev'), nullable=False)
    kontobezeichnung_not_mdata = Column(Unicode(255),)
    _soll = Column('soll',  NUMERIC(20,2),)
    _haben = Column('haben',  NUMERIC(20,2),)
    period = Column(Integer, nullable=False)
    datum = Column(Date,)
    bu = Column(Unicode(255),)
    gegenkonto = Column(Unicode(255),)
    buchungstext = Column(Unicode(255),)
    ust = Column(Float,)
    belegfeld1 = Column(Unicode(255),)
    wkz = Column(Unicode(255),)
    kurs = Column(Float,)
    stapel_nr = Column(Unicode(255),)
    bsnr = Column(Unicode(255),)
    hk = Column(Unicode(255),)
    kost1 = Column(Unicode(255), ForeignKey('tbl_cost_centers.costcenternr'))
    tmp = Column(Unicode(255),)
    id_parent = Column(Integer,)
    company = Column(Unicode(255), nullable=False)
    foreign_amount = Column(Float,)
    comment = Column(Unicode(255),)
    imp_str = Column(Unicode(255),)
    zui = Column(Unicode(255), default=u'na', nullable=False)
    comment_2 = Column(Unicode(255),)
    pers_code = Column(Unicode(255), ForeignKey('tbl_person_stand.code'), nullable=False, default=0)
    
    fieldnames = ['id', 'fin_statement', 'hgb_acc_sort_code', 'account_datev', 'name_datev', 'amount', 'period', 'buchungstext', 'company', 'kost1', 'project_code', 'pers_code', 'full_name']
    
    account = relationship("Account", lazy='joined') 
    
    person = relationship("Person", lazy='joined')
    
    costcenter = relationship("CostCode", lazy='joined')

    def __str__(self):
        return "Datev() Account: %s %.2f" % (self.account_datev, self.amount)
    
    def getAmount(self):
        return self.soll - self.haben
    amount = property(getAmount)
    
    ##
    def getAccName(self):
        try:
            return self.account.name_datev
        except: return 'n.a.'
    name_datev = property(getAccName)
    ##
    def getFinStatement(self):
        try:
            return self.account.zuordnung_bwa
        except: return 'n.a.'
    fin_statement = property(getFinStatement)
    ##
    def getHGBSortSchema(self):
        try:
            return self.account.hgb_acc_sort_code
        except: return 'n.a.'
    hgb_acc_sort_code = property(getHGBSortSchema)
    ##
    
    def getPersonName(self):
        try:
            return self.person.full_name
        except: return False
    full_name = property(getPersonName)
    ##
        
    def getSoll(self):
        return self._soll
    def setSoll(self, v):
        if type(v)==str:
            val = v.replace(',', '')
            self._soll = val
        else: self._soll = v
    soll = property(getSoll, setSoll)
        
    def getHaben(self):
        return self._haben
    def setHaben(self, v):
        if type(v)==str:
            val = v.replace(',', '')
            self._haben = val
        else: self._haben = v
    haben = property(getHaben, setHaben)
    
    ##
    def getProjectCode(self):
        if self.costcenter:
            return self.costcenter.project_code
        else: return 'n.a.'
    project_code = property(getProjectCode)
    



    def copy(self):
        "Returns a copy of itself as new instance."
        cp = Datev()
        #cp.id NOT the id
        cp.account_datev = self.account_datev
        cp.kontobezeichnung_not_mdata = self.kontobezeichnung_not_mdata
        cp.soll = self.soll
        cp.haben = self.haben
        cp.period = self.period
        cp.datum = self.datum
        cp.bu = self.bu
        cp.gegenkonto = self.gegenkonto
        cp.buchungstext = self.buchungstext
        cp.ust = self.ust
        cp.belegfeld1 = self.belegfeld1
        cp.wkz = self.wkz
        cp.kurs = self.kurs
        cp.stapel_nr = self.stapel_nr
        cp.bsnr = self.bsnr
        cp.hk = self.hk
        cp.kost1 = self.kost1
        cp.tmp = self.tmp
        cp.id_parent = self.id_parent
        cp.company = self.company
        cp.foreign_amount = self.foreign_amount
        cp.comment = self.comment
        cp.imp_str = self.imp_str
        cp.zui = self.zui
        cp.comment_2 = self.comment_2
        cp.pers_code = self.pers_code

        return cp
    

class DatevAlchemy(Datev, RecordAlchemy):
    session = getSession() 
    
    def __init__(self):
        super(RecordAlchemy, self).__init__()
        
    
    def OnRecordDblClick(self, fieldname, obj):
        print fieldname
        if obj.pers_code>0:
            print obj.pers_code
        
        else:
            pass
        
        showForm(obj)
           

def getSampleObj(withID):
    session = DatevAlchemy.session
    return session.query(DatevAlchemy).get(withID)

def test(persCode):
    session = getSession()
    import wx
    from ahutils import record
    from wx_forms import Frm2
    
    qry = session.query(DatevAlchemy).filter(DatevAlchemy.period>201400 ).filter( or_ (DatevAlchemy.company==u'LSE HGB',
                                                                                       DatevAlchemy.company==u'LSE IFRS',
                                                                                       DatevAlchemy.company==u'LSE Wages',) )
    lst = loadFromAlchemy(qry, DatevAlchemy)
    lst.pivot(['fin_statement', 'account_datev', 'name_datev'], ['period'], 'amount')

    app = wx.App()
        
    frame = Frm2(None, lst)
    frame.Show()

    app.MainLoop() 
    
def showFrm2(persCode):
    session = getSession()
    import wx
    from ahutils import record
    from wx_forms import Frm2
    
    qry = session.query(Datev).filter(Datev.pers_code==unicode( persCode) )
    lst = loadFromAlchemy(qry, Datev)
    lst.pivot(['fin_statement', 'account_datev', 'name_datev'], ['period'], 'amount')


        
    frame = Frm2(None, lst)
    
    return frame

def returnPivotedPerson(persCode):
    raise
    session = getSession()    
    qry = session.query(Datev).filter(Datev.pers_code==unicode( persCode) )
    lst = loadFromAlchemy(qry, Datev)
    lst.pivot(['fin_statement', 'account_datev', 'name_datev'], ['period'], 'amount')
    return lst
    
def showPerson(persCode):
    """Show the person within the GUI"""
    session = DatevAlchemy.session
    import wx
    from ahutils import record
    from wx_forms import Frm
    
    qry = session.query(DatevAlchemy).filter(DatevAlchemy.pers_code==unicode(persCode))
    lst = loadFromAlchemy(qry, DatevAlchemy)
    lst.pivot(['fin_statement', 'account_datev', 'name_datev'], ['period'], 'amount')
    
    app = wx.GetApp()
    frame = Frm(app.mdi_parent_frame, lst)
    frame.Show()

 
def showPersonGrid(wxParent, persCode):
    """Show the person but return a grid.
    This is to be used in within a call in a wx Form"""
    raise
    session = getSession()

    from wx_forms import MyGrid
    
    qry = session.query(Datev).filter(Datev.pers_code==unicode(persCode))
    lst = loadFromAlchemy(qry, Datev)
    lst.pivot(['fin_statement', 'account_datev', 'name_datev'], ['period'], 'amount')
    
    return MyGrid(wxParent, lst)


if __name__=='__main__':
    import doctest
    doctest.testmod()

    test('00159')