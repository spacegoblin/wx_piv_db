#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
wx.SetDefaultPyEncoding("utf-8")

#---------------------------
#here are some imports that are needed for files
#that are in the scripts directory
#import wx.html
#import matplotlib

import __version__
from exceptions import Exception

import os
import sys

if '.' not in sys.path:
    sys.path.append('.')

if '..' not in sys.path:
    sys.path.append('..')


import imp
import pprint

#pprint.pprint(sys.path)

#from flask.ext.sqlalchemy import SQLAlchemy
#try:
# from sqlalchemy import *
# from sqlalchemy import orm
#except: pass
import contextlib #did this as I dropped sqlalchemy in the dist folder and needed this import
import sets
import urlparse
import urllib
from ConfigParser import ConfigParser


import matplotlib
matplotlib.use('wxagg')
import pylab

print os.getcwd()

import wx_forms
import ahutils


import psycopg2

from psycopg2 import extras, extensions



#===============================================================================
# from sqlalchemy import *
# from sqlalchemy import orm
# #===============================================================================


import wx.lib.mixins.inspection

#------------------------
import exceptions

import ahgui.ssc_logo_3 as ssc_logo_2
   
        
####

def initDatabaseSelection(py_driver, odbc_dsn='Postgress', user=None, password=None):
    try:
        const.py_driver = py_driver
        const.odbc_dsn = odbc_dsn
    except:pass
    
    if password=='password':
        try:
            password = const.pwd
        except:pass

    Db = WhichDb_v3(const.py_driver, const.odbc_dsn, const.user, password)
    globals()['Db'] = Db
    return Db

def importCode(code,name,add_to_sys_modules=1):
    """
Import dynamically generated code as a module. code is the
object containing the code (a string, a file handle or an
actual compiled code object, same types as accepted by an
exec statement). The name is the name to give to the module,
and the final argument says wheter to add it to sys.modules
or not. If it is added, a subsequent import statement using
name will return this module. If it is not added to sys.modules
import will try to load it in the normal fashion.

import foo

is equivalent to

foofile = open("/path/to/foo.py")
foo = importCode(foofile,"foo",1)

Returns a newly generated module.
"""

    module = imp.new_module(name)
    
    #exec code in module.__dict__
    exec(code, module.__dict__)
    if add_to_sys_modules:
        sys.modules[name] = module

    return module



class DbSelectionFrm(wx.Frame):
    """Select any one of various databases."""
    def __init__(
            self, app, parent, ID=-1, title='Database selection', pos=wx.DefaultPosition,
            size=(300,300), style=wx.DEFAULT_FRAME_STYLE
            ):

        self.app = app

        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        wx.Frame.SetIcon(self, ssc_logo_2.getssc_logo_Icon())
        
        self.emergencyExit = False #when the form closes
                                   #OnExit is triggered, meaning you never get into the
                                   #app, hence this constant
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.nb = wx.aui.AuiNotebook(self)
        
        panel = wx.Panel(self.nb, -1)
        LEFT_POS_A = 2
        LEFT_POS_B = 50
        ROW_BLINE = 50
        self.connectionList = ['Postgress', 'Access', 'sqlite']
        wx.StaticText(panel, -1, 'Db driver', (LEFT_POS_A, ROW_BLINE))
        self.cb = wx.ComboBox(
            panel, -1, "Select DB type.", (LEFT_POS_B, ROW_BLINE),
            (150, -1), self.connectionList, wx.CB_DROPDOWN
            )
        self.cb.SetSelection(0)
        wx.StaticText(panel, -1, 'Db name', (LEFT_POS_A, ROW_BLINE+30))
        #self.t1 = wx.TextCtrl(panel, -1, xconfig.config.const.db_lst_dsn, pos=(LEFT_POS_B, ROW_BLINE+30), size=(125, -1))
        lst = const.db_lst_dsn.split(',')
        self.lst_dbname = [r.strip() for r in lst]
        self.cb2 = wx.ComboBox(
            panel, -1, "Select name.", (LEFT_POS_B, ROW_BLINE+30),
            (150, -1), self.lst_dbname, wx.CB_DROPDOWN
            )
        self.cb2.SetSelection(0)
        wx.StaticText(panel, -1, 'User', (LEFT_POS_A, ROW_BLINE+60))
        self.txt_usr = wx.TextCtrl(panel, -1, "user", pos=(LEFT_POS_B, ROW_BLINE+60), size=(125, -1))
        self.txt_usr.SetValue(const.gui_user)
        wx.StaticText(panel, -1, 'Password', (LEFT_POS_A, ROW_BLINE+90))
        self.txt_pwd = wx.TextCtrl(panel, -1, "password", pos=(LEFT_POS_B, ROW_BLINE+90), size=(125, -1),style=wx.TE_PASSWORD)
