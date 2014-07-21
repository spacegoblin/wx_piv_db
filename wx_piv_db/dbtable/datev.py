#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime


if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
 
    
class Datev(Base):
    """Base class for a DATEV Data."""

    __tablename__ = 'tbl_susa'
    
    id = Column(Integer, primary_key=True)
    account_datev = Column(Unicode(255), nullable=False)
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
    pers_code = Column(Unicode(255),)
    
    fieldnames = ['id', 'account_datev', 'amount', 'period']
        

    def __str__(self):
        return "%s %.2f" % (self.account_datev, self.amount)
    
    def getAmount(self):
        return self.soll - self.haben
    amount = property(getAmount)
    
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
    
def getSession():
    
    from ahutils import pwd                                                                                  
    engine = create_engine("postgresql+psycopg2://ahetland:%s@/lse_fin_db?host=192.168.1.91" % pwd.pwd('hetland'))  
    
     
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    #Base.metadata.create_all(engine)
    
    #From here we have declarations for the queries.
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()

    return session
                   

def test():
    session = getSession()
    qry = session.query(Datev)
    print qry.first()

if __name__=='__main__':
    import doctest
    doctest.testmod()

    test()