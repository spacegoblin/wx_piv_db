#!/usr/bin/python
# -*- coding: utf-8 -*-

"""The record module is the ORM module for my home grown ORM solution. The main
classes in use are RecordList and Record. RecordList is a list of objects of type record,
or any other object. The factory method loadFromDb loads a RecordList into memory."""


import wx

import sys
if '..//' not in sys.path:
    sys.path.append('..//')
        
        
from ahutils import db
from ahutils.db import dictToUpdate, dictToInsert, insertBlobSql
from mx.DateTime import DateTimeType as DateTimeType
from ahconfig import const


import re
import copy
import pprint

import cPickle
import psycopg2
import base64
from exceptions import Exception


import datetime


class GUICodeNotExisting(Exception):
    pass


#from wx_forms import GenericMsgDlg
#above did not work so copy and paste
def GenericMsgDlg(message, caption, styles=wx.OK | wx.ICON_INFORMATION):
    """
    Create a message dialog with the passed in parameters
    """
    try:
        dlg = wx.MessageDialog(None, message, caption, styles)
        result = dlg.ShowModal()
        dlg.Destroy()
    except:
        print "Could not create wx message, Error is printed instead:\n"
        print message
        raise ("Error")
    return result 


def WhichDb_v3(Driver, DbSelection, user=None, password=None):
    print "WhichDb_v3"

    from db import setQuote

    if Driver=='Postgress':
        setQuote('Postgress')
        globals()['Db'] = db.This_Db(DbSelection, user, password)
        return globals()['Db']

    elif Driver=='sqlite':
        globals()['Db'] = db.Sqlite(dbName, user, password)
        return globals()['Db']

    else:
        raise("You must set the database driver and dsn first to get a connection.")
        
    
    
def funcToMethod(func,clas,method_name=None):
    """Adds a method to a class dynamically.
    
    >>> def tester(self):
    >>>     return "this is a tester"
    >>>
    >>> funcToMethod(tester, Record)
    >>> t=Record('none')
    >>> print t.tester()
    this is a tester
    """
    import new
    method = new.instancemethod(func,None,clas)
    if not method_name: method_name=func.__name__
    setattr(clas, method_name, func)


class MetaRecord(object):
    """Class that adds meta information to a Record object.
    The MetaReoord can take binary data search keys and categories."""

    def __init__(self, parent):
        self.id = None
        self.parent= parent #this is the object itself
        self.base_table = self.parent.base_table
   
    def getDbNextId(self):
        sql = "select nextval('tbl_meta_id_seq')"
        Db.c.execute(sql)
        self.id = Db.c.fetchone()[0]
        return self.id
    
    
    def insertBlob(self, fname, pathWithFileName):
        
        sql = insertBlobSql(fname, pathWithFileName, self.parent.id, self.base_table)
        
        try:
            Db.c.execute(sql)
            Db.commit()
            #return True
        except: return False
        
        sql_id = "select max(id) from tbl_meta where base_table='%s' and parent_id=%d" % (self.base_table, self.parent.id)
        Db.c.execute(sql_id)
        m_id = Db.c.fetchone()[0]
        
        sql_lnk = """insert into tbl_meta_link (parent_id, 
        base_table, meta_id) values (%d, '%s', %d)""" % (self.parent.id, self.base_table, m_id)
        
        print m_id, "m_id"
        
#        try:
        Db.c.execute(sql_lnk)
        Db.commit()
        return True
#        except: return False
                        
        
    def getBlob(self, dbId):
        import cStringIO
        sql = "select blob from tbl_meta where id=%d" % dbId
        Db.c.execute(sql)    
        stream = base64.b64decode(Db.c.fetchone()[0].strip())
        stream = cStringIO.StringIO(stream)
        return stream
    
    def getBlobbyBlobId(self, blobId):
        """If the id of the blob (the primary key in the meta table),
        has been entered in the table then you can fetch the blob from here.
        
        The reason for this method is that this was refactored. The field name for the
        id_blob did not (and probably does not) exist in earlier table. This meant that
        one record could only hold several documents, but one document could not
        reference several records. This is still not the best solution as I should use
        a many to many relationship, however given that I would like to be able to use
        access this is stil not possible as I cannot get the auto increment for next_id in access. (MS sucks!)"""
        #this was implemented through getFileNames()
        pass      


    def getFileNames(self):
        sql = """select id, filename from tbl_meta 
        where parent_id=%d and base_table='%s'""" % (self.parent.id, self.base_table)
        print "SQL in record getFileNames", sql
        Db.c.execute(sql)  
        __lst = Db.c.fetchall()
        try:
            idBlob = getattr(self.parent, 'id_blob', None)
            if idBlob:
                #there can only be one additional id to fetch
                sql = """select id, filename from tbl_meta 
                where id=%d""" % (idBlob)
                #print "Blob id getter refactored ", sql
                Db.c.execute(sql)  
                __lstadd = Db.c.fetchone()                
                __lst.append(__lstadd)
        except: pass
        return __lst
        

   
        
