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
from coa import Account
 
#Base = declarative_base()    I use the Base in the mapper below so we need to use the same base
 
    
class Datev(Base):
    """Base class for a DATEV Data."""

    __tablename__ = 'tbl_susa'
    
    id = Column(Integer, primary_key=True)
    account_datev = Column(Unicode(255), ForeignKey('tbl_chart_of_accounts.account_datev'), nullable=False)
    kontobezeichnung_not_mdata = Column(Unicode(255),)
    _soll = Column('soll', Float,)
    haben = Column(Float,)
    period = Column(Integer,)
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
    kost1 = Column(Unicode(255),)
    tmp = Column(Unicode(255),)
    id_parent = Column(Integer,)
    company = Column(Unicode(255), nullable=False)
    foreign_amount = Column(Float,)
    comment = Column(Unicode(255),)
    imp_str = Column(Unicode(255),)
    zui = Column(Unicode(255), default=u'na', nullable=False)
    comment_2 = Column(Unicode(255),)
    pers_code = Column(Unicode(255), ForeignKey('tbl_person_stand.code'), nullable=False, default=0)
    
    fieldnames = ['id', 'fin_statement', 'account_datev', 'name_datev', 'amount', 'period']
    
    account = relationship("Account")

    def __str__(self):
        return "%s %.2f" % (self.account_datev, self.amount)
    
    def getAmount(self):
        return self.soll - self.haben
    amount = property(getAmount)
    
    ##
    def getAccName(self):
        return self.account.name_datev
    name_datev = property(getAccName)
    ##
    def getFinStatement(self):
        return self.account.zuordnung_bwa
    fin_statement = property(getFinStatement)
    
    def getSoll(self):
        return self._soll
    def setSoll(self, v):
        if type(v)==str:
            val = v.replace(',', '')
            self._soll = val
        else: self._soll = v
    soll = property(getSoll, setSoll)
        
    
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
    

                   

def test():
    session = getSession()
    import wx
    from ahutils import record
    from wx_forms import Frm2
    
    qry = session.query(Datev).filter(Datev.pers_code==u'00159')
    lst = record.loadFromAlchemy(qry, Datev)
    lst.pivot(['fin_statement', 'account_datev', 'name_datev'], ['period'], 'amount')

    app = wx.PySimpleApp()
    
    app.MY_FLOAT_FORMAT = ',.2f'
    
    frame = Frm2(None, lst)
    frame.Show()

    app.MainLoop() 
    
def show():
    session = getSession()
    import wx
    from ahutils import record
    from wx_forms import Frm2
    
    qry = session.query(Datev).filter(Datev.pers_code==u'00159')
    lst = record.loadFromAlchemy(qry, Datev) 
    
    app = wx.PySimpleApp()
    
    app.MY_FLOAT_FORMAT = ',.2f'
    
    frame = Frm2(None, lst)
    frame.Show()

    app.MainLoop() 

if __name__=='__main__':
    import doctest
    doctest.testmod()

    test()