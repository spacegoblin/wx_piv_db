#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.grid
import wx.lib.gridmovers as gridmovers

import datetime
import decimal
#from mx.DateTime import DateTimeType as mxDateTimeType

class MyGridTable(wx.grid.PyGridTableBase):
    def __init__(self, lst):
        self.lst = lst
        try:
            self.lst.sort(0)
        except: pass
        wx.grid.PyGridTableBase.__init__(self)
        
        self.evenAttr = wx.grid.GridCellAttr()
        self.evenAttr.SetBackgroundColour('white')
        self.evenAttr.SetAlignment(wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
        self.evenAttr.SetOverflow(False)
        
        self.oddAttr = wx.grid.GridCellAttr()
        self.oddAttr.SetBackgroundColour((235,235,235))
        self.oddAttr.SetAlignment(wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
        self.oddAttr.SetOverflow(False)
        
# self.dataTypes = [wx.grid.GRID_VALUE_NUMBER,
# wx.grid.GRID_VALUE_STRING,
# wx.grid.GRID_VALUE_CHOICE + ':Approved,Approved w. remarks,Revisit,Cancelled,Going to Yellow',
# wx.grid.GRID_VALUE_STRING
# ]
# self.dataTypes = dataTypes
        
# def GetTypeName(self, row, col):
# if self.dataTypes:
# return self.dataTypes[col]
# else: return ''
#
# def CanGetValueAs(self, row, col, typeName):
# if self.dataTypes:
# colType = self.dataTypes[col].split(':')[0]
# if typeName == colType:
# return True
# else:
# return False
        self.identifiers = self.lst.fieldnames
        
    def GetNumberRows(self):
        return self.lst.GetNumberRows()

    def GetNumberCols(self):
        return self.lst.GetNumberCols()
    
    def IsEmptyCell(self, row, col):
        return self.lst.get(row, col) is not None

    def GetValue(self, row, col):
        value = self.lst.get(row, col)
        if value is not None:
            
            if type(value)==datetime.datetime:
                try:
                    return value.strftime( wx.GetApp().MY_DATE_FORMAT )
                except:
                    print row, col, value, "Error in date returned"
                    return str(value)
                
            elif type(value)==datetime.date:
                
                return value.strftime( wx.GetApp().MY_DATE_FORMAT )
                            
# elif type(value)==mxDateTimeType:
# return value.strftime('%Y-%m-%d')

            elif type(value)==float:

                fmt = "{:%s}" % wx.GetApp().MY_FLOAT_FORMAT
            
                try:
                    return fmt.format(value)
                except ValueError:
                    return value
                

            elif type(value)==decimal.Decimal:
                #return "{:,.2f}".format(value)
                try:
                    fmt = "{:%s}" % wx.GetApp().MY_DECIMAL_FORMAT
                except AttributeError:
                    fmt = "{:,.2f}"
                return fmt.format(value)
            
            return value
        else:
            return ''

    def SetValue(self, row, col, value):
        #self.lst[(row, col)] = value
        self.lst.set(row, col, value)
        
    def GetColLabelValue(self, col):
        return self.lst.fieldnames[col]

# def GetTypeName(self, row, col):
# if col>0 and row>0:
# return wx.grid.GRID_VALUE_FLOAT + ':,2'
# else:
# return wx.grid.GRID_VALUE_STRING
#
#
# def CanGetValueAs(self, row, col, typeName):
# return False
        #colType = self.dataTypes[col].split(':')[0]
# print "xxxxx"
# print typeName
# if typeName == '':
# return True
# else:
# return False
    # Move the column
    def MoveColumn(self,frm,to):
        grid = self.GetView()

        if grid:
            # Move the identifiers
            old = self.identifiers[frm]
            del self.identifiers[frm]

            if to > frm:
                self.identifiers.insert(to-1,old)
            else:
                self.identifiers.insert(to,old)

            # Notify the grid
            grid.BeginBatch()
            msg = wx.grid.GridTableMessage(
                    self, wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED, frm, 1
                    )
                    
            grid.ProcessTableMessage(msg)
            
            msg = wx.grid.GridTableMessage(
                    self, wx.grid.GRIDTABLE_NOTIFY_COLS_INSERTED, to, 1
                    )

            grid.ProcessTableMessage(msg)
            grid.EndBatch()
            

    def GetAttr(self, row, col, kind):
        attr = [self.evenAttr, self.oddAttr][row % 2]
        try:
            attr.IncRef()
            return attr
        except: pass
        
    def AppendRows(self, numRows=1):
        #print "len append", (len(self.lst) + numRows)
        #print "got here", (self.GetNumberRows() + numRows)
        return self.GetNumberRows() + numRows
        #return True
        
# def DeleteCols(self, pos):
# print "got here"
# self.DeleteCols(pos, 1)
# return True
    def RemoveColumn(self, colNum):
        self.lst.pop(colNum)
        self.GetView().ProcessTableMessage(wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED,
                                                                    len(self.lst.fieldnames), 1))
        
    def RemoveData(self, rowNum):
        #print "len lst", len(self.lst)
        self.lst.popRow(rowNum)
        #print "after pop", len(self.lst)
        self.GetView().ProcessTableMessage(wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,
                                                                    len(self.lst), 1))
    def RemoveRange(self, idx_from, idx_to):
        self.lst.deleteRange(idx_from, idx_to)
        removed = idx_to - idx_from
        self.GetView().ProcessTableMessage(wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,
                                                                    len(self.lst), removed))
#ProcessTableMessage(wx.grid.GridTableMessage(
# self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, len(data), 1))
    
class MyGrid(wx.grid.Grid):
    def __init__(self, parent, lst):
        wx.grid.Grid.__init__(self, parent, -1)
        self.SetTable(MyGridTable(lst),True)
        self.Fit()

        # Enable Column moving
        gridmovers.GridColMover(self)
        self.Bind(gridmovers.EVT_GRID_COL_MOVE, self.OnColMove, self)

    # Event method called when a column move needs to take place
    def OnColMove(self,evt):
        frm = evt.GetMoveColumn() # Column being moved
        to = evt.GetBeforeColumn() # Before which column to insert
        self.GetTable().MoveColumn(frm,to)
                        
# def NewTable(self, lst):
# self.SetTable(MyGridTable(lst),True)
# self.Refresh()
# self.Fit()
       
if __name__=='__main__':
    from wx_piv_app import main
    main(None)
# from ahutils.record import loadFromDb, WhichDb_v3
# Db=WhichDb_v3('Postgress', None)
# lst = loadFromDb("select * from tbljde_accounts")
# print len(lst)