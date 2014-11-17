#!/usr/bin/python
# -*- coding: utf-8 -*-

#===============================================================================
# You can either run db_setup.sql with the SQL commands that will create the database tables
# or you can run this script which does the same, but uses the application itself to 
# set everything up.
#===============================================================================

import sys, pprint
sys.path.append('..')
pprint.pprint(sys.path)

from ahconfig import const

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dbtable import Base, getSession

from dbtable.gui import GuiUSer, GuiUserView, GuiUserView, GuiEval, GuiView, ExampleAlchemy
from dbtable.gui import addView, addUser, addUserToView

def setUp():

    from ahutils import pwd
    a=GuiUSer()
    b=GuiUserView()
    c=GuiUserView()
    d=GuiEval()
    e=GuiView()
    f = ExampleAlchemy()
    
    engine = create_engine("postgresql+psycopg2://%s:%s@/%s?host=%s" % (const.gui_user, const.windows_pwd, const.db_lst_dsn, const.host))  
    
    #This will create the database table if not created already
    Base.metadata.create_all(engine)
    


def initData():
    addView()
    uid = addUser(const.gui_user)
    addUserToView(uid)

def createExamppleData():
    import random
    m = ExampleAlchemy()
    session = m.session
    
    for q in xrange(200):
    
        for i in m.exampleYear():
            n = ExampleAlchemy()
            n.period = i
            n.account = random.choice( n.exampleAccountList() )
            n.costcenter = random.choice( n.exampleCostCenterList() )
            n.amount = random.randint(1,1000)
            n.description = u'A random generated amount'
            session.add(n)
        
    session.commit()
        
def run():
    "Run the main program from here."
    import sys
    from wx_piv_app import main
    main(sys.argv)

if __name__=='__main__':

    setUp()
    initData()
    createExamppleData()
    run()