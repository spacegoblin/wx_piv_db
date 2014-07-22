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
from dbtable import Base, getSession
 
    
class PlanSusa(Base):
    """Base class for a Plan SUSA Record."""

    __tablename__ = 'tbl_susa_plan'
    
    id = Column(Integer, primary_key=True)
    account_datev = Column(Unicode(255), nullable=False)
    kontobezeichnung_not_mdata = Column(Unicode(255),)
    soll = Column(NUMERIC(20,2),)
    haben = Column(NUMERIC(20,2),)
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
    project_code = Column(Unicode(255),)
    comment = Column(Unicode(255),)
    comment_2 = Column(Unicode(255),)
    z_type = Column(Unicode(255),)
    company = Column(Unicode(255), nullable=False)
    foreign_amount = Column(NUMERIC(20,2),)
    pers_code = Column(Unicode(255),)
    
    fieldnames = ['id', 'account_datev', 'amount', 'period']
        

    def __str__(self):
        return "%s %.2f" % (self.account_datev, self.amount)
    
    def getAmount(self):
        return self.soll - self.haben
    amount = property(getAmount)
    

    def copy(self):
        "Returns a copy of itself as new instance."
        cp = PlanSusa()
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
        cp.project_code = self.project_code
        cp.comment = self.comment
        cp.comment_2 = self.comment_2
        cp.z_type = self.z_type
        cp.company = self.company
        cp.foreign_amount = self.foreign_amount
        cp.pers_code = self.pers_code

        return cp
    
    

def getNewPlanPersonRecord():
    "One record for a plan person."
    new = PlanSusa()
    new.account_datev = u'Plan record created Jul14'
    new.kontobezeichnung_not_mdata = None
    new.soll = 0
    new.haben = 0
    new.period = 201407
    new.datum = None
    new.bu = None
    new.gegenkonto = None
    new.buchungstext = None
    new.ust = None
    new.belegfeld1 = None
    new.wkz = None
    new.kurs = None
    new.stapel_nr = None
    new.bsnr = None
    new.hk = None
    new.kost1 = None
    new.tmp = None
    new.id_parent = 0
    new.project_code = 0
    new.comment = u'Person plan'
    new.comment_2 = u'Person plan'
    new.z_type = u'FC_F14v1'
    new.company = u'LSE IFRS'
    new.foreign_amount = 0
    new.pers_code = 0
    return new
        
                   

def test():
    session = getSession()
    qry = session.query(PlanSusa)
    print qry.first()

if __name__=='__main__':
    import doctest
    doctest.testmod()

    test()