#         try:
#             self.txt_pwd.SetValue(const.gui_pwd)
#         except: pass
        
        self.button = wx.Button(panel, wx.NewId(), "Open database", pos=(LEFT_POS_B, ROW_BLINE+120))
        self.Bind(wx.EVT_BUTTON, self.OnSelectDb, self.button)
        
        self.Centre(wx.BOTH)
        
        panel_edit = wx.Panel(self.nb, -1)
        self.editButton = wx.Button(panel_edit, wx.NewId(), "Edit config.",
                                    pos=(LEFT_POS_B, ROW_BLINE+20))
        self.Bind(wx.EVT_BUTTON, self.OnEditConfig, self.editButton)
        
        self.nb.AddPage(panel, 'Database')
        self.nb.AddPage(panel_edit, 'Edit')
        
        panel.Fit()
        
    def OnEditConfig(self, event):
        print "Attempting: import editConfig"
        #from xconfig import editConfig
        import editConfig
        #app.mdi_parent_frame = None
        frame = editConfig.FrmTest(None)
        frame.Show(True)
                
    def OnSelectDb(self, event):
        busy = wx.BusyInfo("Establishing database connection...")
        odbc_dsn = self.lst_dbname[self.cb2.GetSelection()] #self.t1.GetValue()
        py_driver = self.connectionList[self.cb.GetSelection()]

        pwd = self.txt_pwd.GetValue()
        if pwd=='password':
            pwd = const.pwd
        
        user = self.txt_usr.GetValue()
        try:
            const.gui_version = __version__.version
            const.user = user
        except: 
            
            pass
        
        initDatabaseSelection(py_driver, odbc_dsn, user, pwd)
        self.emergencyExit = True


        self.OnInit2()
    
        self.Destroy()
                    
        self.Close()
        
    def OnInit2(self):
        print "OnInit2"
        frame = MDIPFrame(App, const.odbc_dsn, const.gui_version)
        frame.Show(True)
        self.app.mdi_parent_frame = frame
        self.app.SetTopWindow(frame)
        self.app.db_name = str(const.odbc_dsn)

        return True

    def OnExit(self, evt):
        if not self.emergencyExit:
            app = wx.GetApp()
            app.OnExit()
        else:
            #print "self.Close"
            self.Destroy()


