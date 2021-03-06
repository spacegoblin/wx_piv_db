#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx
import wx.lib.agw.genericmessagedialog as GMD
print wx.version() 
import wx.aui
from mygridtable_v2 import MyGridTable #, MyGridTableAlchemy
import wx.lib.gridmovers as gridmovers
from ahutils.record import loadFromDb, GUICodeNotExisting
from ahconfig import const
import datetime
#from mx.DateTime.DateTime import DateTimeType
import datetime
import os
import exceptions

import operator

from ahgui import piv_ico

import ahgui.ssc_logo_3 as ssc_logo_2

SHEET_NAME = const.SHEET_NAME

##from pytesser import *
#from PIL import Image
##import pyPdf
#import tempfile



def getPDFContent(tmpfile):
    content = []
    # Load PDF into pyPDF
    pdf = pyPdf.PdfFileReader(file(tmpfile, "rb"))
    # Iterate pages

    for i in range(0, pdf.getNumPages()):
        str = ( pdf.getPage(i).extractText() + "\n" )
        #str = str.replace("\xa0", " ").strip().split()
        str = str.replace("\xa0", " ").split()
        #print str
        content.append( " ".join(str) )
        content.append( "\n\n" )

    return " ".join(content)
        
#import sys


### -Uitlities- ###
def GenericQuestionDlg(message, caption, default=''):
    
    dlg = wx.TextEntryDialog(None, message, caption, default)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        val = dlg.GetValue()
        dlg.Destroy()
        return val #dlg.GetValue()
    else:
        dlg.Destroy()
        return None

def GenericMsgDlg(message='Message', caption='Caption', styles=wx.OK | wx.ICON_INFORMATION):
    """
Create a message dialog with the passed in parameters
"""
    dlg = wx.MessageDialog(None, message, caption, styles)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result



def getXlsImage():
    "Put a nice icon on the form"
    #print xls
    bmp = piv_ico.getxlsBitmap()
    #bmp.Rescale(18,18)
    return bmp

def FrmShow(parent, lst):
    "Shows the data -lst- in a shell in a new Window."
    frame = Frm(parent, lst)
    frame.Show(True)

def _getObjAttr(obj, label):
    "Utility for text in wx"
    try:
        txt = getattr(obj, label)
    except AttributeError:
        txt = 'no attr' #return False #'The field does not exist'
    if type(txt) == datetime.datetime:
        txt = txt.strftime('%Y-%m-%d')
# elif type(txt)== DateTimeType:
# txt = txt.strftime('%Y-%m-%d')
    if not txt:
        txt = ''
    return txt

class CtrWCloseUtil(object):
    """Bundeled the accelerator table here for inheritance."""
    def __init__(self):
        ID_CLOSE = wx.NewId()
        wx.EVT_MENU(self, ID_CLOSE, self.OnClose)
        acceltbl = wx.AcceleratorTable( [(wx.ACCEL_CTRL, ord('W'),
                                        ID_CLOSE)] )
        self.SetAcceleratorTable(acceltbl)

    def OnClose(self, event):
        self.Close()
        event.Skip()
                        
### -The Grid- ###
class MyGrid(wx.grid.Grid):
    def __init__(self, parent, lst, dataCols=None):
        wx.grid.Grid.__init__(self, parent, -1)
        self.parent = parent
        assert lst is not None
        self.onInit(lst, dataCols)
        
        
    def onInit(self, lst, dataCols):
        self.lst = lst
        #refactored this to include self.table
        self.table=MyGridTable(lst) #, dataCols)
        
        self.SetTable(self.table, True)

        self.SetRowLabelSize(20)
        self.SetMargins(0,0)
        self.AutoSizeColumns(False)
        self.SetDefaultCellOverflow(False)
       # self.SetColFormatFloat(3, -1, 2)
       
       
        #mapping keys to behave different.
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        #self.Fit()
        
        self.Bind(wx.grid.EVT_GRID_CMD_LABEL_LEFT_CLICK, self.OnClickCol)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightClick)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnUpdate_v03)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnRightClickCol)
        
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLblLeftDbClick)
        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)

        self.Bind(wx.grid.EVT_GRID_CMD_CELL_LEFT_DCLICK, self.OnDoubleClickCellLeft)
        #self.Bind(wx.grid.EVT_GRID_CELL_BEGIN_DRAG, self.OnBeginDrag)
        
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnClickCellLeft)
        
        
        #popup menu
        self.menuPop = m = wx.Menu()
        #a = m.Append(-1, "Data")
        b = m.Append(-1, "Search data")
        c = m.Append(-1, "Append copy")
        d = m.Append(-1, "Set filter")
        #e = m.Append(-1, "Insert")
        f = m.Append(-1, "SQL query")
        g = m.Append(-1, "Single view")
        h = m.Append(-1, "Update column")
        i = m.Append(-1, "Update by group id")
        #id_i = wx.NewId()
        #i = m.Append(id_i, "Eval code ...")
        sub_i = wx.Menu()
        self.dicCodeExecIds = {}
        if self.lst.dicExecCode:
            m.AppendSeparator()
            for key in self.lst.dicExecCode.keys():
                
                id_sub_i = wx.NewId()
                sub_i.Append(id_sub_i, key)
                self.dicCodeExecIds[id_sub_i]=key
                self.Bind(wx.EVT_MENU, self.OnEvalCode, id=id_sub_i)
                
            m.AppendMenu(-1, "Go do ...", sub_i)
            
        #Math capabilities
        m.AppendSeparator()
        sub_math_menue = wx.Menu()

        id_sub_math_add = wx.NewId()
        sub_math_menue.Append(id_sub_math_add, 'Add to number')
        self.Bind(wx.EVT_MENU, self.OnAddNumber, id=id_sub_math_add)
        
        id_sub_math_sub = wx.NewId()
        sub_math_menue.Append(id_sub_math_sub, 'Subtract from number')
        self.Bind(wx.EVT_MENU, self.OnSubtractNumber, id=id_sub_math_sub)

        id_sub_math_frm = wx.NewId()
        sub_math_menue.Append(id_sub_math_frm, 'Increment by 1')
        self.Bind(wx.EVT_MENU, self.OnIncByOne, id=id_sub_math_frm)
        
        
        id_sub_math_commit = wx.NewId()
        sub_math_menue.Append(id_sub_math_commit, 'Commit to DB')
        self.Bind(wx.EVT_MENU, self.OnCommitToDb, id=id_sub_math_commit)
                        
        
        m.AppendMenu(-1, "Math ...", sub_math_menue)
          
        #self.Bind(wx.EVT_MENU, self.OnDoSmth, a)
        self.Bind(wx.EVT_MENU, self.OnSearch, b)
        self.Bind(wx.EVT_MENU, self.OnAppendCopy, c)
        self.Bind(wx.EVT_MENU, self.OnSetFilterTo, d)
        #self.Bind(wx.EVT_MENU, self.OnInsert, e)
        self.Bind(wx.EVT_MENU, self.OnSQLQuery, f)
        self.Bind(wx.EVT_MENU, self.OnSingleForm, g)
        self.Bind(wx.EVT_MENU, self.OnUpdateColForm, h)
        self.Bind(wx.EVT_MENU, self.OnUpdateColFormGroup, i)
        
        
        #column menu
        self.menuColPop = m = wx.Menu()
        self.sorter = m.Append(-1, "Sort")
        m.AppendSeparator()
        #the rows
        self.rowDelete = m.Append(-1, " ")   #Remove Row
        self.rangeDelete = m.Append(-1, " ")  #Remove Range
        #spacer
        m.AppendSeparator()
        #the columns
        self.columnDelete = m.Append(-1, "Remove Column")  
        #spacer
        m.AppendSeparator()
        #the columns
        self.columnSetNull = m.Append(-1, "Set to Null")
        
        self.Bind(wx.EVT_MENU, self.OnSort, self.sorter)
        self.Bind(wx.EVT_MENU, self.OnDelRow, self.rowDelete)
        self.Bind(wx.EVT_MENU, self.OnDelColumn, self.columnDelete)
        self.Bind(wx.EVT_MENU, self.OnDelRange, self.rangeDelete)
        self.Bind(wx.EVT_MENU, self.OnSetFieldNull, self.columnSetNull)
        
        ID_CLOSE = wx.NewId()
        wx.EVT_MENU(self, ID_CLOSE, self.OnClose)
        
        
        #set the movement of the cursor
        self.c_move = False
        ID_CMOVE = wx.NewId()
        wx.EVT_MENU(self, ID_CMOVE, self.setCMove)
        
        #accelerator table for shortcut keys
        self.acceltbl = wx.AcceleratorTable( [(wx.ACCEL_CTRL, ord('F'),
                                        b.GetId()),
                                        (wx.ACCEL_CTRL, ord('C'),
                                        c.GetId()),
                                        (wx.ACCEL_CTRL, ord('W'),
                                        ID_CLOSE),
                                        (wx.ACCEL_NORMAL, wx.WXK_F12, ID_CMOVE)] ) #wx.ACCEL_NORMAL, wx.WXK_F3, findnextID
        self.SetAcceleratorTable(self.acceltbl)
        #if updating this must be TRUE
        self.UPDATE_ALLOWED = False
        
        #variables for events ini the grid
        self.grd_range_left_top = ''
        self.grd_range_bottom_right = ''
        self.grd_col_num = ''
        self.grd_row_num = ''

        # Enable Column moving
        gridmovers.GridColMover(self)
        self.Bind(gridmovers.EVT_GRID_COL_MOVE, self.OnColMove, self)
        
        self.Bind(wx.EVT_SET_FOCUS, self.onFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.onLostFocus)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.OnSelectCell)
        
        
    def onFocus(self, event):
        #print "onFocus"
        self.hasFocus = True
        event.Skip()
        
    def onLostFocus(self, event):
        #print "onLostFocus"
        self.hasFocus = False
        event.Skip()
        
    def debugTest(self, event):
        print "Event debug fired %s" % event
    
    def OnSelectCell(self, evt):
       # print "OnSelectCell"
        evt.Skip()
        
    def OnColMove(self,evt):
        frm = evt.GetMoveColumn() # Column being moved
        to = evt.GetBeforeColumn() # Before which column to insert
        self.GetTable().MoveColumn(frm,to)
        evt.Skip()
            
    def OnRangeSelect(self, event):
        if event.Selecting():

            self.grd_range_left_top = event.GetTopLeftCoords()
            self.grd_range_bottom_right = event.GetBottomRightCoords()

            a,b = self.grd_range_left_top

            c,d = self.grd_range_bottom_right
            self.rangeDelete.SetText("Remove range %d to %d" % (a+1, c+1))

        
        event.Skip()
        
    
    def OnRightClick(self, event):
        "The Mini Frame"
        try:
            self.PopupMenu(self.menuPop)
        except: pass
        event.Skip()

    def OnRightClickCol(self, event):
        self.PopupMenu(self.menuColPop)
        
    def OnClickCol(self, event):
        self.grd_col_num = int(event.GetCol())
        self.grd_row_num = int(event.GetRow())

        #we are clicking the label on the sides

        if self.grd_row_num==-1:
            self.sorter.SetText('Sort column %d' % (int(self.grd_col_num)+1))
            self.rowDelete.SetText(' ') #Remove Row %d' % (int(self.grd_row_num)+1))
            
        if self.grd_col_num==-1:
            self.rowDelete.SetText('Remove Row %d' % (int(self.grd_row_num)+1))
        event.Skip()
        
    def OnLblLeftDbClick(self, event):
        print "OnLblLeftDbClick"
        self.showSingleForm( event.GetRow() )
        
    def OnSort(self, event):
        if self.grd_row_num==-1 and self.grd_col_num>=0:
            self.lst.sort(int(self.grd_col_num))
            self.ForceRefresh()
        event.Skip()


    def OnClickCellLeft(self, event):
        #GRIDMACRO
        row_num = event.GetRow()
        col_num = event.GetCol()
        #print "OnClickCellLeft", row_num, col_num #, event.GetPosition()
        event.Skip()
        
    def OnDoubleClickCellLeft(self, event):
        print "OnDoubleClickCellLeft"
       # print self.parent.__class__.__name__
       # print self.parent.pivot_lst.__class__.__name__
        
        row_num = event.GetRow()
        col_num = event.GetCol()
        wx.BeginBusyCursor()
        lst = False
        
        print "self.lst.view_id", self.lst.view_id
        app = wx.GetApp()
        #print app.mdi_parent_frame.MenuSetting.dic_view_ids
        
        try:
            #if pvt_getNode does not throw error
