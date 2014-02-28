#!/usr/bin/python
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
import const
#from ahutils import decrypt


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


    
# const.db_lst_dsn=cfg.get('active_database', 'db_lst_dsn')
# 
# const.gui_user=cfg.get('user', 'gui_user')
# const.gui_pwd=decrypt(cfg.get('user', 'gui_pwd'), 'rccl')
# 
# const.conpath = cfg.get('path', 'conpath')
# 
# 
# const.alchemy_engine_rcldb = 'postgres://%s:%s@%s:5432/rcl_db' % (const.gui_user, const.gui_pwd, const.host)
const.host='192.168.1.91'
#const.host='localhost'

const.db_lst_dsn='lse_fin_db'
#const.db_lst_dsn='new_db'
 
const.gui_user='ahetland'
#const.gui_pwd=decrypt('camilla', 'rccl')
#const.gui_pwd=('isabelle')

if __name__=='__main__':
    import sys
    sys.path.append('..//')
    from wx_piv_app import main
    main(None)
    