class LoadFromFileMDIChild(wx.MDIChildFrame):
    def __init__(self, parent):
        wx.MDIChildFrame.__init__(self, parent, -1, 'child')
        
        self.parent = parent
        self.panel = wx.Panel(self, -1)
        wx.StaticText(self.panel, -1, 'Base table', (5, 10))
        self.ctrTbl = wx.TextCtrl(self.panel, -1, 'base database table', size=(150, 20),pos=(60, 10))
        
        wx.StaticText(self.panel, -1, 'Sheet', (5, 30))
        self.ctrSheet = wx.TextCtrl(self.panel, -1, 'Sheet1', size=(150, 20),pos=(60, 30))
        
        wx.StaticText(self.panel, -1, 'File', (5, 50))
        self.ctrPath = wx.TextCtrl(self.panel, -1, 'path', size=(150, 20),pos=(60, 50))
        
        btnPath = wx.Button(self.panel, wx.NewId(), "...select", size=(50, 20), pos=(210, 50))

        self.Bind(wx.EVT_BUTTON, self.OnClickBtnDownload, btnPath)

        self.btnPathSelect = wx.Button(self.panel, wx.NewId(), "Load - xls", size=(150, 20), pos=(60, 75))

        self.Bind(wx.EVT_BUTTON, self.OnMakeFrm, self.btnPathSelect)
        self.path = None
        
        self.btnLoadCsv = wx.Button(self.panel, wx.NewId(), "Load - csv", size=(150, 20), pos=(60, 100))
        self.Bind(wx.EVT_BUTTON, self.OnLoadCsv, self.btnLoadCsv)
        
        
    def OnMakeFrm(self, event):
        
        from ahutils.record import loadFromFile
        #def loadFromFile(file, sheet='Sheet1', basetable='No db table - xls'):
        
        basetable = self.ctrTbl.GetValue().strip()
        sheet = self.ctrSheet.GetValue().strip()
        if not self.path:
            self.path = self.ctrPath.GetValue().strip()
            

        lst = loadFromFile(self.path, sheet, basetable)
        frame = Frm(self.parent, lst, self.path)
        frame.Show(True)
        
        #TODO: should reintroduce this when bug by AK is found
        