class Record(object):
    "Single database aware record"
    def __init__(self, base_table):
        self.base_table = base_table
        #self._parent = None THIS DID NOT WORK, to heavy on the resources
        self.value_field = None
        #self.linked_redords = None  #a list of related objects       
    

    def __str__(self):
        #return "Object dict: %s" % self.__dict__
        return pprint.pformat(self.__dict__, indent=4)
        
    
    def __call__(self, attr):
        "Returns the attribute value called."
        return self.__dict__[attr]
    
    def __len__(self):
        return len(self.__dict__)
        
    def __repr__(self):
        return "%s" % self.__dict__
    
    #SOME MATH ON THE RECORD
    def __mul__(self, val):
        "Multiply the value field with the number."
        setattr(self, self.value_field,  getattr(self, self.value_field) * val ) 

    def __add__(self, val):
        "Add the value field with the number."
        setattr(self, self.value_field,  getattr(self, self.value_field) + val ) 

    def __sub__(self, val):
        "Subtract the value field with the number."
        setattr(self, self.value_field,  getattr(self, self.value_field) + val ) 

    def __div__(self, val):
        "Divide the value field with the number."
        setattr(self, self.value_field,  getattr(self, self.value_field) + float(val) ) 
    #END MATH ON RECORD
                       
    def items(self):
        raise('in use?')
        for x, y in self.__dict__.items():
            yield x, y
        
    def copy(self):
        "make a deep copy"
        cop = copy.deepcopy(self)
        return cop
    
    def copyEmpty(self):
        cp = self.copy()
        for key, val in cp.__dict__.items():
            val = None
        return cp
    
    def comDate(self, key):
        return self.__dict__[key].COMDate()
    
    def compare(self, other, fieldlist=None):
        """Should return a negative integer if self < other, 
        zero if self == other, 
        a positive integer if self > other"""
        if fieldlist:
            raise NotImplementedError("This functionality has not yet been implemented")
        
        for k, v in self.__dict__.items():
            #if k is not '_parent':
            #refactor out parent
            if not k =='id':
                if type(v)==int or type(v)==float:
                    if v > getattr(other, k):
                        #print k,v
                        return 1
                    elif v < getattr(other, k):
                        #print k,v
                        return -1
                    else: pass
                elif v == getattr(other, k):
                    pass
                else: 
                    #print k,v
                    return -1, k, v
        return 0
                
            
        
    def values(self, valueList=None):
        if valueList:
            for key in valueList:
                try:
                    #yield self.__dict__[key]
                    yield getattr(self, key)
                except:
                    yield None
        else:
            for key in self.__dict__:
                yield self.__dict__[key]
            

    
    def update(self, *arg):
        """table is the table against to update
        dict is a dictionary with field value pairs to update
        """

        d = {}
        if arg:     
            for attr in arg:
                d[attr]=self.__dict__[attr]
        else:
            d = copy.deepcopy(self.__dict__)
            d.pop('base_table')
            d.pop('value_field')
            #d.pop('_parent')
            d.pop('id')
           # d.pop('_parent')
           #refactor out parent     
        sql = dictToUpdate(d, self.base_table, id=self.id)
                        
        try:
            Db.c.execute(sql)
            Db.cnn.commit()           
        except Exception, e:
            print sql
            print str(e)
            GenericMsgDlg(str(e), 'Other error', wx.OK | wx.ICON_INFORMATION)
            Db.resetConnection()
            return False   
        return sql
    
      
        
    def insert(self, fields=None, sqlString=None):
        """insert into datanase. 
        If args: fields inserts fields only, 
        sqlString=True returns only string to be executed"""
        dict = {}
        
        if fields:
            #pass as argument the fields you want to have inserted
            for d in fields:
                if not d in ['id','base_table', 'value_field']:
                    print self
                    dict.update({d:getattr(self, d)})            
        else:
            for d in self.__dict__:
                if not d in ['id','base_table', 'value_field']:
                    dict.update({d:self.__dict__[d]})
        
        
        sql = dictToInsert(dict, self.base_table)
        
        if sqlString:
            return sql

        try:
            Db.c.execute(sql)
            Db.cnn.commit()

        except psycopg2.IntegrityError, e:
            
            print sql
            print str(e)
            Db.resetConnection()
            GenericMsgDlg(str(e), 'Integrity error', wx.OK | wx.ICON_INFORMATION)
            return False
        except psycopg2.DataError, e:
            print sql
            print str(e)
            GenericMsgDlg(str(e), 'Data error', wx.OK | wx.ICON_INFORMATION)
            
            Db.resetConnection()
            return False 
        except psycopg2.ProgrammingError, e:
            
            print sql
            print str(e)
            GenericMsgDlg(str(e), 'Programming error', wx.OK | wx.ICON_INFORMATION)
            
            Db.resetConnection()
            return False             
        except Exception, e:
            GenericMsgDlg(str(e), 'Other error', wx.OK | wx.ICON_INFORMATION)
            print sql
            print str(e)
            Db.resetConnection()
            return False   
#        t3 = datetime.datetime.now()
#        print "Time to insert %s" % (t3-t2)
         
        return sql
        
    def delete(self):
        sql = "delete from %s where id=%d" % (self.base_table, self.id)
        try:
            Db.c.execute(sql)
            Db.cnn.commit()
            return sql
        except Exception, e:
            print str(e)
            print sql
            
            GenericMsgDlg(str(e), 'Error deleting.', wx.OK | wx.ICON_INFORMATION)

            Db.resetConnection()
            return False
        
    def search(self, searchStr, field=None):
        """Search for searchStr in the record. Either all fields or only named field
        searchStr: the string that is searched for
        field: None if searching in entire object, field attribute name if only in that field
        Returns the Object when True 
        False if nothing found
        """       

        try:
            a, b = searchStr.split('+')
            searchStr = '(%s.+%s)|(%s.+%s)' % (a, b, b, a)
            s = re.compile(unicode(searchStr), re.IGNORECASE|re.UNICODE)
        except:
            s = re.compile(unicode(searchStr), re.IGNORECASE|re.UNICODE)
                
        if field is None:

            strng = ["%s" % val for val in self.__dict__.values()]
            
            strng = ' '.join(strng)
            
            if s.findall(strng):
                return self
            else: return False

        else:
            if s.findall(self.__dict__[field]):
                return self
            else: return False

        
    def setNull(self, field):
        "Sets db the enrty to null."
        sql = "update %s set %s = Null where id=%d" % (self.base_table, field, self.id)
        Db.c.execute(sql)
        Db.cnn.commit()
        return sql

    def executeSql(self, sql):
        """Execute an arbritary sql statement,
        WARNING this method is dangerous and must be confirmed first!"""
        sq = sql
        
        def do(confirm):
            if confirm:
                print "executing: %s" % sq
                try:
                    Db.c.execute(sql)
                    Db.cnn.commit()
                
                except psycopg2.ProgrammingError, e:
                    print str(e)
                    print sql
                    Db.resetConnection()
                    return False                    
                
                except Exception, e:
                    print str(e)
                    print sql
                    Db.resetConnection()
                    return False
            else:
                return False

        return do
     
    
    def deleteAttr(self, *attr):
        "pops the entries, self.__dict__.pop()"
        for att in attr:
            self.__dict__.pop(att)
            

    def OnRecordDblClick(self):
        """This method can be used to call code to be executed when the object is double clicked.
        An usage example could be to create a custom defined form for the object, or to define special jumps etc."""
        raise GUICodeNotExisting("Must be overridden. This event can be used to overwrite the double click event in the GUI.")

          
