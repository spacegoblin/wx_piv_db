#!/usr/bin/python
# -*- coding: utf-8 -*-

#===============================================================================
# OCRA trial balance report
# OCRA export of Financial Data in Excel saved as csv
# Income Statement + Balance Sheet + Other Data and supress zero values
# Put the three sheets into one sheet and add a column fin_statement (name them Other Data, IS, BS)
# add a column company
# column period is in the code
#===============================================================================

import os
import sys
import datetime
import re

if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
 

class Ocra(Base):
    """Class for Personnel Costs as from the other report in xls from Zindler."""

    __tablename__ = 'tbl_ocra_tb'
    
    id = Column(Integer, primary_key=True)
    _account_desc = Column('account_desc', Unicode(255),)
    _the_x = Column('the_x', Unicode(255),)
    _amount_booked = Column('amount_booked', Numeric(20, 2), default=0)
    _adjustment = Column('adjustment', Numeric(20, 2), default=0)
    _inter_company = Column('inter_company', Numeric(20, 2), default=0)
    _intra_company = Column('intra_company', Numeric(20, 2), default=0)
    _amount_reported = Column('amount_reported', Numeric(20, 2), default=0)
    _account_code = Column('account_code', Integer,)
    
    fin_statement = Column(Unicode(255),)
    company = Column(Unicode(255),)
        
    period = Column(Integer,)
    z_type = Column(Unicode(255),)
    z_comment = Column(Unicode(255),)
    z_random_str = Column(Unicode(255),)
    
    ##Helper methods

    def convNumber(self, v):
        """Convert a k number string into float"""
        if not v or v=='':
            return 0
        print "value v", v
        
        if '.' in v:
            a,b = v.split('.')
            
            a = a.replace(',', '')
            
            #print a, "b", b, "-"
            
            
            if len(b)==3:
                n="%s%s" % (a,b)
                print float(n)
            elif len(b)==2:
                n="%s%s0" % (a,b)
                print float(n)
            else:
                raise
            
        #print "---------- %s" % self.fin_statement
        else:
            n = float(v)
        return n
    
    ##The properties
    def getaccount_desc(self):
        return self._account_desc
    def setaccount_desc(self, v):
        self._account_desc = v.strip()
    account_desc = property(getaccount_desc, setaccount_desc)
    
    ##the_x
    def getthe_x(self):
        return self._the_x
    def setthe_x(self, v):
        self._the_x=v.strip()
    the_x = property (getthe_x, setthe_x)
    
    ##amount_booked
    def getamount_booked(self):
        return self._amount_booked
    def setamount_booked(self, v):
        self._amount_booked = self.convNumber(v)
    amount_booked = property(getamount_booked, setamount_booked)
    
    ##adjustment
    def getadjustment(self):
        return self._adjustment
    def setadjustment(self, v):
        self._adjustment = self.convNumber(v) 
    adjustment = property(getadjustment, setadjustment)
    
    ##inter_company
    def getinter_company(self):
        return self._inter_company
    def setinter_company(self, v):
        self._inter_company = self.convNumber(v)
    inter_company = property(getinter_company, setinter_company)
    
    #intra_company
    def getintra_company(self):
        return self._intra_company
    def setintra_company(self, v):
        self._intra_company = self.convNumber(v)
    intra_company = property(getintra_company, setintra_company)
    
    ##amount_reported
    def getamount_reported(self):
        return self._amount_reported
    def setamount_reported(self, v):
        self._amount_reported = self.convNumber(v)
    amount_reported = property(getamount_reported, setamount_reported)
    
    ##account_code
    def getaccount_code(self):
        return self._account_code
    def setaccount_code(self, v):
        v = v.strip()
        v = v.replace(',', '')
        v = v.replace('.000', '')
        v = v.replace('.00', '')
        self._account_code = int ( v )
    account_code = property(getaccount_code, setaccount_code)    
               
    def __str__(self):
        return "%s %s %s %s %s %s %s %s" % (self.account_desc, self.the_x, self.amount_booked, self.adjustment, self.inter_company, \
                                   self.intra_company, self.amount_reported, self.account_code)

from ahutils import pwd


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




def fixNumber(str_amnt):
    "Helper method to fix the amount string into float."
    str_amnt = str_amnt.replace('.', '')
    if '-' in str_amnt:
        str_amnt = int(str_amnt.replace('-', '')) /-100.0
    else:
        str_amnt = int(str_amnt) /100.0
    return str_amnt

CSV_ROW = ['Account', '', 'Booked (EUR)', 'Adjustment','Intercompany', 'Intracompany', 'Reported', 'Account', 'fin_statement', 'company']

def importFile(FILE, period, type):
    
    reader = csv.reader(open(FILE, "rb"), delimiter=",")
    i=0

    for row in reader:
       if i==0:
           assert row==CSV_ROW, "%s" % row
           i+=1
           pass
           
       else:
           #print row
           ocra = Ocra()
           ocra.account_desc = unicode(row[0], errors='ignore')  
           ocra.the_x = unicode(row[1], errors='ignore') 
           ocra.amount_booked = row[2]
           ocra.adjustment = row[3]
           ocra.inter_company = row[4]
           ocra.intra_company = row[5]
           ocra.amount_reported = row[6]
           ocra.account_code = row[7]
           ocra.fin_statement = unicode(row[8], errors='ignore')  
           ocra.company = unicode(row[9], errors='ignore')  

           ocra.z_random_str = unicode(random_str)
           ocra.period = period
           ocra.z_type = unicode( type )
           #print ocra
           session.add(ocra)
    session.commit()


if __name__=='__main__':
    import doctest
    doctest.testmod()
    importFile('C:\ocra_export\imp.csv', 201405, 'Fcst June')
    