#             print "00 calling pvt_getNode"
            lst = self.parent.pivot_lst.pvt_getNode(row_num, col_num)
#             print "01 lst was collected in first try"
#             #lst.appMenu = self.parent.pivot_lst.appMenu
#             
#             print "02 appMenu", lst.appMenu
#             print "02 view_id", lst.view_id
            
        except:
            
            obj = self.lst[row_num]
            
            try:
                field_name = self.lst.fieldnames[col_num]
                obj.OnRecordDblClick(field_name, obj)
                #print "There has been defined an own method for the double click."
 
                wx.EndBusyCursor()
                return True
            except GUICodeNotExisting:
                pass
            
#             print "Open single form instead"
#             print self.parent.parent
            

           # print unicode ( obj )
            #print self.lst.view_id
#             print "Fieldnames: ", self.lst.fieldnames
#             print '-----'
            
            #frame = FrmSingle(self.parent.parent, obj, self.lst)
            frame = False
            
            if self.parent.__class__.__name__=='Frm2':
                frame = FrmSingle2(self.parent.parent, obj, self.lst.view_id, self.lst.fieldnames) #, self.lst)
            else:
                #frame = FrmSingle(self.parent.parent, obj, self.lst.view_id,  self.lst.fieldnames) #, self.lst)
                
                
                if self.parent.parent.MenuSetting.getAppMenu(self.lst.view_id):
                    if self.parent.parent.MenuSetting.getAppMenu(self.lst.view_id).incl_dblclick:
                        
                        appM = self.parent.parent.MenuSetting.getAppMenu(self.lst.view_id)
                        #print appM.dicExecCode
    
                        #self.OnEvalCodeNoEvent(appM.dicExecCode['Alchemy Form'], obj)
                        self.OnEvalCodeNoEvent(appM.dblClickCode, obj)
                else:
                    frame = FrmSingle(self.parent.parent, obj, self.lst.view_id,  self.lst.fieldnames)
                    
                
            wx.EndBusyCursor()
            if frame: 
                frame.Show(True)
            
            return False
        
        try:

            #lst = self.parent.pivot_lst.pvt_getNode(row_num, col_num)
            #was moved upwards in the code
            print "03 in next try loop"
            
            #these hacks are done because lst is now NOT
            #ListRecord class but only a list
            #self.pvt_data
            lst.view_id = self.parent.pivot_lst.view_id
            lst.dicExecCode = self.parent.pivot_lst.dicExecCode
            lst.appMenu = self.parent.pivot_lst.appMenu
            
            #lst.loadExecCode()
            
            print "03 view_id is: %s" % lst.view_id
            
#             print "after lst.loadExecCode() line 365"
#             print lst.view_id
            
            #helper hack so that we can double click
            #when using a form without being a child of app
            if self.parent.__class__.__name__=='Frm2':
                t = lambda: lst.base_table or 'Grid'
                #print lst.base_table, "lst.base_table"
                frame = Frm2(self.parent, lst, aTitle=t())
                frame.Raise()
            else:
                frame = Frm(self.parent.parent, lst)
                
            frame.Show(True)


        except:
            if self.CanEnableCellControl():
                self.EnableCellEditControl()

        finally:
            wx.EndBusyCursor()
            #event.Skip()
            return lst
    #def OnHideColumn
    def OnDelRange(self, event):
        #deletes rows
        self.BeginBatch()
        #self.GetTable().RemoveRange(self.grd_range_left_top[0][0], self.grd_range_bottom_right[0][0]+1)
        self.GetTable().RemoveRange(self.grd_range_left_top[0],
                                    self.grd_range_bottom_right[0]+1)
        self.EndBatch()
    
    def OnDelColumn(self, event):
        if self.grd_row_num==-1:
            self.GetTable().RemoveColumn(int(self.grd_col_num))
        
    def OnDelRow(self, event):
        #self.BeginBatch()
        if self.grd_col_num==-1:
            self.GetTable().RemoveData(self.grd_row_num)
        #self.EndBatch()
        
    def OnSetFieldNull(self, event):
        "update field (all records) to Null in DB"
        
        dlg = wx.MessageDialog(self, """You are about to set to Null (empty) the attribute %s
for all records in this set. The changes are in reversable. Would you like to proceed?""" % self.lst.fieldnames[int(self.grd_col_num)],
                           'Database message.',
                           wx.YES_NO | wx.YES_DEFAULT |
                    wx.ICON_QUESTION)
        val = dlg.ShowModal()
        
        if val==wx.ID_YES:
            try:
                wx.BeginBusyCursor()
                
                for r in self.lst:
                    print r.setNull( self.lst.fieldnames[int(self.grd_col_num)] )
            finally:
                wx.EndBusyCursor()
        
       # event.Skip()
        
   
    ##@anythread
    def OnSQLQuery(self, event):
