#!/usr/bin/python
# -*- coding: utf-8 -*-

#===============================================================================
# This is a new report sent by Frau Zindler
#===============================================================================

import os
import sys
import datetime
import re
import csv 



if '..//' not in sys.path:
    sys.path.append('..//')

from dbtable.datev import Datev
from ahutils.utils import randomString
random_str = randomString()

CSV_ROW = ['Nr','Abrechnungsmonat','Pers.Nr.','Name,Vorname','Abr-Monat','MA-Gruppe','Umsatz','Gegen-Kto','Bu-Text','Belegfeld','Kto','KSt','BuSatz','BuNr','Std','KtoGruppe','NBA']

from dbtable import datev

session = datev.getSession()

def importFile(FILE):
    
    reader = csv.reader(open(FILE, "rb"), delimiter=",")
    i=0
    
    #dic_with_sum_acc = {}  #a dictionary that holds the sum of the amounts over the datev accounts
    
    for row in reader:
       if i==0:
           assert row==CSV_ROW, "%s" % row
           i+=1
           pass
           
       else:
           #print "x", row[1]
           a, b = row[1].split('/')
           per_int = "%s%s" % (a, b)
           #print per_int
           
           new_datev = datev.Datev()
           new_datev.account_datev = "%s" % row[7]
           new_datev.soll = row[6]
           new_datev.haben = 0
           new_datev.period = per_int
           new_datev.gegenkonto = row[10]
           new_datev.pers_code = u"%05d" % int(row[2])
           
           new_datev.buchungstext = unicode(row[3], errors='ignore')
           new_datev.comment = unicode(row[8], errors='ignore')
           new_datev.comment_2 = u"Salary details from Lohn"
           new_datev.kost1 = unicode(row[11], errors='ignore')
           new_datev.imp_str = u"Salary-%s" % random_str
           new_datev.company = u"LSE Wages"
           new_datev.belegfeld1 = row[9]
           
           session.add(new_datev)
           
           contra_datev = new_datev.copy()
           
           contra_datev.haben = new_datev.soll
           contra_datev.soll = new_datev.haben
           contra_datev.pers_code = 0
           contra_datev.buchungstext = u'Contra'
           contra_datev.imp_str = u"Salary-%s" % random_str
           contra_datev.company = u"LSE Wages"
            
           session.add(contra_datev)

    session.commit()

if __name__=='__main__':
    import doctest
    doctest.testmod()
    
    importFile('C:\\Users\\hetland\\Desktop\\local_work\\imp2.csv')
