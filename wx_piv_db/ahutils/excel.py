# Excel demos from doubletalk
import win32com.client
import win32com.client.dynamic
from pywintypes import UnicodeType, TimeType

import pprint
import os
import time
import string
import sys

SHEET_NAME = 'Sheet1'

class easyExcel:
    """A utility to make it easier to get at Excel.  Remembering
    to save the data is your problem, as is  error handling.
    Operates on one workbook at a time."""
    
    def __init__(self, filename=None):
        self.xlApp = win32com.client.dynamic.Dispatch('Excel.Application')
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename = ''  
    
    def save(self, newfilename=None):
        if newfilename:
            self.filename = newfilename
            self.xlBook.SaveAs(newfilename)
        else:
            self.xlBook.Save()

    def close(self):
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp
   
    def show(self):
        self.xlApp.Visible = 1
        
    def hide(self):
        self.xlApp.Visible = 0
        
    def doPivot(self):
        from win32com.client import constants as cnst#, Dispatch
        #xl = Dispatch('Excel.Application')
        xl = self.xlBook
        #xl.ActiveWorkbook.SaveAs(r'd:\pivottable.xls')
        ws = xl.Worksheets(SHEET_NAME)
        pc = xl.PivotCaches().Add(cnst.xlExternal)
        pc.Connection = r'ODBC;DSN=MS Access Database;DBQ=d:\test.mdb;'
        pc.CommandType = cnst.xlCmdSql
        pc.CommandText = 'SELECT * FROM whatever'
        pc.CreatePivotTable(ws.Cells(3,1),'pivot')
        #xl.ActiveWorkbook.Save()

#
#    now for the helper methods
#
    def getCell(self, sheet, row, col):
        "Get value of one cell"
        sht = self.xlBook.Worksheets(sheet)
        return sht.Cells(row, col).Value
    
    def setCell(self, sheet, row, col, value):
        "set value of one cell"
        sht = self.xlBook.Worksheets(sheet)
        sht.Cells(row, col).Value = value
        
    def setNamedCell(self, sheet, name, value):
        "set value of a named cell"
        sht = self.xlBook.Worksheets(sheet)
        sht.Range(name).Value = value    

    def getNamedRange(self, sheet, row, col):
        """Tracks down and across from top left cell until it
        encounters blank cells; returns the non-blank range.
        Looks at first row and column; blanks at bottom or right
        are OK and return None witin the array"""
        sht = self.xlBook.Worksheets(sheet)
        return sht.Range(sht.Cells(1, 1), sht.Cells(row, col)).Value
        
    def getRange(self, sheet, row1, col1, row2, col2):
        "return a 2d array (i.e. tuple of tuples)"
        sht = self.xlBook.Worksheets(sheet)
        return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value
    
    def setRange(self, sheet, leftCol, topRow, data):
        """insert a 2d array starting at given location. 
        Works out the size needed for itself"""
        
        bottomRow = topRow + len(data) - 1
        rightCol = leftCol + len(data[0]) - 1
        sht = self.xlBook.Worksheets(sheet)
        sht.Range(
            sht.Cells(topRow, leftCol), 
            sht.Cells(bottomRow, rightCol)
            ).Value = data

    def getContiguousRange(self, sheet, row=1, col=1):
        """Tracks down and across from top left cell until it
        encounters blank cells; returns the non-blank range.
        Looks at first row and column; blanks at bottom or right
        are OK and return None witin the array"""
        
        sht = self.xlBook.Worksheets(sheet)
        
        # find the bottom row
        bottom = row
        while sht.Cells(bottom + 1, col).Value not in [None, '']:
            bottom = bottom + 1
        
        # right column
        right = col
        while sht.Cells(row, right + 1).Value not in [None, '']:
            right = right + 1
        
        return sht.Range(sht.Cells(row, col), sht.Cells(bottom, right)).Value

    def getNamedRange(self, sheet, row, col):
        """Tracks down and across from top left cell until it
        encounters blank cells; returns the non-blank range.
        Looks at first row and column; blanks at bottom or right
        are OK and return None witin the array"""
        return sht.Range(sht.Cells(0, 0), sht.Cells(row, col)).Value
     
    def fixStringsAndDates(self, aMatrix):
        # converts all unicode strings and times
        newmatrix = []
        for row in aMatrix:
            newrow = []
            for cell in row:
                if type(cell) is UnicodeType:
                    newrow.append(str(cell))
                elif type(cell) is TimeType:
                    newrow.append(int(cell))
                else:
                    newrow.append(cell)
            newmatrix.append(tuple(newrow))
        return newmatrix
    
        
def test():
    # puts things in a new sheet which it does not save
    spr = easyExcel()
    spr.show()
    
    input = 'hello'
    spr.setCell(SHEET_NAME,1,4, input)
    output = spr.getCell(SHEET_NAME,1,4)
    assert input == output, 'setCell/getCell failed'
    
    input = []
    for i in range(10):
        row = []
        for j in range(4):
            row.append(str('(%d,%d)'% (j, i)))
        input.append(tuple(row))
    
    spr.setRange(SHEET_NAME,2,2,input)
    
    output = spr.getRange(SHEET_NAME,2,2,11,5)
    # get rid of unicode strings
    output = spr.fixStringsAndDates(output)
    assert input == output, 'setRange/getRange test failed'
    
    #get a contiguous range
    output2 = spr.getContiguousRange(SHEET_NAME, 2,2)
    dimensions = (len(output2), len(output2[0]))
    assert dimensions == (10, 4), 'getContiguousRange failed'
    
    print 'passed!'

if __name__=='__main__':
    test()
    