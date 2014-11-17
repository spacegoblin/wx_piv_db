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

from dbtable import Base, getLocalSession


def fixNumber(str_amnt):
    "Helper method to fix the amount string into float."
    print "fixNumber ", str_amnt
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
    return datetime.datetime.strptime(st, '%m/%d/%Y')


class Bank(Base):
    """Banking data"""

    __tablename__ = 'tbl_bank'
    
    #Booking date;Value date;Transaction Type;Beneficiary / Originator;Payment Details;IBAN;BIC;Customer Reference;Mandate Reference;Creditor ID;Compensation amount;
    #Original Amount;Ultimate creditor;Debit;Credit;Currency
    id = Column(Integer, primary_key=True)
    booking_date = Column(Date,)
    value_date = Column(Date,)
    transaction_type = Column(Unicode(255), )
    beneficiary = Column(Unicode(255), )
    payment_details = Column(Unicode(255), )
    iban = Column(Unicode(255), )
    bic = Column(Unicode(255), )
    customer_reference = Column(Unicode(255), )
    mandate_reference = Column(Unicode(255), )
    creditor_id = Column(Unicode(255), )
    compensation_amount = Column(Unicode(255), )
    original_amount = Column(Unicode(255), )
    ultimate_creditor = Column(Unicode(255), )
    _debit = Column('debit', NUMERIC(20,2),)
    _credit = Column('credit', NUMERIC(20,2),)
    currency = Column(String(255), )
    _period = Column('period', Integer, )
    account = Column(Unicode(255), )
    _amount = Column('amount', NUMERIC(20,2),)
    #id_parent
    account_grp = Column(Unicode(255), )
    
    def setDebit(self, v):
        self._debit=float(v)
    def getDebit(self):
        return self._debit
    debit = property(getDebit, setDebit)

    def setCredit(self, v):
        self._credit=float(v)
    def getCredit(self):
        return self._credit
    credit = property(getCredit, setCredit)
    
    def getAmount(self):
        return self._amount
    def setAmount(self, v):
        self._amount = self.debit + self.credit
    amount = property(getAmount, setAmount)
    
    def getPeriod(self):
        return self._period
    def setPeriod(self, v):
        self._period = v
    
    period = property(getPeriod, setPeriod)
    
    fieldnames = ['id', 'account_grp', 'account', 'period', 'amount', 'value_date', 'booking_date', 'payment_details']
 
        
    def __str__(self):
        """Return string representation"""        
        return "%s %s %s Amount: %s for %s" % (self.id, self.debit, self.credit, self.amount, self.period)  
    
    def OnRecordDblClick(self, event, fild):
        pass
    
    def update(self):
        raise
 
str="""Voucher date;Date of receipt;Reason for payment;Foreign currency;Amount;Exchange rate;Amount;Currency

['Booking date', 'Value date', 'Transaction Type', 'Beneficiary / Originator', 'Payment Details', 'IBAN', 'BIC', 'Customer Reference', 'Mandate Reference', 'Creditor ID', 'Compensation amount', 'Original Amount', 'Ultimate creditor', 'Debit', 'Credit', 'Currency']

"""
def importCreditFile(period, FILE):
    #Voucher date;Date of receipt;Reason for payment;Foreign currency;Amount;Exchange rate;Amount;Currency
    session = getLocalSession()
    
    reader = csv.reader(open(FILE, "rb"), delimiter=";")
    i=0
    lst = list(reader)
    lngt = len(lst)

    
    for row in lst:
       if i==0:
           #assert row==CSV_ROW, "%s" % row
           i+=1
           pass
       if i==lngt:
           #last row
           continue
       if i<=5:
           i+=1
           continue
           

       else:
           print row
           b = Bank()
           b.booking_date = dateFromStr( row[0] )
           b.value_date = dateFromStr( row[1] )
           b.payment_details = unicode(row[2], errors='ignore')
           b.debit = fixNumber(row[6])
           b.credit = fixNumber(row[6])*-1
           b.currency = unicode(row[7], errors='ignore')
           b.period = period
           b.amount = 0
           b.account=u'Visa abrechnung'
           b.account_grp = 'Visa'
           session.add(b)

           i+=1
       
       session.commit()




def importFile_v02(FILE):
    """Different file defs.
    Booking date;Value date;Transactions Payment details;Debit;Credit;Currency

    """
    session = getLocalSession()
    
    reader = csv.reader(open(FILE, "rb"), delimiter=";")
    i=0
    lst = list(reader)
    lngt = len(lst)

    
    for row in lst:
       print row
       if i==0:
           #assert row==CSV_ROW, "%s" % row
           i+=1
           pass
       if i==lngt:
           #last row
           continue
       if i<=5:
           i+=1
           continue
       
       else:
           
           b = Bank()
           b.booking_date = dateFromStr( row[0] )
           b.value_date = dateFromStr( row[1] )
           #b.transaction_type = unicode(row[2], errors='ignore')
          # b.beneficiary = unicode(row[3], errors='ignore')
           b.payment_details = unicode(row[4], errors='ignore')
           #b.iban = unicode(row[5], errors='ignore')
           #b.bic = unicode(row[6], errors='ignore')
           #b.customer_reference = unicode(row[7], errors='ignore')
           #b.mandate_reference = unicode(row[8], errors='ignore')
           #b.creditor_id = unicode(row[9], errors='ignore')
           #b.compensation_amount = unicode(row[10], errors='ignore')
           #b.original_amount = unicode(row[11], errors='ignore')
           #b.ultimate_creditor = unicode(row[12], errors='ignore')
           b.debit = fixNumber(row[13])
           b.credit = fixNumber(row[14])
           #print "14", fixNumber(row[14]), b.credit
           b.currency = unicode(row[15], errors='ignore')
           b.period = "%d%02d" % (b.value_date.year, b.value_date.month)
           b.amount = 0
           b.account_grp = 'Bank'
        
           session.add(b)

           i+=1
       
       session.commit()
                  
def show():
    session = getLocalSession()
    
    qry = session.query(Bank)
    from ahutils import record
    from wx_forms import Frm2
    
    lst = record.loadFromAlchemy(qry, Bank)
    
    lst.pivot(['account_grp', 'account'], ['period'], 'amount')
    
    import wx

    wx.SetDefaultPyEncoding('utf-8')
    app = wx.App()
    app.MY_DATE_FORMAT = '%d.%m.%Y'
    frame = Frm2(None, lst)
    frame.Show()

    app.MainLoop() 
    


    
if __name__=='__main__':

    
    import doctest

    doctest.testmod()
    show()
    #importFile_v02('C:\\Users\\hetland\\Documents\\Office\\MyOffice\\Bank\\Transactions_111_400798500_20140916_103247.csv')
    #importCreditFile(201407, 'C:\\Users\\hetland\\Documents\\Office\\MyOffice\\Bank\\visa\\CreditCardTransactions4779131110003542_2014_07(6).csv')
