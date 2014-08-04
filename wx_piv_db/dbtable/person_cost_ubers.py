#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime

if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float, Boolean, Numeric
from sqlalchemy.dialects.postgresql import NUMERIC

from sqlalchemy.orm import relationship

from dbtable import Base, getSession
 
    
class PersKost(Base):
    u"""Class for Personnel Costs as from the PDF report Personalkostenübersicht from Zindler."""

    __tablename__ = 'tbl_datev_perskosten'
    
    id = Column(Integer, primary_key=True)
    pers_code = Column(Unicode(255),)
    p_name = Column(Unicode(255),)

    gesamtbrutto = Column(Numeric(20, 2), default=0)
    ag_anteil_bav = Column(Numeric(20, 2))
    nettobezuge = Column(Numeric(20, 2), default=0)
    sv_ag_anteil = Column(Numeric(20, 2), default=0)
    umlage = Column(Numeric(20, 2), default=0)
    pauschale_steuern = Column(Numeric(20, 2), default=0)
    gesamtkosten = Column(Numeric(20, 2), default=0)
        
    z_period = Column(Integer,)
    z_comment = Column(Unicode(255),)
    z_random_str = Column(Unicode(255),)
    
    
    fieldnames = ['id', 'pers_code', 'p_name', 'z_period', 'gesamtbrutto']

    def test(self):
        "Test if the sums are correct"
        test = self.gesamtkosten - self.gesamtbrutto - self.nettobezuge - self.sv_ag_anteil - self.umlage - self.pauschale_steuern

        if test > 0.001 or test < -0.001:
            print self
            raise

        
    def __str__(self):
        return "%s %s" % (self.pers_code, self.p_name)
       

    
def test():
    session = getSession()
    
    qry = session.query(PersKost)
    from ahutils import record
    from wx_forms import Frm2
    
    lst = record.loadFromAlchemy(qry, PersKost)
    
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