# if const.RESTRICTED_USER:
        row_num = self.GetGridCursorRow()
        col_num = self.GetGridCursorCol()
        obj = self.lst[row_num]
        value = self.GetCellValue(row_num, col_num)
        sql = "select * from %s where %s='%s'" % (obj.base_table, self.lst.fieldnames[col_num], value)
        print sql
        query = loadFromDb(sql, obj.base_table)
        query.view_id = self.parent.pivot_lst.view_id
        query.value_field = self.parent.pivot_lst.value_field
        query.loadExecCode()
        try:
            frm = Frm(self.parent.parent, query)
        except TypeError:
            frm = Frm2(self.parent, query)
        frm.Show()
# else: pass
# event.Skip()
                
    def OnUpdate_v02(self, event):
        print "OnUpdate_v02"
        row_num = self.GetGridCursorRow()
        col_num = self.GetGridCursorCol()
        label = self.GetColLabelValue(col_num)
        obj = self.lst[row_num]
        app = wx.GetApp()
        
        if not self.UPDATE_ALLOWED:
            print "if not self.UPDATE_ALLOWED: %s" % self.UPDATE_ALLOWED
            
            dlg = wx.MessageDialog(self, """You are about to make an update.
Would you like to set the table in update mode?""",
                               'Database message.',
                               wx.YES_NO | wx.YES_DEFAULT |
                        wx.ICON_QUESTION)
            
            val = dlg.ShowModal()
            
            dlg.Destroy()
            
            #self.parent.Raise() #the bug that Alex had I also received with upgrade to version 3.0 ... this should solve it.
            
            wx.BeginBusyCursor()
            if val==wx.ID_YES:
                print "if val==wx.ID_YES:"
                busy = wx.BusyInfo("Inserting data ...")
                
                self.UPDATE_ALLOWED = True

                upd = obj.update(str(label))
                
                print "upd = obj.update(str(label)): %s" % upd
                
                if upd:
                    #helper hack so that we can double click
                    #when using a form without being a child of app
                    try:
                        app.mdi_parent_frame.statusbar.SetStatusText('Record id: %d was successfully updated.' % obj.id)
                    except: pass
                else:
                    #helper hack so that we can double click
                    #when using a form without being a child of app
                    try:
                        app.mdi_parent_frame.statusbar.SetStatusText('NO UPDATE MADE!!!')
                    except: pass
                
                #event.Skip()
            else:
                print "self.UPDATE_ALLOWED = False"
                self.UPDATE_ALLOWED = False
        else:
            print "ELSE self.UPDATE_ALLOWED: %s" % self.UPDATE_ALLOWED
            busy = wx.BusyInfo("Inserting data ...")
            wx.BeginBusyCursor()
            upd = obj.update(label)
            if upd:
                print "if upd"
                try:
                    app.mdi_parent_frame.statusbar.SetStatusText('Record id: %d was successfully updated.' % obj.id)
                except: pass
            else:
                try:
                    app.mdi_parent_frame.statusbar.SetStatusText('NO UPDATE MADE!!!')
                except: pass
                
        wx.EndBusyCursor()
        #event.Skip()

    def setUpdateStatus(self):   
        dlg = wx.MessageDialog(self, """You are about to make an update.
Would you like to set the table in update mode?""",
                           'Database message.',
                           wx.YES_NO | wx.YES_DEFAULT |
                    wx.ICON_QUESTION)

        self.UPDATE_ALLOWED = dlg.ShowModal()

        dlg.Destroy()

    def setUpdateStatus_TEST(self):
        
        _msg = """You are about to make an update.
Would you like to set the table in update mode?"""
        
        dlg = GMD.GenericMessageDialog(self, _msg,
                                       "Database message.",
                                       wx.YES_NO | wx.ICON_QUESTION)
        
        dlg.ShowModal()
        dlg.Destroy()
        if dlg==wx.ID_YES:
            self.UPDATE_ALLOWED = True
            return True
                
    def OnUpdate_v03(self, event):
        print "OnUpdate_v03"
        
#         from wx_frm_confirm import MsgConfirmFrame
#          
#         if not self.UPDATE_ALLOWED:
#             msg = MsgConfirmFrame()
#             msg.Show()
            
            
        self.UPDATE_ALLOWED = True # msg.decisssion
#             
#             while msg.close_me:
#                 self.UPDATE_ALLOWED = msg.decisssion
#                 msg.close_me = False
#                 break
            #self.setUpdateStatus()
        #self.UPDATE_ALLOWED = True

        if self.UPDATE_ALLOWED:
            wx.BeginBusyCursor()
            
            row_num = self.GetGridCursorRow()
            col_num = self.GetGridCursorCol()
            label = self.GetColLabelValue(col_num)
            obj = self.lst[row_num]
            app = wx.GetApp()

            busy = wx.BusyInfo("Inserting data ...")

            upd = obj.update(label)
            
            if upd:
                print upd
                try:
                    app.mdi_parent_frame.statusbar.SetStatusText('Record id: %d was successfully updated.' % obj.id)
                except: pass
            else:
                try:
                    app.mdi_parent_frame.statusbar.SetStatusText('NO UPDATE MADE!!!')
                except: pass
                
            wx.EndBusyCursor()
            
        event.Skip()

                
    def OnSearch(self, event):
        
       # wx.SetDefaultPyEncoding('utf-8') #trying to fix the decode problem when searching
         
        dlg = wx.TextEntryDialog(None, "Enter a search string:", "Search box")
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetValue()
               
            new_lst = self.lst.search(response)
            new_lst.loadExecCode()
            #frm = Frm(self.parent.parent, new_lst)
            app = wx.GetApp()

            if self.parent.__class__.__name__=='Frm2':
                frm = Frm2(self.parent.parent, new_lst, self.parent.title)
            else:
                frm = Frm(self.parent.parent, new_lst, self.parent.title)
        
            frm.Show()
            #return True
        dlg.Destroy()
        
        event.Skip()
        
  

    def OnClose(self, event):
        print "OnClose MyGrid"

        self.parent.OnClose(event)
        


    def OnAppendCopy(self, event):
        
        row_num = self.GetGridCursorRow()
        obj = self.lst[row_num]
        
        dlg = wx.TextEntryDialog(self, 'Enter number of copies.')
        
        dlg.ShowModal()
        
        _tmp_lst=[]
        
        
        for x in range(int(dlg.GetValue())):
            copy = obj.copy()

            if obj.id:
                copy.id_parent = obj.id
                _tmp_lst.append(copy)

            print copy.insert()
      
            #print len(self.lst)
            self.lst.append(copy)
            #print len(self.lst)
            self.AppendRows(1)
#
        self.parent.Refresh()

        dlg.Destroy()
        
        try:
            #in my old orm I do this
            sql = "select * from %s where id_parent=%d" % (obj.base_table, obj.id)
            n_lst = loadFromDb(sql, '%s' % obj.base_table)
        except:
            #when using alchemy I have to do this different
            
            n_lst = self.lst.createNewList()
            
            n_lst.data = _tmp_lst
            
        if self.parent.__class__.__name__=='Frm2':
            frm = Frm2(self.parent.parent, n_lst)
        else:
            frm = Frm(self.parent.parent, n_lst)
        frm.Show()
        
        #event.Skip()
               
    def OnSetFilterTo(self, event):
        "set filter"
        col_num = self.GetGridCursorCol()
        row_num = self.GetGridCursorRow()

        new_table = self.lst.filterGrid(row_num, col_num)
        
        new_table.loadExecCode()
        app = wx.GetApp()
        if self.parent.__class__.__name__=='Frm2':
            app = wx.GetApp()
            #frm = Frm2(app.mdi_parent_frame, new_table, 'Grid 2')
            frm = Frm2(self.parent.parent, new_table, self.parent.title)
        else:
            frm = Frm(self.parent.parent, new_table, self.parent.title)
            
        frm.Show()
        #event.Skip()


    def showSingleForm(self, row_num):

        print "showSingleForm"
        obj = self.lst[row_num]
        #frame = FrmSingle(self.parent.parent, obj, self.lst)
        frame = FrmSingle(self.parent.parent, obj, self.lst.view_id) #, self.lst)
        frame.Show(True)


        

    def OnEvalCode(self, event):
        print "wx_forms MyGrid() OnEvalCode"
        col_num = self.GetGridCursorCol()
        row_num = self.GetGridCursorRow()
        e_id = event.GetId()
        
        here_recordval = self.lst.get(row_num, col_num)
        here_field = self.lst.fieldnames[col_num]
        here_obj = self.lst[row_num]
        here_lst = self.lst
        
        try:
            exec( self.lst.dicExecCode [ self.dicCodeExecIds[e_id] ] )
        except TypeError:
            apply( self.lst.dicExecCode [ self.dicCodeExecIds[e_id] ] )
            
    def OnEvalCodeNoEvent(self, codeStr, here_obj):
        print "wx_forms MyGrid() OnEvalCodeNoEvent"

        try:
            exec( codeStr )
        except TypeError:
            apply( codeStr )
            
    def doingSomeMath(self, event, operate):
        "Helper method for OnAddNumber and others"
        col_num = self.GetGridCursorCol()

        here_field = self.lst.fieldnames[col_num]

        dlg = wx.TextEntryDialog(self, 'Enter number to operate on:')
        
        dlg.ShowModal()
        
        A = float(dlg.GetValue())
        
        dlg.Destroy()
        
        for r in self.lst:
            try:
                B = float(getattr(r, here_field))
                setattr(r, here_field, operate(B, A) )
               # update changes in DB with other
               #method see OnCommitToDb r.update( here_field )
            except:
                raise('not possible to change value')
        #event.Skip()

    def OnAddNumber(self, event):
        return self.doingSomeMath(event, operator.add)
    
    def OnSubtractNumber(self, event):
        return self.doingSomeMath(event, operator.sub)
    
    def OnCommitToDb(self, event):
        "Do not commit to db math calculations straight away, do it by this method afterwards."
        
        col_num = self.GetGridCursorCol()
        here_field = self.lst.fieldnames[col_num]
        
        for r in self.lst:
            print r.update( here_field )
        #event.Skip()
        
    def OnIncByOne(self, event):
        col_num = self.GetGridCursorCol()
        here_field = self.lst.fieldnames[col_num]

        row_num = self.GetGridCursorRow()
        
        here_recordval = self.lst.get(row_num, col_num)

        here_obj = self.lst[row_num]
        
        per_start = float(getattr(here_obj, here_field))
        
        i=0
        for r in self.lst:
            setattr(r, here_field, per_start + i )
            i+=1
            