class RecordAlchemy(Record):
    """A mix inn class for alchemised records.
    
    Usage example:
    
    class PersonAlchemy(Person, RecordAlchemy):
        session = getSession()  #static attribute set only once
    def __init__(self):
        super(RecordAlchemy, self).__init__()
        
    """
    
    def __init__(self):
        print "init RecordAlchemy"
        super(RecordAlchemy, self).__init__()
        
        
    def fieldnames(self):
        raise("must be overridden")
        
    def getBaseTable(self):
        return self.__tablename__
    
    base_table = property(getBaseTable)

    def set(self, key, val):
        setattr(self, key, val)
        
    def insert(self):
        raise
    
    def copy(self):
        raise('This method must be overridden to work, see example in startup model')
    
    def update(self, *arg):
        self.session.commit()
        return True
    
                        
class RecordList(object):
    """A list of objects of class Record."""
    def __init__(self, valuefield=None):
        self.isPivoted = False
        self.data = []
        self.fieldnames = []
        self.fieldnames_original = False
        self.field_types = []
        self.value_field = valuefield 
        self.sql = ''
        self.base_table = None
        self.pivot_left = None
        self.pivot_top = None
#        self.copyOfOrg = False
#        self.dicSqlJumps = {}
        self.dicExecCode = None
        self.view_id = None #this is the id of the views defined in the database
        
    def append(self, obj):
        obj.value_field = self.value_field
        #obj.base_table = self.base_table some of the updates seem not to work with this
        self.data.append(obj)

    def loadFromDb(self, sql, table_name="<NO_UPDATE_TABLE>", value_filed=None):
        """Returns a recordset from an sql statement.
        
        Example sql::
        >>> WhichDb_v3('Postgres', None)
        >>> sql = "select * from tbb_period where year=2007"
        >>> lst = loadFromDb(sql)
        >>> print len(lst)
        12
        """
        raise("Use the factory method instead")


    def loadFromAlchemy(self, query, table_name, base_record):
        """Loads an sql alchemy query object."""
        raise("Use the factory method instead")

        
    def appendWithNewAttribute(self, obj):
        """Adding a new object to instance, when the object has an
        unknow attribute."""
        tmp = obj.__dict__.keys()
        for t in tmp:
            if t not in self.fieldnames:
                self.fieldnames.append(t)
        self.data.append(obj)
        
    def appendAttributeOnly(self, attribute):
        "Adds a new attribute to the objects, their value set to None"
        if attribute not in self.fieldnames:
            self.fieldnames.append(attribute)
        else: raise("This attribute exists allready")
        for objx in self.data:
            objx.attribute = None
        
    def extend(self, otherRecordList):
        "Extends this list with the list of same type other"
        self.data = self.data + otherRecordList.data
        
    def __call__(self):
        raise("does not seem useful, is this used")
        return self.data
    
    def __iter__(self):
        "Iterator yields objects in self.data"
        if self.isPivoted:
            for obj in self.pivot_data:
                yield obj
        else:         
            for obj in self.data:
                yield obj
    
    def yieldValues(self):
        assert self.value_field, 'The value_field must be set.'
        if self.isPivoted:
            for obj in self.pivot_data:
                yield float( getattr(obj, self.value_field ) )
        else:         
            for obj in self.data:
                yield  float( getattr(obj, self.value_field ) )
    
    def __getitem__(self, index):
        "Returns object by index in self.data"
        if self.isPivoted:
            print "isPivoted"
            raise ("Why would I want to use this, gets ugly with SQLAlchemy ... ")
            return self.pivot_data[index]
        else:
            return self.data[index]
    
    def __len__(self):
        "Returns len(self.data)"
        if self.isPivoted:
            return len(self.pivot_data)
        else:
            return len(self.data)
    
    def fieldList(self, field):
        "Returns a unique list of the specified field."
        dicUnique = {} #unique values
        for r in self:
            dicUnique[getattr(r, field)] = 1
#        _str = ','.join(str (dicUnique.keys()) )
#        return ':'+_str
        return dicUnique.keys()
            
    def getTable(self):
        """The table returns the data, as self returns
        object records."""
    
        tmp = []
        tmp.append(tuple(self.fieldnames))
        for obj in self.data:
            #print obj.valueTuples(self.fieldnames)
            #refactoring so as to get rid of dependency on record above
            tmp_2 = []
            for f in self.fieldnames:
                tmp_2.append( getattr(obj, f) )
            #tmp.append(obj.valueTuples(self.fieldnames))
            tmp.append(tmp_2)
        return tmp
    table = property(getTable)
    
    def csv(self, fname='C:\\home\\test.csv'):
        "instead of xls return a csv file"
        import csv
        from cStringIO import StringIO
        
        try:
            s = StringIO()
            writer = csv.writer(s)
        
            writer.writerow(self.fieldnames)
            
            for obj in self.data:
                tmp = []
                for f in self.fieldnames:
                    val = getattr(obj, f)
                    if isinstance(val, str) or isinstance(val, unicode):
                        val = val.encode('iso-8859-1')
                    tmp.append( val )
                writer.writerow(tmp)
        finally:
            f = open(fname, mode='w+b')
            f.writelines( s.getvalue() )
            f.close()
        
    def convertPivotSheetToTable(self, fileName='C:\home\default_db.csv', colFixed=3, rowFixed=1):
        """We want to convert a pivoted table to a databse flat table.
        fileName: path and name of new csv file
        colFixed: left side columns number of columns that has been pivoted
        rowFixed: default 1 top row in the pivot.
        """
        assert colFixed + rowFixed > 2, 'There must be both column and row defined'
        
        import csv
        
        f = open(fileName, mode='w+b')
        
        writer = csv.writer(f)
        
        writer.writerow(self.fieldnames[:colFixed] + ['A', 'B'])
        
        for head in  self.fieldnames[colFixed:]:
            print "head", head
            
            for obj in self.data:
                
                tmp_2 = []
                
                for f in self.fieldnames[:colFixed]:
                    tmp_2.append( getattr(obj, f) )
                
                tmp_2.append( head )
                tmp_2.append( getattr(obj, head) )
                
                writer.writerow(tmp_2)
                
        f.close()
        
    
    def getXlsTable(self):
        """The table returns the data, as self returns
        object records."""
        tmp = []
        tmp.append(tuple(self.fieldnames))
        for obj in self.data:
            #for key, atr in obj.items(): alchemy refactoring to below
            
            for key, atr in obj.__dict__.items():
                if type(atr) is DateTimeType:
                    obj.__dict__[key] = atr.COMDate()
                    #move up to record object to call
                if type(atr) is str:
                    obj.__dict__[key] = atr.decode('utf-8')
                    #move up to record object to call
            #tmp.append(obj.valueTuples(self.fieldnames))
            tmp_2 = []
            for f in self.fieldnames:
                try:
                    tmp_2.append( getattr(obj, f) )
                except TypeError:
                    print f, obj
            #tmp.append(obj.valueTuples(self.fieldnames))
            tmp.append(tmp_2)
        return tmp        
        
    xlsTable = property(getXlsTable)
    
    def xls(self):
        """Export the contents of the grid into an xls sheet."""
        assert len(self.fieldnames) > 1 #or else we get a bad list 
        from win32com.client import Dispatch
        xlApp = Dispatch('Excel.Application')
        xlBook = xlApp.Workbooks.Add()
        xlSheet = xlBook.Worksheets('Sheet1')
        
        rightCol = len(self.fieldnames)
        row = len(self.xlsTable)
        xlSheet.Range(xlSheet.Cells(1, 1),
                        xlSheet.Cells(row, rightCol)).Value = self.xlsTable

        xlApp.Visible = 1
        xlApp = None
            
    def get(self, row, col):
        "Returns the value for row, col for objects in a table."
        if self.isPivoted:
            try:
                obj = self.pivot_data[row]
                if obj.__class__.__name__=='list':
                    return self.pivot_data[row][col]
                else:
                    return getattr(obj, self.fieldnames[col])
            except: 
                return None
        else:
            try:
                obj = self.data[row]
                #print obj
                if obj.__class__.__name__=='list':
                    return self.data[row][col]
                else:
                    #return obj(self.fieldnames[col])
                    return getattr(obj, self.fieldnames[col])
            except: return None            
        
    def obj(self, **keys):
        "returns a list of the objects with that key"
