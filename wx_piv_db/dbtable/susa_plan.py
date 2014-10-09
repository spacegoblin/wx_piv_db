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
from ahutils.record import RecordAlchemy, loadFromAlchemy
 
    
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
    
    fieldnames = ['id', 'account_datev', 'amount', 'period', 'buchungstext', 'project_code', 'z_type', 'company', 'pers_code']
    


    def __str__(self):
        return "Account: %s for %d %.2f" % (self.account_datev, self.period, self.amount)
    
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
    
    
class PlanSusaAlchemy(PlanSusa, RecordAlchemy):
    session = getSession()
    
    def __init__(self):
        super(PlanSusaAlchemy, self).__init__()
           
    
def getNewPlanPersonRecord():
    "One record for a plan person."
    new = PlanSusa()
    new.account_datev = u'Plan record 2015 created Sep14'
    new.kontobezeichnung_not_mdata = u'Plan record 2015 created Sep14'
    new.soll = 0
    new.haben = 0
    new.period = 201500
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
    new.comment = u'Plan 2015 people'
    new.comment_2 = u'Plan 2015 people'
    new.z_type = u'PB_15v1'
    new.company = u'LSE IFRS'
    new.foreign_amount = 0
    new.pers_code = 0
    return new
        
def copyRecordToPlanBase(obj):
    print "copyRecordToPlanBase"
    new = PlanSusa()

    new.account_datev = obj.account_datev
    new.kontobezeichnung_not_mdata = obj.kontobezeichnung_not_mdata
    new.soll = obj.soll
    new.haben = obj.haben
    new.period = 201500
    new.datum = None
    new.bu = None
    new.gegenkonto = obj.gegenkonto
    new.buchungstext = obj.buchungstext
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
    new.project_code = obj.project_code
    new.comment = obj.comment
    new.comment_2 = obj.comment_2
    new.z_type = u'PB_15_Base'
    new.company = u'LSE IFRS'
    new.foreign_amount = 0
    new.pers_code = obj.pers_code
    
    session = getSession()
    session.add(new)
    session.commit()
    
    return new

 
                 

def test():

    session = PlanSusaAlchemy.session
    qry = session.query(PlanSusaAlchemy)
    print qry.first()

if __name__=='__main__':
    import doctest
    doctest.testmod()

    test()