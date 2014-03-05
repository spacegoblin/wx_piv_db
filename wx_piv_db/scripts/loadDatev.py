#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import datetime

import sys
if '..//' not in sys.path:
    sys.path.append('..//')
    
from ahutils.utils import randomString
from ahconfig import const
const.random_str = randomString()


from ahutils import db
db.setQuote('Postgress')

pwd = raw_input ("Enter password: ")

DB = db.This_Db(const.db_lst_dsn, 'ahetland', pwd)
DB = db.This_Db(const.db_lst_dsn, 'ahetland', )



raise

CSV_ROW = ['BL', 'Kontonummer', 'Datum', 'BU', 'Gegenkonto', 'Buchungstext', 'USt%', 'Belegfeld1', 'Umsatz Soll', 'Umsatz Haben', 'WKZ', 'Eingabebetrag', 'Kurs', 'Stapel-Nr.', 'BSNr.', 'HK', 'KOST1']
        #   0         1            2      3          4              5           6          7             8               9          10          11          12          13        14       15    16
        

def helper(x):
    try:
        return datetime.datetime.strptime(x, '%d.%m.%Y')
    except: return None
    
def helpMonth(stapelNr):
    return stapelNr[3:7] + stapelNr[0:2]
                    
def run(FILE):
    """Insert a datev file into the database"""
                    
    reader = csv.reader(open(FILE, "rb"), delimiter=",")
    i=0
    lst = []
    try:
        for row in reader:
            dict_ = {}
            if i==0:
                assert row==CSV_ROW, "%s" % row
                

            else:

            
            #id        kontobezeichnung_not_mdata    tmp    id_parent        foreign_amount    comment       
            #zui    comment_2
            
                 #dict_['xx'] = row[0]
                dict_['account_datev'] = row[1]
                dict_['datum'] = helper( row[2] )
                dict_['bu'] = row[3]
                dict_['gegenkonto'] = row[4]
                print row[5]
                dict_['buchungstext'] = unicode(row[5], errors='ignore')  #.decode('utf-8').encode('utf-8')
                dict_['ust'] = row[6]
                dict_['belegfeld1'] = row[7]
                dict_['soll'] = row[8].replace(',', '')
                dict_['haben'] = row[9].replace(',', '')
                dict_['wkz'] = row[10]
                #dict_['xx'] = row[11]
                dict_['kurs'] = row[12]
                dict_['stapel_nr'] = row[13]
                dict_['bsnr'] = row[14]
                dict_['hk'] = row[15]
                dict_['kost1'] = row[16]
                
                dict_['period'] = helpMonth( dict_['stapel_nr'] )
                dict_['company'] = 'LSE HGB'
                dict_['imp_str'] = const.random_str
                
                sql = db.dictToInsert(dict_, 'tbl_susa')
                
                DB.c.execute(sql)
                DB.cnn.commit()
                
            i+=1         

    except csv.Error, e:
        print 'line %d: %s' % (reader.line_num, e)
        raise
    


if __name__ == '__main__':
    
    PATH='Z:/Reporting/2014/02-Feb/v01/imp.csv'

    run(PATH)
    raise
    run(PATH)
