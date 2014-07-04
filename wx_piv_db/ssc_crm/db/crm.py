#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime


if '..//..//' not in sys.path:
    sys.path.append('..//..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
 
    
class CRM(Base):
    """Class for a single CRM Record."""

    __tablename__ = 'tbl_ssccrm'
    
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer,)
    project_id = Column(Unicode(255),)
    _date = Column('date', Date, )   #nullable=False
    stage = Column(Unicode(255),)
    text = Column(Unicode(255),)
    organization = Column(Unicode(255),)
    user_id = Column(Unicode(255),)
    status = Column(Unicode(255),)
    _delivery_start = Column('delivery_start', Date,)
    amount = Column(Float,)
    _delivery_start2 = Column('delivery_start2', Date,)
    amount2 = Column(Float,)
    _delivery_start3 = Column('delivery_start3', Date,)
    amount3 = Column(Float,)
    #length3 = Column(Unicode(255),)
    ssc_main_party = Column(Unicode(255),)
    z_random_str = Column(Unicode(255),)
    z_type = Column(Unicode(255),)
    z_year = Column(Integer,)
    z_amount = Column(Float, default=0)
    z_history = Column(Unicode(255),)
    z_comment = Column(Unicode(255),)
    z_partner_adj = Column(Unicode(255),)   #To use the same partner name as in the accounting
    include_in_revenue_plan = Column(Integer,)


    def getdate(self):
        return self._date
    def setdate(self, val):
        try:
            self._date = datetime.datetime.strptime(val, '%d/%m/%Y')
        except:
            print val, "did not enter as date"
            self._date = None
    date = property(getdate, setdate)
    
          
    def getdelivery_start(self):
        return self._delivery_start
    def setdelivery_start(self, val):
        try:
            self._delivery_start = datetime.datetime.strptime(val, '%d/%m/%Y')
        except:
            self._delivery_start = None
    delivery_start = property(getdelivery_start, setdelivery_start)
    
    def getdelivery_start2(self):
        return self._delivery_start2
    def setdelivery_start2(self, val):
        try:
            self._delivery_start2 = datetime.datetime.strptime(val, '%d/%m/%Y')
        except:
            self._delivery_start2 = None
    delivery_start2 = property(getdelivery_start2, setdelivery_start2)

    def getdelivery_start3(self):
        return self._delivery_start3
    def setdelivery_start3(self, val):
        try:
            self._delivery_start3 = datetime.datetime.strptime(val, '%d/%m/%Y')
        except:
            self._delivery_start3 = None
    delivery_start3 = property(getdelivery_start3, setdelivery_start3)
        
    def __str__(self):
        """Return string representation"""
        
        return "%s Project: %s" % (self.z_type, self.project_id) 
    

 
# Create an engine that stores data in the local directory's
# sqlalchemy.db file.

    def copy(self):
        """create a copy of self"""
        obj = CRM()
        # obj.id = None since it has not been inserted into db 
        obj.sale_id  =  self.sale_id
        obj.project_id  =  self.project_id
        obj.date  =  self.date
        obj.stage  =  self.stage
        obj.text  =  self.text
        obj.organization  =  self.organization
        obj.user_id  =  self.user_id
        obj.status  =  self.status
        obj._delivery_start  =  self.delivery_start
        obj.amount  =  self.amount
        obj.delivery_start2  =  self.delivery_start2
        obj.amount2  =  self.amount2
        obj.delivery_start3  =  self.delivery_start3
        obj.amount3  =  self.amount3
        obj.ssc_main_party  =  self.ssc_main_party
        obj.z_random_str  =  self.z_random_str
        obj.z_type  =  None
        obj.z_year = None
        obj.z_amount = None
        obj.z_history = self.z_history
        obj.z_comment = self.z_comment
        obj.include_in_revenue_plan = self.include_in_revenue_plan
        return obj
    
#engine = create_engine('sqlite:///crm_ssc.db')

from ahutils import pwd

                                                                                    #, client_encoding='utf8')
engine = create_engine("postgresql+psycopg2://ahetland:%s@/lse_fin_db?host=192.168.1.91" % pwd.pwd('hetland'))  

 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

#From here we have declarations for the queries.
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

    
from ahutils.utils import randomString
random_str = randomString()
import csv

def loadCSVFile(PATH):
    """Load a CRM file"""

    reader = csv.reader(open(PATH, "rb"), delimiter=",")
    i=0
    lst = []

    for row in reader:

        if i==0:
            #assert row==CSV_ROW, "%s" % row
            pass
        else:
            crm = CRM()
            crm.sale_id = row[0]
            crm.project_id = row[1]
            crm.date = row[2]
            crm.stage = row[3]
            crm.text = unicode(row[4], errors='ignore')
            crm.organization = unicode(row[5], errors='ignore')
            crm.user_id = row[6]
            crm.status = row[7]
            crm.delivery_start = row[8]
            crm.amount = row[9]
            crm.delivery_start2 = row[10]
            crm.amount2 = row[11]
            crm.delivery_start3 = row[12]
            crm.amount3 = row[13]
            #######crm.length3 = row[14]
            crm.ssc_main_party = unicode(row[15], errors='ignore')
            crm.z_random_str = random_str
            crm.z_type = 'Original'
            crm.z_history = 'Current'
            crm.z_comment = None
            crm.include_in_revenue_plan = row[16]
            session.add(crm)
            
            #We will for each Original Record insert a copy with value and year
            if crm.delivery_start:
                cp = crm.copy()
                cp.z_year = crm.delivery_start.year
                cp.z_amount = crm.amount
                cp.z_type = 'Generated'
                session.add(cp)

            if crm.delivery_start2:
                cp = crm.copy()
                cp.z_year = crm.delivery_start2.year
                cp.z_amount = crm.amount2
                cp.z_type = 'Generated'
                session.add(cp)

            if crm.delivery_start3:
                cp = crm.copy()
                cp.z_year = crm.delivery_start3.year
                cp.z_amount = crm.amount3
                cp.z_type = 'Generated'
                session.add(cp)
                                                        
        i+=1

    session.commit()
                   

def test():
    qry = session.query(CRM)
    print qry.all()

if __name__=='__main__':
    import doctest
    doctest.testmod()
    loadCSVFile(PATH='C:\ocra_export\imp.csv')