# print "test is working"
# print here_recordval
# i=0
# start=float(here_recordval)
# for x in here_lst:
#     x.period=start+i
#     i+=1
#     x.update('period')

            #         frm = FrmMathCalcHlp(self.parent.parent, self.lst, here_field)
            #         frm.Show()
            #         frm.Raise()
                 

    
        
    def OnSingleForm(self, event):
        self.showSingleForm( self.GetGridCursorRow() )


###Startin to refactor the class Frm below.
###This form should have as its base class a panel
###the current structure only alows for the use of this as a MDIChild

    def OnUpdateColForm(self, event):
        "Updates the entire column"
        col_num = self.GetGridCursorCol()
        here_field = self.lst.fieldnames[col_num]
        
        dlg = wx.TextEntryDialog(None, "Enter new string and update %s:" % here_field, "Update column %s" % here_field)
        
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetValue()

            for r in self.lst:

                setattr(r, here_field, response)
                print r.update(here_field)
                
        self.ForceRefresh()
        dlg.Destroy()
        
        #event.Skip()
        
    def OnUpdateColFormGroup(self, event):
        "Updates the entire columnb, but using a different sql statement"
        col_num = self.GetGridCursorCol()
        here_field = self.lst.fieldnames[col_num]
        
        dlg = wx.TextEntryDialog(None, "Enter new string:", "Update column %s" % here_field)
        
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetValue()
            lst_ids = []
            
            table = self.lst[0].base_table
            for r in self.lst:
                
                lst_ids.append(r.id)
                setattr(r, here_field, response)
                #print r.update(here_field)
                assert table == r.base_table #can be dangerous in a union select
                        
        print self.lst.sqlUpdateGrup(table, here_field, response, lst_ids)
        
        self.ForceRefresh()
        dlg.Destroy()
        
        #event.Skip()
    
    def setCMove(self, evt):
        "Change the modus of how the cursor moves"
        if self.c_move:
            self.c_move = False
        else:
            self.c_move = True
        evt.Skip()

    def OnKeyDown(self, evt):
        #print evt.GetKeyCode()
        #print wx.WXK_RETURN
        #both enter and return or no? and evt.GetKeyCode() != 370
        
        if self.c_move:
            if evt.GetKeyCode() != wx.WXK_RETURN and evt.GetKeyCode() != 370:
                evt.Skip()
                return
    
            if evt.ControlDown(): # the edit control needs this key
                evt.Skip()
                return
    
            self.DisableCellEditControl()
            success = self.MoveCursorRight(evt.ShiftDown())
    
            if not success:
                newRow = self.GetGridCursorRow() + 1
    
                if newRow < self.GetTable().GetNumberRows():
                    self.SetGridCursor(newRow, 0)
                    self.MakeCellVisible(newRow, 0)
                else:
                    # this would be a good place to add a new row if your app
                    # needs to do that
                    pass
        else:
            evt.Skip()
            return

    def addFuncToMenu(self, txtDescripton, func):
        custom = self.menuPop.Append(-1, txtDescripton)
        self.Bind(wx.EVT_MENU, func, custom)

class FrmMixInn(object):
    def __init__(self, parent, lst, aTitle='Grid Frame'):
        self.title = aTitle
        self.parent = parent
        self.pivot_lst = lst

    #------------------------------------------------------------------------------
    def createTheToolBar(self):
        #print self.CreateToolBar.__doc__

        tb = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT )
       # tb = wx.ToolBar(self, -1, style= wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        
        bmp_size = (25,25)
        
        id_xls = wx.NewId()
        #print "CreateToolBar", tb
        
        tb.AddSimpleTool(id_xls, getXlsImage(), "Export to xls", "Export to xls")
        self.Bind(wx.EVT_TOOL, self.OnXlsExport, id=id_xls)

        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_TOOLBAR, bmp_size)
        id_newpvt = wx.NewId()
        tb.AddSimpleTool(id_newpvt, copy_bmp, "Show View", "Show view definitions")
        self.Bind(wx.EVT_TOOL, self.OnShowViewDef, id=id_newpvt)

        copy_exe = wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR, bmp_size)
        id_shell = wx.NewId()
        tb.AddSimpleTool(id_shell, copy_exe, "wxPython shell", "wxPython shell")
        self.Bind(wx.EVT_TOOL, self.OnShell_v02, id=id_shell)

        hist_img = wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_TOOLBAR, bmp_size)
        id_hist_img = wx.NewId()
        tb.AddSimpleTool(id_hist_img, hist_img, "Show histogram", "Show histogram")
        self.Bind(wx.EVT_TOOL, self.OnShowStatHistogram, id=id_hist_img)
        
        refresh_bmp = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, bmp_size)
        id_refresh = wx.NewId()
        tb.AddSimpleTool(id_refresh, refresh_bmp, "Refresh pivot", "Refresh pivot")
        self.Bind(wx.EVT_TOOL, self.OnViewPivot_2, id=id_refresh)        
        
        tb.AddSeparator()
        #ID_TEST_BUTTON = wx.NewId()
        #tb.AddControl( wx.Button( tb, ID_TEST_BUTTON, "Button", wx.DefaultPosition, wx.DefaultSize ) )
        tb.AddControl( wx.StaticText( tb, -1, self.title))
                       
        tb.SetToolBitmapSize(bmp_size)
        
        tb.Realize()
        
    def addToolBar(self, method):
        """Add elements onto the tool bar, this method is not in use ....
"""
        #raise NotImplementedError
        id_shell = wx.NewId()
        copy_exe = wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR, (18,18))
        self.tb.AddSimpleTool(id_shell, copy_exe, "Custom method", "Custom method")
        self.Bind(wx.EVT_TOOL, method, id=id_shell)
        self.tb.Realize()
        
    def OnShowViewDef(self, event):
        frm = ViewDefFrm(self.parent, self.pivot_lst)
        frm.Show(True)
        
    def OnViewPivot_2(self, event):
        """Re-opens a pivoted view by getting the data from the database again."""
        
        print "OnViewPivot_2"
        
        test = self.pivot_lst.isPivoted
        
        if test:
            wx.BeginBusyCursor()
            
            newRecSet = self.pivot_lst.refreshPivot()
            newRecSet.view_id = self.pivot_lst.view_id
            
            frame = Frm(self.parent, newRecSet, self.title)
            frame.Show(True)
            self.Close()
            
            wx.EndBusyCursor()
        else:
            self.Close()

        
    def OnXlsExport(self, event):
        """Export the contents of the grid into an xls sheet."""
        print "OnXlsExport in wx_forms"
        
        rightCol = len(self.grid.lst.fieldnames)
