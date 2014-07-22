#!/usr/bin/python
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
import const

import sys
if '..//' not in sys.path:
    sys.path.append('..//')
    
from ahutils import pwd


# cfg = ConfigParser()
# 
# try:
#     cfg.read('./config.cfg')
# except IOError:
#     print "IOError"
#     cfg.read('../ahconfig/config.cfg')
#  
# finally:
#     const.host=cfg.get('host', 'host')
#     const.db_lst_dsn=cfg.get('database', 'database')
#     const.gui_user=cfg.get('user', 'user')
#     

#loading the menues from config

#id    menutitle    tablename    sql    view_type    pivothead    pivotrow    pivotvalue    gui_menu    comment    sorted    id_parent    username, , tbl_users_view.view_id
# const.gui_menues_tpl = [(1, 'menutitle', 'tablename', 'SQL', 'PIVOT', 'pivothead',  'pivotrow', 'pivotvalue', 'gui_menu', 'comment', 0, 0, 'ahetland', 0),
#                         
#                         ]

# const.db_lst_dsn=cfg.get('active_database', 'db_lst_dsn')
# 
# const.gui_user=cfg.get('user', 'gui_user')
# const.gui_pwd=decrypt(cfg.get('user', 'gui_pwd'), 'rccl')
# 
# const.conpath = cfg.get('path', 'conpath')
# 
# 
# const.alchemy_engine_rcldb = 'postgres://%s:%s@%s:5432/rcl_db' % (const.gui_user, const.gui_pwd, const.host)

const.SHEET_NAME = 'Sheet1'

const.host='192.168.1.91'
#const.host='localhost'

const.db_lst_dsn='lse_fin_db'
#const.db_lst_dsn='rpt_db_may'

 
const.gui_user='ahetland'
#const.pwd=pwd.pwd('hetland')
const.windows_pwd=pwd.pwd('hetland')


if __name__=='__main__':

    from wx_piv_app import main
    main(None)
    
