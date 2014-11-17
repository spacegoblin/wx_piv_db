#!/usr/bin/python
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
import const

import sys
if '..//' not in sys.path:
    sys.path.append('..//')
    
from ahutils import pwd

const.SHEET_NAME = 'Sheet1'     #'Tabelle1' this can cause annoying error 

#const.host='192.168.1.91'
const.host='localhost'

#const.db_lst_dsn='lse_fin_db'
const.db_lst_dsn='new_db2'
#const.db_lst_dsn='ah_db'

const.gui_user='ahetland'
const.pwd=pwd.pwd('hetland')

const.windows_pwd=pwd.pwd('hetland')


if __name__=='__main__':

    from wx_piv_app import main
    main(None)
    