# try:
        
        if self.grid.lst.isPivoted:
            #raise('the grid is in pivot')
            dlg = wx.MessageDialog(self, "The table is pivoted, drill down to export",
                               'Application message.',
                               wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return True
            #event.Skip()

        wx.BeginBusyCursor()
        
        row = len(self.grid.lst.table)
        
        from win32com.client import Dispatch
        try:
            xlApp = Dispatch('Excel.Application')
            xlBook = xlApp.Workbooks.Add()
            
            xlSheet = xlBook.Worksheets(SHEET_NAME)
            
            xlSheet.Range(xlSheet.Cells(1, 1),
                            xlSheet.Cells(row, rightCol)).Value = self.grid.lst.xlsTable
    
            xlApp.Visible = 1
            xlApp = None
            
            
        except Exception, e:
            dlg = wx.MessageDialog(self, "An exception with following message was generated:\n %s" % str(e),
                               'Application message.',
                               wx.OK | wx.ICON_INFORMATION)
            print """Hint! If the xls sheet name in config is wrong you could end up here in the code.
            For example if you have German settings and a new xls sheet is named Tabelle1 but Sheet1 is in the
            config definitions you will have this error."""
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            wx.EndBusyCursor()
            #event.Skip()

            
    def importFile(self, fullpathname='C:\\home\\workspace\\period.py'):
        "loads a module into the name space of crust"
        import imp
        path, filename = os.path.split(str(fullpathname))
        root, ext = os.path.splitext(filename)
        print root, path
        found = imp.find_module(root, [path])
        if found:
            (file, pathname, description) = found
            try:
                module = imp.load_module(root, file, pathname, description)
                #print module
                #I seem not to be able to find the scope of this
                #self.shell.interp.locals[root]= module
                #globals()[root] = module
                #locals()[root] = module
                #lst.locals[root]= module
                print 'module sucessfully loaded'
            finally:
                file.close()
                #so I just return it for now
                return module
        else: print 'file not found'
                

        
    def OnShowStatHistogram(self, event):
        self.grid.lst.stat_plotHist()
        #event.Skip()
        
        
    def OnShell_v02(self, event):
        from wx.py.editor import EditorNotebookFrame #EditorNotebookFrame
        from wx.py.shell import ShellFrame
        
        #frame = EditorFrame(self) #EditorNotebookFrame(filename=None)
        frame = EditorNotebookFrame(parent=self)
        
        frame.shell.interp.locals['lst']= self.pivot_lst
        frame.shell.interp.locals['r']= self.pivot_lst[0]
        
        frame.shell.interp.locals['importFile']= self.importFile
        frame.shell.interp.locals['FrmShow']= FrmShow
        frame.shell.interp.locals['parent']= self.parent
        frame.shell.interp.locals['App']= wx.GetApp()
            
        # frame.shell.interp.locals['lst']= self.pivot_lst
        # frame.shell.interp.locals['r']= self.pivot_lst[0]
        frame.Show()
        frame.shell.write('"In local scope: r - lst - importFile - FrmShow - parent"')
        
        
        #self.SetTopWindow(self.frame)
        

                       
class FrmMathCalcHlp(wx.MDIChildFrame, CtrWCloseUtil):
    """Form that collects information on what operations to do on a list of record objects."""
    def __init__(self, parent, lst, here_field):
        """Calculate on a list.
"""
        raise("lets not use this any more")
    
        self.lst = lst
        self.here_field = here_field
        
        wx.MDIChildFrame.__init__(self, parent, id=-1, title='List calculations',
                          size=(500,200))
        
        wx.MDIChildFrame.SetIcon(self, ssc_logo_2.getssc_logo_Icon())
        
        CtrWCloseUtil.__init__(self)
        
        panel = wx.Panel(self, id=-1)
        
        self.cmbForUpd = wx.ComboBox(panel, -1, self.here_field, pos=(10,10),
                            size=(80,20), choices=lst.fieldnames)
        
        self.Bind(wx.EVT_TEXT, self.OnTextUpdField, self.cmbForUpd)
        
        
        self.txt_ch = wx.TextCtrl(panel, -1, 'Changes will be made on %s' % here_field,
                                  size=(300, 20),pos=(90, 10), style=wx.TE_READONLY)
        
        self.cmbA = wx.ComboBox(panel, -1, pos=(10,35),
                            size=(80,20), choices=lst.fieldnames)

        self.cmbOperator = wx.ComboBox(panel, -1, pos=(100,35),
                            size=(50,20), choices=['+', '-', '*', '/'])
                
        self.numb = wx.TextCtrl(panel, -1, '0.0', size=(50, 20),pos=(150, 35))
        

        
        self.txt = wx.StaticText(panel, -1, 'Perform operation on the records of the list',
                                 size=(200, 25),pos=(10, 70))
        
        self.btn = wx.Button(panel, -1, "Calc.", pos=(350, 80))
        self.btn_commit = wx.Button(panel, -1, "Commit", pos=(350, 103))
        
        self.Bind(wx.EVT_BUTTON, self.OnClickBtn, self.btn)
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnCommit, self.btn_commit)
        
    def OnClickBtn(self, event):
        cmbA = self.cmbA.GetValue()
        cmbOperator = self.cmbOperator.GetValue()
        numb = float( self.numb.GetValue() )
        for r in self.lst:
            cmbA_flt = float( getattr(r, cmbA) )
            if cmbOperator=='+':
                new_nr = operator.add(cmbA_flt, numb)
            elif cmbOperator=='*':
                new_nr = operator.mul(cmbA_flt, numb)
            elif cmbOperator=='/':
                new_nr = operator.div(cmbA_flt, numb)
            elif cmbOperator=='-':
                new_nr = operator.sub(cmbA_flt, numb)
            else: raise('select an operator')
            setattr(r, self.here_field, new_nr)
                
        #event.Skip()
        
    def OnClickBtnCommit(self, event):
        for r in self.lst:
            print r.update( self.here_field )
            
        #event.Skip()
        
    def OnTextUpdField(self, event):
        self.here_field = self.cmbForUpd.GetValue()
        self.txt_ch.SetValue('Changes will be made on %s' % self.here_field)


class Frm(wx.MDIChildFrame, FrmMixInn):
    """The pivot form in the GUI App."""
    def __init__(self, parent, lst, aTitle='Grid Frame'):
        """The Grid
Example usage in Crust:
f = Frm(None, lst)
f.Show()
"""

        FrmMixInn.__init__(self, parent, lst, aTitle)
        
        wx.MDIChildFrame.__init__(self, parent, id=-1, title='%s' % aTitle, size=(950,600))
        
        wx.MDIChildFrame.SetIcon(self, ssc_logo_2.getssc_logo_Icon())
        
        self.createGrid(lst, dataCols=None)
        #self.grid = MyGrid(self, lst)
        
        self.createTheToolBar()
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.Bind(wx.EVT_MENU_CLOSE, self.OnMenuClose)


    def createGrid(self, lst, dataCols=None):
        self.grid = MyGrid(self, lst) #, dataCols)
        return self.grid
        
    def OnClose(self, event):
        print "closing Frm"
        # print "self.grid.Destroy() This causes imediate crash!"
        # self.grid.Destroy()
        self.grid.Close()

        self.Destroy()
        
        #event.Skip()
        
    def OnMenuClose(self, evt):
        print "OnMenuClose"
        evt.Skip()
        
    def OnSetFocus(self, evt):
        print "OnSetFocus"
        self.grid.SetFocus()
        evt.Skip()
        
    def OnTextCopy(self, evt):
        print "EVT_TEXT_COPY, OnTextCopy"
        #self.grid.SetFocusFromKbd()
        evt.Skip()
           
    def OnWindowDestry(self, evt):
        print "OnWindowDestry"
        self.Destroy()
        #evt.Skip()
                   

class Frm2(wx.Frame, FrmMixInn):
    def __init__(self, parent, lst, aTitle='Grid Frame', dataCols=None):
        """The Grid
Example usage in Crust:
f = Frm(None, lst)
f.Show()
"""
        
        FrmMixInn.__init__(self, parent, lst, aTitle)
        wx.Frame.__init__(self, parent, id=-1, title='%s' % aTitle,
                          size=(950,600))

        self.createGrid(lst, dataCols=None)
        #self.grid = MyGrid(self, lst)
        self.createTheToolBar()

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        wx.Frame.SetIcon(self, ssc_logo_2.getssc_logo_Icon())
        
    def OnClose(self, event):
        print "closing parent"
        self.Destroy()
        #event.Skip()
                
    def createGrid(self, lst, dataCols=None):
        self.grid = MyGrid(self, lst, dataCols)
        return self.grid
    
    def addToolBar(self, method, title=''):
        
        x_bmp = wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_TOOLBAR, (18,18))
        id_x = wx.NewId()
        self.tb.AddSimpleTool(id_x, x_bmp, "%s" % title, "%s" % title)
        self.Bind(wx.EVT_TOOL, method, id=id_x)
        
### -Sigle Object Form- ###

from ahutils.record import MetaRecord