#        print keys
        raise('Raised Oct 2012')
        key, val = keys.items()[0]
#        print getattr(self.data[0], key[0])
#        print key, val
        lst = [rec for rec in self.data if getattr(rec, key)==val ]
        assert len(lst) == 1
        return lst[0]

    def obj_2(self, **keys):
        """returns a list of the objects with that key
        without the one obj assertion."""
#        print keys
        raise('Raised Oct 2012')
        key, val = keys.items()[0]
#        print getattr(self.data[0], key[0])
        lst = [rec for rec in self.data if getattr(rec, key)==val ]

        return lst
       


    def loadExecCode(self):
        "This should be refactored ..... "
        if self.view_id:
            self.dicExecCode = {}
            sql = "select description, evalcode from tbl_eval where view_id=%d" % self.view_id
            Db.c.execute(sql)
            lst = Db.c.fetchall()
            if len(lst)>0:
                for rec in lst:
                    self.dicExecCode[rec[0]] = rec[1].strip()
                return True
            else:
                self.dicExecCode = None
                return False
        else: pass #return self.dicExecCode
            
        
    def set(self, row, col, value):
        """Sets the value of an attribute in an object, where
        the row is the object and col is the attribute."""
        if self.isPivoted:
            raise("You cannot set data directly in the pivot but must drill down to the record")
        else:
            obj = self.data[row]
            setattr(obj, self.fieldnames[col], value)
    
    def toDict(self, key, val):
        """Creates a dictionary of the key, val given."""
        dic = {}
        for obj in self:
            dic[getattr(obj, key)] = getattr(obj, val)
        return dic
    
    def compare(self, other, equalKey):
        """Compare objects of this list to the objects of the other list
        over a defined equal key field.
        Example: if the key xid are the same for two objects, check if
        all other attributes are the same.
        """
        keys_this = dict([ (getattr(obj, equalKey), obj) for obj in self])
        keys_other = dict([ (getattr(obj, equalKey), obj) for obj in other])
        #
        print "len(self)", len(keys_this)
        print "len(other)", len(keys_other)
        return 1
    
    
    def dictOfObj(self, *keys):
        """The keys are a tuple, to find one
        do k = x, """
        d1 = {}
        for r in self:
            lst = []
            for key in keys:
                t = getattr(r, key)
                lst.append(t)
            d1.setdefault(tuple(lst), []).append(r)
        return d1
        
    def filterGrid(self, row, col):
        "For data in grid filter for this value and reduce set."
        #obj = self[row]
        new_lst = self.createNewList()

        filterValue = self.get(row, col)
        
        for obj in self.data:
            #print getattr(obj, self.fieldnames[col]), filterValue
            if getattr(obj, self.fieldnames[col])==filterValue:
                new_lst.append(obj)
#            if obj(self.fieldnames[col])==filterValue:
#                new_lst.append(obj)
        return new_lst
        
    def sort(self, col=0):
        lst = []
        if col >= 0:
            lstSort = [getattr(obj, self.fieldnames[col]) for obj in self.data]
            decorated = zip(lstSort, self.data)
            try:
                decorated.sort()
            except TypeError:
                #this is to fix the problem with date error as date cannot compare to None
                tmp_a = []
                tmp_b = []
                for z in decorated:
                    if not z[0]:
                        tmp_a.append(z)
                    else:
                        tmp_b.append(z)
                tmp_b.sort()
                decorated = []
                decorated = tmp_a + tmp_b
            lst = [item for index, item in decorated]
            self.data[:] = lst
        else:
            raise("the index number to sort seems wrong")
        return self
    
    def copyEmpty(self):
        "Returns an empty copy (no data members)."
        newRecordList = copy.deepcopy(self)
        newRecordList.data[:]=[]
        return newRecordList
    
    def createEmptyObject(self):
        "Returns an empty object (copy) from the list members."
        
        obj=Record(self.base_table)
        for xx in self.fieldnames:
            #obj.set(xx, None)
            setattr(obj, xx, None)
        return obj

    def copy(self):
        newRecordList = copy.deepcopy(self)
        return newRecordList
    
    def sqlUpdateGrup(self, table_used, field, new_value, lst_ids):
        """A more efficient way of updating when doing from overseas.
        Uses a list of ids to create one update statement (and not one update per record).
        
        Warning!!:
        Since we can have different tables by setting the base table in a union select
        we must check for this when calling the method.
        """
        sql = "update %s set %s='%s' where id in %s" % (table_used, field, new_value, tuple(lst_ids))
        #print sql
        
        try:
            Db.c.execute(sql)
            Db.cnn.commit()  
        except Exception, e:
            print sql
            print str(e)
            GenericMsgDlg(str(e), 'Other error', wx.OK | wx.ICON_INFORMATION)
            Db.resetConnection()
            return False   
        return sql      
    
    def createNewList(self):
        ret = RecordList()
        ret.fieldnames = copy.deepcopy(self.fieldnames)
        ret.field_types = copy.deepcopy(self.field_types)
        ret.value_field = copy.deepcopy(self.value_field)
        ret.view_id = copy.deepcopy(self.view_id)
        return ret

    def createNewListPivoted(self):
        "Basicaly a version 2 of createNewList"
        raise('I do not think there is a reason to use this method')
        ret = RecordList()
        ret.fieldnames = copy.deepcopy(self.fieldnames_original)
        ret.field_types = copy.deepcopy(self.field_types)
        ret.value_field = copy.deepcopy(self.value_field)
        ret.view_id = copy.deepcopy(self.view_id)
        
        for r in self.data:
            ret.data.append(copy.deepcopy(r))
        
        if self.isPivoted:
            ret = ret.pivot(self.pivot_left, self.pivot_top, self.value_field)
        return ret
                    
    def search(self, searchStr, field=None):

                            
        ret = self.createNewList()
        