#         try:
#             wx.BeginBusyCursor()
#             lst = loadFromFile(self.path, sheet, basetable)
#             frame = Frm(self.parent, lst, self.path)
#             frame.Show(True)
# 
#         except:
# 
#             dlg = wx.MessageDialog(None, '''Check the parameters for excel.''',
#                                'Excel did not load!',
#                                wx.OK | wx.ICON_INFORMATION)
#             dlg.ShowModal()
#             dlg.Destroy()
#         finally:
#             wx.EndBusyCursor()

                    
    def OnLoadCsv(self, event):
        from ahutils.record import loadFromFileCsv
        basetable = self.ctrTbl.GetValue().strip()

        if not self.path:
            self.path = self.ctrPath.GetValue().strip()
        try:
            wx.BeginBusyCursor()
            lst = loadFromFileCsv(self.path, basetable)
            frame = Frm(self.parent, lst, self.path)
            frame.Show(True)

        except:

            dlg = wx.MessageDialog(None, '''Check the parameters for the file.''',
                               'File did not load!',
                               wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            wx.EndBusyCursor()
            event.Skip()
    
    def OnClickBtnDownload(self, event):
        dlg = wx.FileDialog(self, message="Select file to load ...",
                            wildcard="*", style=wx.OPEN)
        #dlg.SetFilename(self.lstFileNames[self.lstBox.GetSelection()][1])
        
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            self.path = dlg.GetPath()
            self.ctrPath.SetValue(self.path)
            #self.doMakeFrm(path)
            wx.EndBusyCursor()
        dlg.Destroy()


class AppMenues(object):
    def __init__(self):
        self.idname = wx.NewId()
        self.view_id = None
        self.menutitle = None
        self.tablename = None
        self.sql = None
        self.view_type = None
        self.gui_menu = None
        self.comment = None       
        self.username = None
        self.pivot = False
        self.pivothead = None
        self.pivotrow = None
        self.pivotvalue = None
        self.sorted = None


        
class AppSettings(object):
    """Class that holds the application settings.
    These are collected from the database."""
    def __init__(self):
        self.settings = {}  #event.Id and AppMenues() instance
        self.dic_gui_menu = {}  #rec.gui_menu = wx.Menu()
        

    def __call__(self, eventId, atr):
        """Returns the AppMenues attribute of that particular menu id"""
        return getattr(self.settings[eventId], atr)
    
    def loadMenu(self):
        "loads the menu, step one."
        
        sql = """SELECT tbl_views.*, tbl_users.username
FROM tbl_views INNER JOIN tbl_users_view ON tbl_views.id = tbl_users_view.view_id
INNER JOIN tbl_users ON tbl_users_view.user_id = tbl_users.id
WHERE tbl_users.username='%s' order by tbl_views.sorted""" % const.user

        lst = loadFromDb(sql)
        
        for rec in lst:
            self.dic_gui_menu[rec.gui_menu] = wx.Menu()
                      
class MDIPFrame(wx.MDIParentFrame):
    def __init__(self, app, db_name, gui_version):
        wx.MDIParentFrame.__init__(self, None, -1, "SSC - LSE Space - %s %s" % (db_name, gui_version),
                                   size=(780,500))
        self.app = app

        mb = self.MakeMenuBar()
        self.SetMenuBar(mb)
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        Db.db_name = const.odbc_dsn
        wx.MDIParentFrame.SetIcon(self, ssc_logo_2.getssc_logo_Icon())
        
    def addMenuItem(self, title, method, helpText='', options=None):
        id_ = wx.NewId()
        if options:
            self.menu.Append(id_, title, helpText, options)
        else:
            self.menu.Append(id_, title, helpText)
        self.Bind(wx.EVT_MENU, method, id=id_)
        return id_
                        
    def MakeMenuBar(self):
        self.menu = menu = wx.Menu()


        self.addMenuItem('Crust', self.OnCrust, 'A shell window')

        self.addMenuItem('&Redirect Output', self.OnToggleRedirect,
                         'Redirect print statements to a window', wx.ITEM_CHECK)
        
        self.addMenuItem('Load from File', self.OnFrmLoadFromFile, 'Load an csv or xls file.')

        self.addMenuItem('Scripts', self.OnLoadScripts, 'Load installed scripts')
        
        self.addMenuItem('Options', self.OnLoadOptions, 'Set options')
        
        self.addMenuItem('Exit', self.OnExit, 'Quit')

          
         
        ## next menu
        self.menu2 = menu2 = wx.Menu()
                
        self.menu4 = menu4 = wx.Menu()
        
        self.dicCallSQL = AppSettings()
        
        #self.dic_gui_menu = {}
        
        self.dicCallSQL.loadMenu()
        
        #self.dicCallSQL = {} #dictionaries with the sql statements
        

        self.loadMenuBarFromSQL()
        ## end the munes
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(menu, "File")

        for key, val in self.dicCallSQL.dic_gui_menu.items():
            self.menuBar.Append(val, str(key))
        
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Database - %s DSN: %s" % (const.py_driver, const.odbc_dsn), 0)
        
        return self.menuBar
    

                    
    def loadMenuBarFromSQL(self):
        
        sql = """SELECT tbl_views.*, tbl_users.username, tbl_users_view.view_id
FROM tbl_views INNER JOIN tbl_users_view ON tbl_views.id = tbl_users_view.view_id
INNER JOIN tbl_users ON tbl_users_view.user_id = tbl_users.id
WHERE tbl_users.username='%s' order by tbl_views.sorted""" % const.user
                  
        lst = loadFromDb(sql)
        
        for rec in lst:
            mnuobj = AppMenues()

            #mnuobj.idname = wx.NewId()
            mnuobj.view_id = rec.id
            mnuobj.menutitle = rec.menutitle
            mnuobj.sql = rec.sql
            mnuobj.tablename = rec.tablename
            mnuobj.gui_menu = rec.gui_menu
            mnuobj.comment = rec.comment
            
            if rec.view_type=='PIVOT':
                mnuobj.pivot = True
                _pivothead = rec.pivothead.split(',')
                #strip the field for space
                mnuobj.pivothead = [r.strip() for r in _pivothead]
    
                _pivotrow = rec.pivotrow.split(',')
                #strip the field for space
                mnuobj.pivotrow = [r.strip() for r in _pivotrow]
                
                mnuobj.pivotvalue = rec.pivotvalue
                #use the id to find the sql to use
                self.Bind(wx.EVT_MENU, self.OnShowSqlData, id=mnuobj.idname)
            elif rec.view_type=='EXECUTE':
                #print "selecting to execute"
                mnuobj.pivot = False
                self.Bind(wx.EVT_MENU, self.OnExecuteMenuCode, id=mnuobj.idname)
            else:
                mnuobj.pivot = False
                self.Bind(wx.EVT_MENU, self.OnShowSqlData, id=mnuobj.idname)

            self.dicCallSQL.settings[mnuobj.idname] = mnuobj
            self.dicCallSQL.dic_gui_menu[mnuobj.gui_menu].Append(mnuobj.idname, mnuobj.menutitle)
            
                   
        


    def OnShowSqlData(self, event):
        """Execute the sql stored in menu.xml and display
the data grid Frm(). This method is attached to the
the event method of the menu item."""

        busy = wx.BusyInfo("Retrieving data...")
        wx.BeginBusyCursor()
                
        sql = str( self.dicCallSQL(event.Id, 'sql') )
        tbl = str( self.dicCallSQL(event.Id, 'tablename') )
        pivot_bol = self.dicCallSQL(event.Id, 'pivot') 
        menutitle = self.dicCallSQL(event.Id, 'menutitle')

        lst = loadFromDb(sql, tbl)
        if lst:
            lst.view_id = self.dicCallSQL(event.Id, 'view_id')
            
            lst.loadExecCode()
    
            if pivot_bol:
                pivot_head = self.dicCallSQL(event.Id, 'pivothead') 
                pivot_row = self.dicCallSQL(event.Id, 'pivotrow') 
                pivot_amount = self.dicCallSQL(event.Id, 'pivotvalue') 
    
                lst.pivot(pivot_row, pivot_head, pivot_amount)
    
            frame = Frm(self, lst, menutitle)
        else:
            frame = False
            
        wx.EndBusyCursor()

        if frame:
            frame.Show(True)
            
    def OnExecuteMenuCode(self, event):
        "Executes the code that has been stored in the menu / views table."

           
        busy = wx.BusyInfo("Executing ...")
        
        wx.BeginBusyCursor()
        
        sql = str(getattr(self.dicCallSQL.settings[event.Id], 'sql'))
        tbl = str(getattr(self.dicCallSQL.settings[event.Id], 'tablename'))
        pivot_bol = getattr(self.dicCallSQL.settings[event.Id], 'pivot')
        menutitle = getattr(self.dicCallSQL.settings[event.Id], 'menutitle')
        
        try:
            exec( sql.strip() )

        except:
            #exec( sql.strip() )
            print "Error while executing"
        
        finally:
            wx.EndBusyCursor()


    def OnLoadDatevKontoBlatt(self, event):
        """Insert DATEV Kontoblatt file into the database."""
        default_dir = 'C:\Users\hetland\Documents'
        default_file = '*.csv'
        wildcard = "csv files (*.csv)|*.csv|" \
                    "xls files (*.xlsx)|*.xlsx|" \
                    "All files (*.*)|*.*"

        dialogue = wx.FileDialog(None, "Select file", default_dir,
                               default_file, wildcard, wx.OPEN)
        
        if dialogue.ShowModal() == wx.ID_OK:
            
            progressMax = 100
            prog_dial = wx.ProgressDialog("Inserting data",
                                          "Please wait...",
                                          progressMax,
                                          style = wx.PD_ELAPSED_TIME
                                          | wx.PD_REMAINING_TIME)
            keepGoing = False
            didDelete = False
            
            filestr = dialogue.GetPath()
            from ahutils.data_feed_datev_01 import doInsertKontoBlatt
            #didDelete = doDelete()
            didDelete = True
            if didDelete:
                prog_dial.Update(50)
            keepGoing = doInsert(filestr)
            if keepGoing:
                prog_dial.Destroy()
            
        dialogue.Destroy()
        
        
    def OnFrmLoadFromFile(self, event):
        frame = LoadFromFileMDIChild(self)
        frame.Show(True)
        
    def OnCrust(self, event):
        from wx import py
        frame = py.crust.CrustFrame()
        frame.Show()

    def OnToggleRedirect(self, event):
        app = wx.GetApp()
        if event.Checked():
            app.RedirectStdio()
            print "Print statements and other standard output will now be directed to this window."
        else:
            app.RestoreStdio()
            print "Print statements and other standard output will now be sent to the usual location."

    def OnExit(self, evt):
        print "OnExit"
        app = wx.GetApp()
        app.OnExit()

    def OnLoadScripts(self, evt):
# sys.path.append('.\\scripts')
        import Main
        frame = Main.wxPythonDemo(self, "App: (Scripts)")
        frame.Show(True)
        evt.Skip()
        #frame.Maximize()
        
    def OnLoadOptions(self, evt):

        from wx_forms import FrmOptions
        frame = FrmOptions(self)
        frame.Show()
        evt.Skip()


       
class App(wx.App):
    
    MY_FLOAT_FORMAT = ',.2f'
    MY_DECIMAL_FORMAT = ',.2f'
    MY_DATE_FORMAT = '%Y-%m-%d' #'%b %d, %Y'
    
    def __init__(self, redirect=True, filename=None):
        wx.SetDefaultPyEncoding('utf-8')

        wx.App.__init__(self, redirect, filename)
        self.mdi_parent_frame = None
        self.app_dic_lst = {} #central lists that are loaded
        self.dic_Usefull = {} #None
        self.db_name = None
        
        
    def OnInit(self):
        
        #wx.BeginBusyCursor()
        
        wx.SystemOptions.SetOptionInt("mac.window-plain-transition", 1)
        #set to unicode
        
        print wx.PlatformInfo

        #import sys
        #print "module wx_rccl in OnInit(): sys.getdefaultencoding()", sys.getdefaultencoding()
        reload (sys)
        sys.setdefaultencoding('utf-8')
        print sys.getdefaultencoding()
            

            
        frame = DbSelectionFrm(self, None)
        frame.Show(True)
        frame.Raise()
        #wx.EndBusyCursor()
        
        return True
    
    def initScript(self):
        """Imports and executes the init script in the
script module with the db name. The file has hence the
name init_xx.py where xx is the driver name dsn.
called from OnInit2 above after db has been selected."""
# print "initScript"
# import pprint

        sys.path.append('%s\\scripts' % os.getcwd())
        
        name = 'init_%s' % self.db_name
        import scripts
        
        try:
            __import__('scripts', fromlist=[name,])
        except:
            print "No module on start up imported"
        
 
    def OnExit(self):
        print "Exiting from App class"
# if globals().has_key('Db'):
# del globals()['Db']
# print "globals()['Db']"
        from sys import exit
        exit()
        self.Destroy()
        
    
def main(argv):
    "Can be used in module or run from command."
    try:
        sys.path.append(argv[0])
    except:
        pass
    
    finally:
        pprint.pprint( sys.path )

    from ahconfig import const
        
    from ahutils.record import loadFromDb, WhichDb_v3
    
    from wx_forms import Frm, GenericMsgDlg
    
    global const, loadFromDb, WhichDb_v3, Frm, GenericMsgDlg #, GuiDbVersion MyUser,

    app = App(False)
    #app = App(True, 'C:\\Users\\111625\\Desktop\\temp\\redirect_wx_rccl.txt')
    #app = App(True)
    app.MainLoop()

if __name__=='__main__':
    
    
    main(None)