class ScrolledWindowSingle(wx.ScrolledWindow):
    
    def __init__(self, parent, obj, view_id=None, fieldnames=None):
        self.parent = parent
        self.obj = obj
        self.view_id = view_id
        self.obj = obj
        self.fieldnames = fieldnames
        self.meta = MetaRecord(self.obj)

        self.dicTxtID_Label = {} #the keys and values of the objects.__dict__
                                      #with dicTxtID_Label = {wxID = {key:val}, ...}
                                              
        self.dicTxtID_NewText = {}
        self.dicTxtID_Label = {}
        self.dicLabel_Txt2 = {}
        
        wx.ScrolledWindow.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

        self.SetScrollbars(1,1,950,1600)
        self.SetScrollRate(20,20)
        
        btnUpdate = wx.Button(self, -1, "Update", pos=(600, 30))
        
        btnShell = wx.Button(self, -1, "Shell", pos=(800, 30))
        
        btnUpload = wx.Button(self, -1, "Upload", pos=(700, 60))
        
        btnDelete = wx.Button(self, -1, "Delete")
        
        self.vbox = wx.BoxSizer(wx.HORIZONTAL)
        self.box_btn = wx.BoxSizer(wx.VERTICAL)
        
        self.box_btn.Add(btnShell)
        self.box_btn.Add(btnUpload)
        self.box_btn.AddSpacer(10)
        
        
        self.CreateStaticText()
        self.vbox.AddSizer(self.hbox)
        
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnUpload, btnUpload)
        self.Bind(wx.EVT_BUTTON, self.OnClickSave, btnUpdate)
        self.Bind(wx.EVT_BUTTON, self.OnClickDelete, btnDelete)

        self.Bind(wx.EVT_BUTTON, self.OnShell, btnShell)

        
        if obj.__dict__.has_key('pivothead'):
            btnView = wx.Button(self, -1, "Pivot", pos=(800, 60))
            self.Bind(wx.EVT_BUTTON, self.OnViewPivot, btnView)
            self.box_btn.Add(btnView)
            self.box_btn.AddSpacer(10)
            
        self.box_btn.Add(btnUpdate)
        self.box_btn.AddSpacer(200)
        self.box_btn.Add(btnDelete)
        self.vbox.AddSizer(self.box_btn)
        self.SetSizer(self.vbox)

    def CreateStaticText(self):
        "The object is displayed"
        self.hbox = wx.BoxSizer(wx.VERTICAL)
        cnt = 30
        #for key in self.fieldnames:
        if self.fieldnames:
            l = self.fieldnames
        else:
            #this does probably not happen but sorting is also nice
            l = [key for key in self.obj.__dict__.keys()]
            l.sort()
            
        for key in l:
            vbox_inner = wx.BoxSizer(wx.HORIZONTAL)
            stat_txt = wx.StaticText(self, -1, key, (100, cnt), size=(100,22))
            
            strng = ("%s") % unicode(getattr(self.obj, key))


            ctr_id = wx.NewId()
            #associate the controls with the values
            _d = {}
            _d[key] = strng
            self.dicTxtID_Label[ctr_id] = _d

            #_txt = _getObjAttr(self.obj, key)
            ctr = wx.TextCtrl(self, ctr_id, strng, size=(300, 20),pos=(250, cnt))

            self.dicTxtID_Label[ctr_id] = key
            self.dicLabel_Txt2[key] = ctr

            ctr.Bind(wx.EVT_LEFT_DCLICK, self.OnDblClick)
            ctr.Bind(wx.EVT_TEXT, self.OnText)
            
            cnt+=30
            vbox_inner.AddSpacer(10)
            vbox_inner.Add(stat_txt, 0, wx.RIGHT, 8)
            vbox_inner.Add(ctr, 1, wx.EXPAND|wx.ALL)
            vbox_inner.AddSpacer(10)
            self.hbox.AddSizer(vbox_inner)
                 

    def OnViewPivot(self, event):
        print "OnViewPivot"
        wx.BeginBusyCursor()
        lst = loadFromDb( getattr(self.obj, 'sql'), getattr(self.obj, 'tablename'))
        #lst.view_id = self.lst.view_id
        lst.view_id = self.view_id
        _pivotrow = getattr(self.obj, 'pivotrow')
        _pivotrow = _pivotrow.split(',')
        #strip the field for space
        pivot_row = [r.strip() for r in _pivotrow]
                       
        _pivothead = getattr(self.obj, 'pivothead')
        _pivothead = _pivothead.split(',')
        pivot_head = [r.strip() for r in _pivothead]
        pivot_amount = getattr(self.obj, 'pivotvalue')
        menutitle = getattr(self.obj, 'menutitle')
        #print pivot_row, pivot_head, pivot_amount
        lst.pivot(pivot_row, pivot_head, pivot_amount)
        frame = Frm(self.parent.parent, lst, menutitle)
        frame.Show(True)
        wx.EndBusyCursor()
        #event.Skip()


    def OnClickSave(self, event):
        for key, val in self.dicTxtID_NewText.items():
            #self.obj.__dict__[key] = val
            setattr(self.obj, key, val.strip())
            if val=="":
                msg = self.obj.setNull(key)
                print msg
                if msg:
                    self.dicLabel_Txt2[key].SetBackgroundColour((159, 213, 197))
                else:
                    self.dicLabel_Txt2[key].SetBackgroundColour('Red')
                self.Refresh()
            else:
                msg = self.obj.update(key)
                print msg
                if msg:
                    self.dicLabel_Txt2[key].SetBackgroundColour((159, 213, 197))
                else:
                    self.dicLabel_Txt2[key].SetBackgroundColour('Red')
                self.Refresh()
        self.dicTxtID_NewText = {}
        #event.Skip()
                    

    def OnText(self, event):
        label = self.dicTxtID_Label[event.GetId()]
        self.dicTxtID_NewText[ label ] = event.GetString()
        event.Skip()
                   
    def OnDblClick(self, event):
        "Show a signle field form."
        d = self.dicTxtID_Label[event.GetId()]
        #print d, "d is here"
        frame = FrmSingleField(self, self.obj, d)
        event.Skip()
        frame.Show(True)
        
        
    def OnClickDelete(self, event):
        "Delete the database record"
        msg = GenericMsgDlg('Are you sure you want to permanently delete this record?',
                            'Deleting record', wx.YES_NO|wx.NO_DEFAULT)
        if msg==wx.ID_YES:
            self.obj.delete()
            
        #event.Skip()
        
    def OnClickBtnUpload(self, event):
        dlg = wx.FileDialog(self, wildcard="*")
        
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            didInsert = self.meta.insertBlob( dlg.GetFilename(), dlg.GetPath() )
            if not didInsert:
                dlg = wx.MessageDialog(self, '''Data to complex to insert!
The data was NOT inserted.''',
                                   'Application message.',
                                   wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
            wx.EndBusyCursor()
        dlg.Destroy()
        #event.Skip()
        
    def OnClickBtnDownload(self, event):
        
        dlg = wx.FileDialog(self, message="Save file as ...",
                            wildcard="*", style=wx.SAVE)
        dlg.SetFilename(self.lstFileNames[self.lstBox.GetSelection()][1])
        #import tempfile???
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            path = dlg.GetPath()
            fp = file(path, 'wb') # Create file anew
            db_id = int( self.lstFileNames[self.lstBox.GetSelection()][0] )
            stream = self.meta.getBlob(db_id)
            data = stream.read()
            fp.write(data)
            fp.close()
            
            os.startfile(path)
            
            wx.EndBusyCursor()
        dlg.Destroy()
        #event.Skip()
        
    def OnShell(self, event):
        from wx.py.shell import ShellFrame
        
        frame = ShellFrame(parent=self)
        frame.shell.interp.locals['r']= self.obj
        frame.shell.interp.locals['meta']= self.meta
        #frame.shell.interp.locals['lst']= self.lst
        frame.shell.write('"in local scope: r - meta"')
        frame.Show()
        event.Skip()
        


def showSingleFormObj(obj):
    print "showSingleFormObj"
    app = wx.GetApp()
    frame = FrmSingle2(None, obj, None) #, self.lst)
    frame.Show(True)
                          
class FrmSingle(wx.MDIChildFrame):
    """Displays a record object."""
    #def __init__(self, parent, obj, lst):
    def __init__(self, parent, obj, view_id=None, fieldnames=None):
        
        self.parent = parent

        wx.MDIChildFrame.__init__(self, parent, id=-1, title='Single Object Frame',
                          size=(950,600))
        
        self.panel = ScrolledWindowSingle(self, obj, view_id, fieldnames) #wx.ScrolledWindow(self, -1)

        self.panel.Fit()  
        
        wx.MDIChildFrame.SetIcon(self, ssc_logo_2.getssc_logo_Icon())


        ID_CLOSE = wx.NewId()
        wx.EVT_MENU(self, ID_CLOSE, self.OnClose)    

        #accelerator table for shortcut keys
        acceltbl = wx.AcceleratorTable( [(wx.ACCEL_CTRL, ord('W'),
                                        ID_CLOSE)] )
        self.SetAcceleratorTable(acceltbl)
        
    def OnClose(self, event):
        self.Close()
        #event.Skip()

class FrmSingle2(wx.Frame):
    """Displays a record object."""
    #def __init__(self, parent, obj, lst):
    def __init__(self, parent, obj, view_id=None, fieldnames=None):
        
        self.parent = parent

        wx.Frame.__init__(self, parent, id=-1, title='Single Object Frame',
                          size=(950,600))
        
        self.panel = ScrolledWindowSingle(self, obj, view_id, fieldnames) #wx.ScrolledWindow(self, -1)

        self.panel.Fit()  
        
        wx.Frame.SetIcon(self, ssc_logo_2.getssc_logo_Icon())


        ID_CLOSE = wx.NewId()
        wx.EVT_MENU(self, ID_CLOSE, self.OnClose)    

        #accelerator table for shortcut keys
        acceltbl = wx.AcceleratorTable( [(wx.ACCEL_CTRL, ord('W'),
                                        ID_CLOSE)] )
        self.SetAcceleratorTable(acceltbl)
        
    def OnClose(self, event):
        self.Close()
        #event.Skip()
            
### -Single Filed- ###

class FrmSingleField(wx.Frame):
    def __init__(self, parent, obj, field):
        self.obj = obj
        self.field = field
        wx.Frame.__init__(self, parent, id=-1, title='%s' % self.field, size=(400,400), pos=wx.DefaultPosition, style=wx.DEFAULT_FRAME_STYLE)
        wx.Frame.SetIcon(self, ssc_logo_2.getssc_logo_Icon())
        
        self.panel = wx.Panel(self, id=-1)
        ##-----##
        ID_CLOSE = wx.NewId()
        wx.EVT_MENU(self, ID_CLOSE, self.OnClose)
        #accelerator table for shortcut keys
        acceltbl = wx.AcceleratorTable( [(wx.ACCEL_CTRL, ord('W'),
                                        ID_CLOSE)] )
        self.SetAcceleratorTable(acceltbl)
        ##-----##
        
        
        self.txt = wx.TextCtrl(self.panel, -1, str( getattr(self.obj, field) ), size=(390,390),
                          style=wx.TE_MULTILINE)
        
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.txt.SetFont(font)


        self.btn_update = wx.Button(self.panel, -1, "Update")
        self.Bind(wx.EVT_BUTTON, self.OnBtnUpdate, self.btn_update)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.txt, 3, wx.EXPAND|wx.ALL)
        vbox.Add(self.btn_update, 0, wx.RIGHT)
        self.panel.SetSizer(vbox)
        #self.panel.Fit()
        
    def OnBtnUpdate(self, event):
        setattr(self.obj, self.field, self.txt.GetValue().strip())
        msg = self.obj.update(self.field)
        if msg:
            self.txt.SetBackgroundColour((159, 213, 197))
        else:
            self.txt.SetBackgroundColour('Red')
        self.Refresh()
        #event.Skip()
        
    def OnClose(self, event):
        print "OnClose 3"
        self.Close()
        #event.Skip()
        