#
#        try:
#            a, b = searchStr.split('+')
#            searchStr = '(%s.+%s)|(%s.+%s)' % (a, b, b, a)
#            s = re.compile(searchStr.encode('iso-8859-1'), re.IGNORECASE|re.UNICODE)
#        except:
#            s = re.compile(searchStr.encode('iso-8859-1'), re.IGNORECASE|re.UNICODE)

        try:
            a, b = searchStr.split('+')
            searchStr = '(%s.+%s)|(%s.+%s)' % (a, b, b, a)
            s = re.compile(searchStr, re.IGNORECASE|re.UNICODE)
        except:
            print searchStr
            s = re.compile(searchStr, re.IGNORECASE|re.UNICODE)
                            
        if field is None:

            for obj in self.data:
                strng = ["%s" % val for val in obj.__dict__.values()]
                
                try:
                    strng = ' '.join(strng)
                except UnicodeDecodeError:
                    for val in obj.__dict__.values():
                        strng = ''
                        if type(val)==str:

                            print "UnicodeDecodeError in record:search() ", sys.getdefaultencoding()

                            strng = strng + "%s" % val.decode('utf-8').encode('utf-8')      #.#decode('utf-8', 'replace')   #.encode('utf-8')
                        else:
                            strng = strng + "%s" % val
                        #print strng
                            
                if s.findall(strng):
                    ret.append(obj)

        else:
            for obj in self.data:
                if s.findall(obj.__dict__[field]):
                    ret.append(obj)
           
        return ret
    
    def pop(self, index):
        "reduces the table"
        m = self.fieldnames[index]
        for obj in self.data:
            del obj.__dict__[m]
            
        del self.fieldnames[index]
        del self.field_types[index]
#        ret = self.fieldnames.pop(index)
#        return self

    def popRow(self, rowIndex):
        self.data.pop(rowIndex)
        
    def deleteRange(self, idx_from, idx_to):
        del self.data[idx_from:idx_to]
           
    
    def linkObectList(self, recordList, linkAttrSelf, linkAttrOther):
        """Expands the attributes of the objects in the list with
        the attributes of the objects of the other list.
        
        Example::
        sql = "select * from tbljde_transactions02_plan where (my_type='P_2H_07_v2' and test_period='200707')"
        accr = loadFromDb(sql)
    
        sql = "select * from tblh_people"
        lst = loadFromDb(sql)

        new = accr.linkObectList(lst, 'z_psid', 'peoplesoftid')
    
        new.xls()
        """
        raise ("Likely not used any more, try the GUIDblClick method inherited in record instead.")
        newLst = RecordList()
        newLst.fieldnames = self.fieldnames
        newLst.field_types = self.field_types

        for objSelf in self.data:
            o = objSelf.copy()
            for objOther in recordList:
                if getattr(objSelf, linkAttrSelf)==getattr(objOther,linkAttrOther):
                    #print getattr(objSelf, linkAttrSelf), getattr(objOther,linkAttrOther)
                    for key, val in objOther.__dict__.items():
                        new_attr = 'other_' + key
                        o.set(new_attr, val)

                        if new_attr not in newLst.fieldnames:
                            newLst.fieldnames.append(new_attr)

                    newLst.append(o)
        return newLst
    
    def pivotTime(self, left, top, start, stop, value='count'):
        """To be implemented (I hope).
        pivotTime generates a pivot table from the time series from start to stop
        with the specified time interval. It does not contain the original object
        but generates a series of Piv objects (that references the original).
        The time specified can be day or month.
        Per defualt returns volume when value is set to count.
        """
        
        if not type(start)==datetime.datetime.type:
            raise
        
        class Piv(object):
            def __init__(self, obj):
                self.obj = obj
                self.cnt = 1
                
            def recList(self):
                "returns a list of new objects"
                _t = []
                
            @staticmethod
            def new(self):
                n = Piv()
                return n
            
        #first create new objects to pivot against
        for r in self.data:
            pass
        
        self.pivot(left, top, 'cnt')

    
    def refreshPivot(self):
        """The data is reloaded from the databse and a new lst is produced.
        The new list is pivoted according to the previous definitions."""
        
        lst = loadFromDb(self.sql, self.base_table, self.value_field)
        
        lst.pivot(self.pivot_left, self.pivot_top, self.value_field)
      
        return lst

                        
    def pivot(self, left, top, value=None):
        """you would call pivot with the arguments:
        newList = pivot(['Name',], ['Year',], 'Value')
        """
        self.isPivoted = True
        self.pivot_left = left
        self.pivot_top = top
        self.fieldnames_original = self.fieldnames
        
        if left:
            self.left = left
        if top:
            self.top = top
        if not value:
            if not self.value_field:
                raise("You must set a value field.") 
            value = self.value_field
        else: #value field has been set so remember it ...
            self.value_field = value
            
