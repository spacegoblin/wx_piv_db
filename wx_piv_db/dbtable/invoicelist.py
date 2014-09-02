#!/usr/bin/python
# -*- coding: utf-8 -*-

#===============================================================================
# Banking
#===============================================================================

import os
import sys
import datetime
import csv

if '..//' not in sys.path:
    sys.path.append('..//')
    
    
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, Date, Float, Boolean, Text
from sqlalchemy.dialects.postgresql import NUMERIC

from sqlalchemy.orm import relationship

from dbtable import Base, getSession


def fixNumber(str_amnt):
    "Helper method to fix the amount string into float."
    if str_amnt:
        str_amnt = str_amnt.strip()
        str_amnt = str_amnt.replace(',', '')
        if '-' in str_amnt:
            str_amnt = float(str_amnt.replace('-', ''))*-1
        else:
            str_amnt = float(str_amnt.strip()) 
        return str_amnt
    else: return 0
    
def dateFromStr(st):
    return datetime.datetime.strptime(st, '%d/%m/%y')


class InvoiceList(Base):
    """the invoice list as used by Diana"""

    __tablename__ = 'tbl_invoicelist'
    
    id = Column(Integer, primary_key=True)
    project_code = Column(Unicode(255), ).strip()
    travel = Column(Unicode(255), ).strip()
    month_ms = Column(Unicode(255), ).strip()
    time_for_payment = Column(Unicode(255), ).strip()
    description = Column(Unicode(255), ).strip()
    contract = Column(Unicode(255), ).strip()
    status = Column(Unicode(255), ).strip()
    re_nr = Column(Unicode(255), ).strip()
    kostenstelle = Column(Unicode(255), ).strip()
    datum = Column(Date,)
    kunde = Column(Unicode(255), ).strip()
    summe_netto = Column(NUMERIC(20,2),).strip()
    mwst = Column(NUMERIC(20,2),)
    period = Column(Integer, )
    
    fieldnames = ['id', 'project_code', 'period', 'amount']
    
    def getAmount(self):
        return self.summe_netto
    amount = property(getAmount)
        

def importFile_v02(FILE):
    """Import csv file from Diana

    """
    session = getSession()
    
    reader = csv.reader(open(FILE, "rb"), delimiter=",")
    i=0
    lst = list(reader)
    lngt = len(lst)

    
    for row in lst:
        print row
        if i==0:
            #assert row==CSV_ROW, "%s" % row
            i+=1
            pass
        elif i==lngt:
            #last row
            continue
        else:
            
            b = InvoiceList()
        
            b.project_code = unicode(row[0], errors='ignore')
            b.travel = unicode(row[1], errors='ignore')
            b.month_ms = unicode(row[2], errors='ignore')
            b.time_for_payment = unicode(row[3], errors='ignore')
            b.description = unicode(row[4], errors='ignore')
            b.contract = unicode(row[5], errors='ignore')
            b.status = unicode(row[6], errors='ignore')
            b.re_nr = unicode(row[7], errors='ignore')
            b.kostenstelle = unicode(row[8], errors='ignore')
            b.datum = dateFromStr(row[9])
            b.kunde = unicode(row[10], errors='ignore')
            b.summe_netto = fixNumber(row[11])
            b.mwst = fixNumber(row[12])
        
            print b
         
            session.add(b)
        
            i+=1
        
        session.commit()
                  
def test():
    session = getSession()
    
    qry = session.query(InvoiceList)
    from ahutils import record
    from wx_forms import Frm2
    
    lst = record.loadFromAlchemy(qry, InvoiceList)
    
    import wx

    wx.SetDefaultPyEncoding('utf-8')
    app = wx.App()
    frame = Frm2(None, lst)
    frame.Show()

    app.MainLoop() 
    


    
if __name__=='__main__':

    
    import doctest

    doctest.testmod()
    test()
    #importFile_v02('C:\\Users\\hetland\\Desktop\\Invoice List 2014 WRK.csv')