### -The Information Form- ###

class ViewDefFrm(wx.MDIChildFrame, CtrWCloseUtil):
    """Information Form. Display the view definitions"""
    def __init__(
            self, parent, lst, ID=-1, title='View definitions', pos=wx.DefaultPosition,
            size=(600,600), style=wx.DEFAULT_FRAME_STYLE
            ):

        
        wx.MDIChildFrame.__init__(self, parent, ID, title,
                                  pos, size, style)
        wx.MDIChildFrame.SetIcon(self, ssc_logo_2.getssc_logo_Icon())

        CtrWCloseUtil.__init__(self)

        
        self.parent = parent
        self.lst = lst
                   
        if self.lst.view_id:
            lst_view_sql = "select * from tbl_views where id=%d" % self.lst.view_id
            view_lst = loadFromDb(lst_view_sql, 'tbl_views')
            view_lst.view_id = self.lst.view_id
            grd = MyGrid(self, view_lst)
            grd.parent = self 
        
       
### -Paged Form- ###

class PagePannelBase(wx.Panel):
    def __init__(self, parent, obj):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        self.obj = obj
        
        self.dicTxtID_Label = {}
        self.dicLabel_Txt2 = {}
        self.dicTxtID_NewText = {}
        self.nb_panel = wx.Panel(self, -1)
        self.nb = wx.aui.AuiNotebook(self.nb_panel)

        self.head_panel = wx.Panel(self, -1)
        
        self.sizer_main = wx.BoxSizer(wx.VERTICAL)
        
        
        headers = self.initHeader()
        #self.sizer_main.Add(headers, 1)
        
        self.sizer_main.Add(self.head_panel, 1)
        
        self.initButtons()
        
        self.sizer_main.Add(self.nb_panel, 3, wx.EXPAND)
        
        
        self.initPages()
        
        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer_main)
        self.sizer.Add(self.nb, 1, wx.EXPAND)
        
        self.nb_panel.SetSizer(self.sizer)
        
        #To close
        ID_CLOSE = wx.NewId()
        wx.EVT_MENU(self, ID_CLOSE, self.OnClose)

        #accelerator table for shortcut keys
        acceltbl = wx.AcceleratorTable( [(wx.ACCEL_CTRL, ord('W'),
                                        ID_CLOSE)] )
        self.SetAcceleratorTable(acceltbl)
        
    def initHeader(self):
        raise("This is overridden in the form itself.")
    
    def initPages(self):
        raise("This is overridden in the form itself.")
    
    def initButtons(self):
        if self.insertForm:
            self.btn_insert = wx.Button(self.head_panel, -1, "Insert", pos=(10, 64))
            #vbox.Add(self.btn_insert, 0, wx.RIGHT, 8)
            self.Bind(wx.EVT_BUTTON, self.OnClickInsert, self.btn_insert)
        else:
            self.btn_update = wx.Button(self.head_panel, -1, "Update", pos=(10, 64))
            #vbox.Add(self.btn_update, 0, wx.RIGHT, 8)
            self.Bind(wx.EVT_BUTTON, self.OnClickSave, self.btn_update)

    def createPage(self, lst, pageName):

        vbox = wx.BoxSizer(wx.VERTICAL)

        thePanel = wx.Panel(self.nb, -1)

        for row in lst:
            hbox1 = wx.BoxSizer(wx.HORIZONTAL)
            
            static_txt = wx.StaticText(thePanel, -1, row, size=(100, 22))
           
            txt2 = self.createControl(row, thePanel)
            
            hbox1.Add(static_txt, 0, wx.RIGHT, 8)
            hbox1.Add(txt2, 0, wx.EXPAND|wx.ALL)
            
            vbox.Add(hbox1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 2)
        
        self.nb.AddPage(thePanel, pageName)
        thePanel.SetSizer(vbox)
        thePanel.Fit()
        
    def createListPage(self, lst, pageName):
        "Creates a page for a RecordList"
        vbox = wx.BoxSizer(wx.VERTICAL)

        #thePanel = wx.Panel(self.nb, -1)
        thePanel = MyGrid(self.nb, lst)

        
        self.nb.AddPage(thePanel, pageName)
        thePanel.SetSizer(vbox)
        thePanel.Fit()
        
    def createControl(self, row, thePanel, size=(205,22)):
        app = wx.GetApp()
        if app.dic_Usefull.has_key(row):
            ID_txt2 = wx.NewId()
            txt = _getObjAttr(self.obj, row)

            txt2 = wx.ComboBox(thePanel, ID_txt2, str( txt ), wx.DefaultPosition,
                               size, app.dic_Usefull[row])
            
            self.Bind(wx.EVT_TEXT, self.OnText, txt2)
            txt2.Bind(wx.EVT_LEFT_DCLICK, self.OnDblClick)
            
            self.dicTxtID_Label[ID_txt2] = row
            self.dicLabel_Txt2[row] = txt2
            return txt2

        else:
            ID_txt2 = wx.NewId()
            txt = _getObjAttr(self.obj, row)

            txt2 = wx.TextCtrl(thePanel, ID_txt2, str( txt ),
                               size ,style=wx.EXPAND)
            
            self.Bind(wx.EVT_TEXT, self.OnText, txt2)
            txt2.Bind(wx.EVT_LEFT_DCLICK, self.OnDblClick)
            
            self.dicTxtID_Label[ID_txt2] = row
            self.dicLabel_Txt2[row] = txt2
            return txt2

    
    def OnText(self, event):
        label = self.dicTxtID_Label[event.GetId()]
        self.dicTxtID_NewText[ label ] = event.GetString()
        #event.Skip()
        
    def OnClickSave(self, event):
        for key, val in self.dicTxtID_NewText.items():
            self.obj.__dict__[key] = val
            if val=="":
                msg = self.obj.setNull(key)
                print msg
                if msg:
                    self.dicLabel_Txt2[key].SetBackgroundColour((159, 213, 197))
                else:
                    self.dicLabel_Txt2[key].SetBackgroundColour('Red')
                self.Refresh()
            else:
                msg = self.obj.update(key)
                print msg
                if msg:
                    self.dicLabel_Txt2[key].SetBackgroundColour((159, 213, 197))
                else:
                    self.dicLabel_Txt2[key].SetBackgroundColour('Red')
                self.Refresh()
        self.dicTxtID_NewText = {}
        #event.Skip()
        
    def OnClickInsert(self, event):
        for key, val in self.dicTxtID_NewText.items():
            self.obj.__dict__[key] = val
        msg = self.obj.insert()
        print msg
        if msg:
            for key, val in self.dicTxtID_NewText.items():
                self.dicLabel_Txt2[key].SetBackgroundColour((159, 213, 197))
                self.btn_insert.Show(False)
        else:
            for key, val in self.dicTxtID_NewText.items():
                self.dicLabel_Txt2[key].SetBackgroundColour('Red')
        self.Refresh()
        #event.Skip()
        
    def OnDblClick(self, event):
        "Show a signle field form."
        d = self.dicTxtID_Label[event.GetId()]
        print d
        frame = FrmSingleField(self, self.obj, d)
        
        frame.Show(True)
        #event.Skip()

    def OnClose(self, event):
        print "OnClose 4"
        self.parent.Close()
        #event.Skip()