#        self.copyOfOrg = self.copy() #probably better to get the data again
        
        rs = {}
        self.pvt_dic = {}       #I use same methodology to collect objects 
                        #in a dict of dicts looking like:
                        #{key_tuple_yaxis:key_tuple_xaxis:object_value, ...n}
        ysort = []
        xsort = []
        #self.dic_obj = {}
        
        for row in self.data:
            #yaxis = tuple([row[c] for c in self.left]) changed for alchemy
            yaxis = tuple([getattr(row, c) for c in self.left])
            #print 'yaxis',yaxis
            if yaxis not in ysort: ysort.append(yaxis)
            #xaxis = tuple([row[c] for c in self.top]) changed for alchemy
            xaxis = tuple([getattr(row, c) for c in self.top])
            #print 'xaxis',xaxis
            if xaxis not in xsort: xsort.append(xaxis)
            try:
                rs[yaxis]
                self.pvt_dic[yaxis]
            except KeyError:
                rs[yaxis] = {}
                self.pvt_dic[yaxis] = {}
            if xaxis not in rs[yaxis]:
                rs[yaxis][xaxis] = 0
                self.pvt_dic[yaxis][xaxis] = None
                
            try:
                #print "rs[yaxis][xaxis]", rs[yaxis][xaxis], "value", row[value]
                rs[yaxis][xaxis] += getattr(row, value) #row[value] changed for alchemy
            except TypeError:
                rs[yaxis][xaxis] += 0
            
            if not self.pvt_dic[yaxis][xaxis]:
                newRecordList = RecordList()
                newRecordList.value_field = value
                newRecordList.fieldnames = self.fieldnames
                newRecordList.field_types = self.field_types
                newRecordList.sql = self.sql
                #newRecordList.dicSqlJumps = self.dicSqlJumps
                self.pvt_dic[yaxis][xaxis] = newRecordList
                
            self.pvt_dic[yaxis][xaxis].append(row)

                               
        headings = list(self.left)

        xsort.sort()
        headings.extend(xsort)

        for key in rs:
            if len(rs[key]) < len(xsort):
                for var in xsort:
                    if var not in rs[key].keys():
                        rs[key][var] = ''
                        self.pvt_dic[key][var] = None   
        t = []
        
        ysort.sort() #alex
        
        for left in ysort:
            row = list(left)
            sortedkeys = rs[left].keys()
            sortedkeys.sort()
            sortedvalues = map(rs[left].get, sortedkeys)
            row.extend(sortedvalues)
            t.append(dict(zip(headings,row)))
            #t.append(zip(headings,row))
        #my thing here
        tt_my = []
        ysort.sort() #alex
        for left in ysort:
            row = list(left)
            sortedkeys = self.pvt_dic[left].keys()
            sortedkeys.sort()
            sortedvalues = map(self.pvt_dic[left].get, sortedkeys)
            row.extend(sortedvalues)
            tt_my.append(dict(zip(headings,row)))
        
        #self.pivot_data was now included
        #in refactoring as also self.isPivoted
        self.pivot_data = []            
        #refactored out self.data = []
        #refactored out self.data.append(headings)
        self.pivot_data.append(headings)

        
        for row in t:
            #refactored out self.data.append([row[rec] for rec in headings])
            self.pivot_data.append([row[rec] for rec in headings])

        #now for something new
        #sumation fields:
        #first the rows
#        for key, item in self.pvt_dic.items():
#            suma = 0
#            for inner_item in item.values():
#                if inner_item:
#                    suma += inner_item.pvt_sum()
            #print "This is the sum of the rows", key, suma
            #this could be done aother way
        #then the headers
        dic_head_sum = {}
        for key, item in self.pvt_dic.items():
            for inner_key, inner_item in item.items():
                if dic_head_sum.has_key(inner_key):
                    if inner_item:
                        dic_head_sum[inner_key] = dic_head_sum[inner_key] + inner_item.pvt_sum()
                else:
                    if inner_item:
                        dic_head_sum[inner_key] = inner_item.pvt_sum()
        
        #print "dic_head_sum", dic_head_sum
        #print "len dic_head_sum", len(dic_head_sum)
  
        last_head_sum = []
        for rec in headings:
            try:
                last_head_sum.append(dic_head_sum[rec])
            except:
                str = "Sub total %s" % rec
                last_head_sum.append(str)
        #refactored out self.data.append(last_head_sum)
        self.pivot_data.append(last_head_sum)
        
       # print "last_head_sum", last_head_sum
        ###END
                
        self.pvt_data = []
        self.pvt_data.append(headings)
        self.fieldnames = headings
        
        for row in tt_my:
            self.pvt_data.append([row[rec] for rec in headings])
        
        #here the row sums
        #print "here the row sums"
        #refactored out row = self.data[0]
        row = self.pivot_data[0]
        
        #print row
        row.append('Total')
        #print "self.data[1:]", self.data[1:]
        #refactored out for row in self.data[1:]:
        for row in self.pivot_data[1:]:
            suma = 0
            for entry in row[-len(dic_head_sum):]:      #if the colums
                                                        # have numeric values included these
                try:                                    #will also be added, this is solved here
                    suma+=entry
                except: pass
            row.append(suma)
        
        return self

    def pvt_getNode(self, row, col):
        "in pvt_getNode with row col ", row, col
        newRecordList = RecordList()
        
        try:
            #Here we get the result of one "cell"
            if len(self.pivot_data[:-1]) == row:
                if len(self.pvt_data[row-1])==col:
                    for row in self.pvt_data:
                        for instances in row:
                            if instances.__class__.__name__=='RecordList':
                                newRecordList.value_field = copy.deepcopy(instances.value_field)
                                newRecordList.fieldnames = copy.deepcopy(instances.fieldnames)
                                newRecordList.field_types = copy.deepcopy(instances.field_types)
                                newRecordList.sql = copy.deepcopy(instances.sql)
#                                newRecordList.dicSqlJumps = copy.deepcopy(instances.dicSqlJumps)
                                newRecordList.extend(instances)
                    return newRecordList
                               
            return self.pvt_data[row][col]
        except IndexError:
            #print "Index error was there2", row, col
            #newRecordList = RecordList()

            try:
                #here is the right column result
                if len(self.pvt_data[row])<len(self.pivot_data[row]):
                    #print "here is the right column result"
                   # print "len(self.pvt_data[row])<len(self.data[row])"
                #we have the sumation field in a row
                    for instances in self.pvt_data[row]:
                        if instances.__class__.__name__=='RecordList':
                            newRecordList.value_field = copy.deepcopy(instances.value_field)
                            newRecordList.fieldnames = copy.deepcopy(instances.fieldnames)
                            newRecordList.field_types = copy.deepcopy(instances.field_types)
                            newRecordList.sql = copy.deepcopy(instances.sql)
#                            newRecordList.dicSqlJumps = copy.deepcopy(instances.dicSqlJumps)
                            newRecordList.extend(instances)

            except IndexError:
                if len(self.pvt_data)<len(self.pivot_data):
                    #bottom column result
                    #print "len(self.pvt_data)<len(self.data)"
                    instances = [rec[col] for rec in self.pvt_data]
                    for instances in instances:
                        if instances.__class__.__name__=='RecordList':
                            newRecordList.value_field = copy.deepcopy(instances.value_field)
                            newRecordList.fieldnames = copy.deepcopy(instances.fieldnames)
                            newRecordList.field_types = copy.deepcopy(instances.field_types)
                            newRecordList.sql = copy.deepcopy(instances.sql)
#                            newRecordList.dicSqlJumps = copy.deepcopy(instances.dicSqlJumps)
                            newRecordList.extend(instances) 
            
            return newRecordList
        
    def pvt_sum(self, sumationField=None):
        "helper method creates the sum of a field"
        if sumationField:
            sume = [getattr(val, sumationField) for val in self.data]
            
        else:
            sume = [getattr(val, self.value_field) for val in self.data]

        return sum([r for r in sume if r])

#numeric and statistic section

    def getLen(self):
        return float(self.__len__())
    
    def stat_Sum(self):
        "Returns the sum of the list"
        assert self.value_field, 'The value filed attribute must be set.'
        return float( self.pvt_sum() )
    
    def stat_Mean(self):
        "Returns the mean"
        return (self.stat_Sum() / self.getLen()) 
    
    def stat_StdDevPopulation(self):
        "Returns the standard deviation of an entire population"
        mean = self.stat_Mean()
        tot = 0.0
        for val in self.yieldValues():
            tot += ( val - mean)**2    #the variance
        return (tot/ self.getLen() )**0.5
    
    def stat_StdDevSample(self):
        "Returns the standard deviation of a sample (divide by N-1"
        mean = self.stat_Mean()
        tot = 0.0
        for val in self.yieldValues():
            tot += ( val - mean)**2    #the variance
        return (tot/ (self.getLen()-1.0) )**0.5    
    
    def stat_CV(self):
        """The Coefficient of Variation - the variance relative to the mean
        is the Standard Deviation divided by the Mean
        X: a list of numbers
        returns a float"""
        try:
            return self.stat_StdDevPopulation() / self.stat_Mean()
        except ZeroDivisionError:
            return float('NaN')
        
    def statPrint(self):
        "Print the statistics"
        
        return """Sum:     %f
        Mean:              %f
        St. Dev.:          %f
        Coeff. of Var.:    %f""" % (self.stat_Sum(), self.stat_Mean(), self.stat_StdDevPopulation(), self.stat_CV())
        
    def stat_plotHist(self, bins=10):
        import pylab

        
        pylab.figure(1)
        #pylab.subplot(211)
        n, bins, patches = pylab.hist([r for r in self.yieldValues()], bins=bins)
        y_mean_max = max( n )        
        
        p1, = pylab.plot([self.stat_Mean(),self.stat_Mean()], [0, y_mean_max], '-', color='r', alpha=1.0, label='Mean: %.2f' % self.stat_Mean())
        
        p2, = pylab.plot([( self.stat_Mean() + self.stat_StdDevPopulation() ),( self.stat_Mean() + self.stat_StdDevPopulation() )], 
                   [0, y_mean_max], '--', color='g', alpha=1.0, label=r'Pop. Std. Dev. $\sigma=%.2f$' % self.stat_StdDevPopulation())
        pylab.plot([( self.stat_Mean() - self.stat_StdDevPopulation() ),( self.stat_Mean() - self.stat_StdDevPopulation() )], [0, y_mean_max], '--', color='g', alpha=1.0, label='Std. Dev.')
        
        f = lambda x: x > 0 and x*1.05 or x*0.95 #if the mean is negative we
                                                 #want the line still to appear on the right side
        
        pylab.text(f( self.stat_Mean() ),y_mean_max*0.9, 'Sum: %s' % format( self.stat_Sum(), ',.2f' ), color='g', alpha=1.0)
        pylab.text(f( self.stat_Mean() ),y_mean_max*0.8, 'Mean: %.2f' % self.stat_Mean(), color='r', alpha=1.0)
        
        pylab.text(f( self.stat_Mean() ),y_mean_max*0.7, r'Pop. Std. Dev. $\sigma=%.2f$' % self.stat_StdDevPopulation(), color='g', alpha=1.0)
        pylab.text(f( self.stat_Mean() ),y_mean_max*0.65, r'Sample. Std. Dev. $\sigma=%.2f$' % self.stat_StdDevSample(), color='g', alpha=1.0)
        
        pylab.title('Histogram of %s' % self.value_field)
        
        #format(1234567.89, ',.2f')
        #'{0:,.2f}'.format( self.stat_Sum() )
        pylab.legend( ['Sum: %s' % format( self.stat_Sum(), ',.2f' ), p1.get_label(), p2.get_label() ] )
        
        pylab.figure(2)
        
        pylab.plot( [v for v in self.yieldValues()],'ro' )
        
        pylab.show()
        

    def np_array(self):
        "Returns a numpy array"
        from numpy import array
        return array( [float(getattr(r, self.value_field)) for r in self] )
    
    def np_barChart(self, bar_field):
        from numpy import array
        import numpy as np
        from collections import defaultdict
        from pylab import plt
        
        d = defaultdict(list)
        for r in self:
            d[ getattr(r, bar_field) ].append( float(getattr(r, self.value_field)) ) 
             
        for k,v in d.items():
            d[k] = sum(v)
            
        #return d
        x = np.arange(len(d.keys()))
        y = array(d.values())
        
        plt.bar(x,y)
        
        plt.xticks(x/2., (d.keys()) )
        
        plt.show()
        
    
    def np_testBarPlot(self):
        from pylab import plt
        import numpy as np
        N = 5
        menMeans   = (20, 35, 30, 35, 27)
        womenMeans = (25, 32, 34, 20, 25)
        menStd     = (2, 3, 4, 1, 2)
        womenStd   = (3, 5, 2, 3, 3)
        ind = np.arange(N)    # the x locations for the groups
        width = 0.35       # the width of the bars: can also be len(x) sequence
        
        p1 = plt.bar(ind, menMeans,   width, color='r', yerr=womenStd)
        p2 = plt.bar(ind, womenMeans, width, color='y',
                     bottom=menMeans, yerr=menStd)
        
        plt.ylabel('Scores')
        plt.title('Scores by group and gender')
        plt.xticks(ind+width/2., ('G1', 'G2', 'G3', 'G4', 'G5') )
        plt.yticks(np.arange(0,81,10))
        plt.legend( (p1[0], p2[0]), ('Men', 'Women') )
        
        plt.show()
    