### -HeadedGrid- ###


class TestPannel(PagePannelBase):
    def __init__(self, parent, obj, insertForm=False):
        self.insertForm = insertForm
        PagePannelBase.__init__(self, parent, obj)
        
    def initHeader(self):
        pass
    
    def initPages(self):
            
        lst = ['id', 'pid', 'givenname', 'familyname', 'position']
        self.createPage(lst, "Person")

        lst = ['email', 'phoneextension', 'mobile']
        self.createPage(lst, "Contact Information")
              
class FrmPannel(wx.MDIChildFrame):
    
    def __init__(self, parent, obj, insertForm=False):

        self.parent = parent
                               
        wx.MDIChildFrame.__init__(self, parent, id=-1, title='',
                          size=(550,400))

        panel = TestPannel(self, obj, insertForm)
        

class FrmOptions(wx.MDIChildFrame, CtrWCloseUtil):
    
    def __init__(self, parent):

        self.parent = parent
                               
        wx.MDIChildFrame.__init__(self, parent, id=-1, title='Options',
                          size=(550,400))

        panel = wx.Panel(self, -1)
        
        CtrWCloseUtil.__init__(self)
        
        app = wx.GetApp()
        
        self.txt_floatFormat = wx.TextCtrl(panel, -1, app.MY_FLOAT_FORMAT, size=(100, 21),pos=(10, 10))
        self.btn_floatFormat = wx.Button(panel, -1, 'Update float', pos=(10, 30))
        self.Bind(wx.EVT_BUTTON, self.OnButtonFloatFormat, self.btn_floatFormat)
        
        self.txt_decimalFormat = wx.TextCtrl(panel, -1, app.MY_DECIMAL_FORMAT, size=(100, 21),pos=(10, 70))
        self.btn_decimalFormat = wx.Button(panel, -1, 'Update decimal', pos=(10, 100))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDecimalFormat, self.btn_decimalFormat)

        self.txt_dateFormat = wx.TextCtrl(panel, -1, app.MY_DATE_FORMAT, size=(100, 21),pos=(10, 140))
        self.btn_dateFormat = wx.Button(panel, -1, 'Update date', pos=(10, 170))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDateFormat, self.btn_dateFormat)
                
    def OnButtonFloatFormat(self, evt):
        n_txt = self.txt_floatFormat.GetValue().strip()
        app = wx.GetApp()
        app.MY_FLOAT_FORMAT = n_txt
        
        
    def OnButtonDecimalFormat(self, evt):
        n_txt = self.txt_decimalFormat.GetValue().strip()
        app = wx.GetApp()
        app.MY_DECIMAL_FORMAT = n_txt
        
    def OnButtonDateFormat(self, evt):
        n_txt = self.txt_dateFormat.GetValue().strip()
        app = wx.GetApp()
        app.MY_DATE_FORMAT = n_txt
                        
class ButtonForm(wx.MDIChildFrame, CtrWCloseUtil):
#class ButtonForm(wx.Frame):
    """This class lets you add an external module (see plan_2010) and buttons
so that you can call the methods and display these in the application."""
    def __init__(self, parent):

        self.parent = parent
                               
        wx.MDIChildFrame.__init__(self, parent, id=-1, title='Button Form',
                          size=(550,400))
# wx.Frame.__init__(self, parent, id=-1, title='Button Form',
# size=(550,400))
        CtrWCloseUtil.__init__(self)
        self.panel = wx.Panel(self, -1)
        self.x = 20
        self.y = 20
        
    def addButton(self, text, method):
        id = wx.NewId()
        btn = wx.Button(self.panel, id, text, pos=(self.x, self.y))
        self.Bind(wx.EVT_BUTTON, method, btn)
        
        self.y += 30
        
### -Execute sql statements in the database- ###

class SqlExecForm(wx.Frame, CtrWCloseUtil):
    """Execute sql in this database."""
    def __init__(self, parent=None, title='SQL Execution'):

        wx.Frame.__init__(self, parent, id=-1, title='SQL Execution',
                          pos=wx.DefaultPosition, size=(600,600), style=wx.DEFAULT_FRAME_STYLE)
        CtrWCloseUtil.__init__(self)
        
        self.panel = wx.Panel(self, -1)
        
        v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.txt_sql = wx.TextCtrl(self.panel, -1, 'asdsa',
                               style=wx.EXPAND)
        self.curFont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.curClr = None
        #self.curFont = None
        #self.txt_sql.SetFont(self.font)
        
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_exec = wx.Button(self.panel, -1, "Exceute")
        self.Bind(wx.EVT_BUTTON, self.OnSelectFont, self.btn_exec)
        self.btn_exec2 = wx.Button(self.panel, -1, "Exceute")
        self.Bind(wx.EVT_BUTTON, self.OnSelectFont, self.btn_exec2)
                
        h_sizer.Add(self.btn_exec, 0, wx.BOTTOM)
        h_sizer.AddSpacer(10)
        h_sizer.Add(self.btn_exec2, 0, wx.BOTTOM)
        
        v_sizer.Add(self.txt_sql, 5, wx.EXPAND|wx.ALL|wx.BOTTOM)
        v_sizer.Add(h_sizer)
        
        self.panel.SetSizer(v_sizer)
        
        self.UpdateUI()
        
    def OnBtnClick(self, event):
        pass
    
    def OnSelectFont(self, evt):
        data = wx.FontData()
        data.EnableEffects(True)
        data.SetColour(self.curClr) # set colour
        data.SetInitialFont(self.curFont)

        dlg = wx.FontDialog(self, data)
        
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            colour = data.GetColour()

            self.curFont = font
            self.curClr = colour
            self.UpdateUI()

        # Don't destroy the dialog until you get everything you need from the
        # dialog!
        dlg.Destroy()

    def UpdateUI(self):
        self.txt_sql.SetFont(self.curFont)
        self.txt_sql.SetForegroundColour(self.curClr)
        self.Layout()
        


                
class DevelopmentForm(wx.Frame, CtrWCloseUtil):
    """For used for test and development."""
    def __init__(self, parent, ID=-1, title='Test form', pos=wx.DefaultPosition,
                 size=(600,500), style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        CtrWCloseUtil.__init__(self)
        
        #just emulating a controller here for now ...
        q = session_rcl.query(DbMessage)
        print len(q.all())
        
        new_msg = q.first()
        pannel = MessagePanel(self, new_msg)
        

class FrmContract(wx.Frame):
    
    def __init__(self, obj):
                               
        wx.Frame.__init__(self, parent=None, id=-1, title='',
                          size=(550,400))

        #panel = TestPannel(self, obj, insertForm)
                
    
def createFrmContractinGUI(contract_id):
    "Use this method to create a contract view in the GUI from eval"

    frm = FrmContract( contract_id )
    frm.Show()
    
def a(event):
    print "method a"
def b(event):
    print "method b"

def docCreateIcon():
    "This is how I created the icon."
    from wx.tools import img2py
    #img2py.img2py("xls.ico", 'xls_ico.py',icon=True)
    img2py.img2py("ssc_logo_3.ico", 'ssc_logo_3.py',icon=True)
    
def run():
    "Run the main program from here."
    import sys
    from wx_piv_app import main
    main(sys.argv)

if __name__=='__main__':
    
    run()

# const.user='ahetland'
#     wx.SetDefaultPyEncoding('utf-8')
#     app = wx.PySimpleApp()
#     
#     frame = FrmContract(None)
#     frame.Show()
# # #app =wx.GetApp()
# ## app.mdi_parent_frame = None
# ## frame = ButtonForm(None)
# ## frame.addButton('first',a)
# ## frame.addButton('second',b)
# ## frame.Show(True)
# #
#     app.MainLoop() 