#some wx funcionality
    def GetNumberRows(self):
        if self.isPivoted:
            return len(self.pivot_data)
        else:
            return len(self.data)

    def GetNumberCols(self):
        return len(self.fieldnames)
    
    def WxGetChoiceList(self, field):
        dicUnique = {} #unique values
        for r in self.data:
            print r
            dicUnique[ getattr(r, field)] = 1
        _lst = [k for k in dicUnique.keys() if k]
        print _lst
        _str = ','.join( _lst )
        return ':,'+_str
    
    def WxShowWithApp(self):
        "Quick helper method to show the list from inside the wx_rccl application"
        import wx
        from wx_things.wx_forms import Frm
        app = wx.GetApp()
        frame = Frm(app.mdi_parent_frame, self)
        frame.Show(True)


    def WxShowNoApp(self):
        "Quick helper method to show the list in wx in an independent App."
        import wx
        from wx_things.wx_forms import Frm2

        app = wx.PySimpleApp()
        app.mdi_parent_frame = None

        frame = Frm2(None, self)
        frame.Show(True)
        app.MainLoop() 




def loadFromDb(sql, table_name="<NO_UPDATE_TABLE>", value_filed=None, base_record=Record, base_lst=RecordList):
    """Factory method to load database records into the models.
    sql: sql statement for the records to retrieve
    value_filed: field to be used in pivot and statistics
    base_record: you can override and use an inherited Record
    base_lst: you can override and use an inherited RecordList
    
    You can load directly from an sql statement and have this mapped
    to a default record object or supply your customized object to be loaded.
    In the future I hope you can also decide you would like to load
    SQLAlchemy objects (but Alchemy is a killer in speed).
    
    Returns a recordset from an sql statement.
    
    Example sql::
    >>> WhichDb_v3('Postgres', None)
    >>> sql = "select * from tbb_period where year=2007"
    >>> lst = loadFromDb(sql)
    >>> print len(lst)
    12
    """
    lst=base_lst()
    lst.value_field = value_filed
    lst.base_table = table_name
    #lst.sql = sql
    try:
          
        Db.c.execute(str(sql))
          
    except Exception, e:
              
            print sql
            print 'SQL error message: %s' % str(e)
              
            GenericMsgDlg(str(e), 'SQL error', wx.OK | wx.ICON_INFORMATION)
            Db.resetConnection()
            return False
#    Db.c.execute(str(sql))

    lst.fieldnames = Db.fields()
    lst.field_types = Db.fieldTypes()
    lst.sql = sql

    for rec in Db.c.fetchall():
        obj=base_record(table_name)
        #refactor out parent
        #obj.parent = lst
        last_zip = zip(Db.fields(), rec)
        for xx in last_zip:
            setattr(obj, xx[0], xx[1])
        lst.append(obj)

    return lst




def loadFromAlchemy(query, base_record):
    """Loads an sql alchemy query object."""
    lst=RecordList()
    lst.value_field = None
    lst.base_table = base_record.__table__

    lst.fieldnames = base_record.fieldnames #must be overridden
    lst.field_types = None
    lst.sql = base_record #'cannot be used as error is raised in pivot get node copy method' #query.statement

    for rec in query.all():
        lst.append(rec)

    return lst   


def loadFromFile(file, sheet='Sheet1', basetable='No db table - xls'):
    from ahutils.excel import easyExcel
    lst=RecordList()
#    lst.value_field = value_filed
    lst.base_table = basetable

    xls = easyExcel(file)

    sht = xls.getContiguousRange(sheet)

#    print sht
#    for r in sht:
#        print r
    lst.fieldnames = [str(r) for r in sht[0]]
#    print lst.fieldnames

    for rec in sht[1:]:
        obj=Record(basetable)
        last_zip = zip(lst.fieldnames, rec)
        
        for xx in last_zip:
            setattr(obj, xx[0], xx[1])
        lst.append(obj)

    return lst    

def loadFromFileCsv(file, basetable='No db table - csv'):
    import csv
    reader = csv.reader(open(file, "rb"))
    lst=RecordList()
    lst.base_table = basetable

    i = 0
    for row in reader:
        if i == 0:
            #the first row
            i=1
            lst.fieldnames = row
        else:
            obj=Record(lst.base_table)
            last_zip = zip(lst.fieldnames, row)

            for xx in last_zip:
                setattr(obj, xx[0], xx[1])
            lst.append(obj)
    return lst

def setDbConst():
    #Db=WhichDb_v3('Postgress', 'lse_fin_db', const.gui_user, const.gui_pwd)
    Db=WhichDb_v3('Postgress', 'lse_fin_db', const.gui_user, const.gui_pwd)
    
def insertIntoUserView(viewid, username='ahetland'):
    sql = """insert into tbl_users_view ("user", view_id) values ('%s', %d)""" % (username, viewid)
    Db.c.execute(sql)
    Db.cnn.commit()
    return True  



def showExample():
    import wx
    from wx_piv_ap.wx_forms import Frm2
    import datetime 
    
    class CustomClas(Record):
        def __init__(self, base_table):
            Record.__init__(self, 'x')
            
            
        def getYear(self):
            return self._start[0:4]
        year = property(getYear)
        
        def getCnt(self):
            return 1
        cnt = property(getCnt)
        
     
    
    app = wx.PySimpleApp()
    app.mdi_parent_frame = None
    t_1 = datetime.datetime.now()
    lst = loadFromDb("""select * from tbl_users""", 'xxx', None) 
    #lst.fieldnames.append('year')
    
    #lst.pivot(['year',], ['year',], 'cnt')
    
#     lst.value_field = 'amount'
#     lst.stat_plotHist()
    
    t_2 = datetime.datetime.now()
    
    print t_2 - t_1
    frame = Frm2(None, lst)
    frame.Show(True)
    app.MainLoop() 
    
    

def run():
    "Run the main program from here."
    from wx_piv_app import main
    main(None)
    
    
if __name__=='__main__':
    

#     setDbConst()
# 
#     showExample()
    run()
#    developCSVCapability()

