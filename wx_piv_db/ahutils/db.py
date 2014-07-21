#import decimal #imported this to make pyodbc with py2exe work
#import pyodbc
import psycopg2
from psycopg2.extensions import QuotedString
import datetime
from string import join, replace
import decimal

import sys
if '..//' not in sys.path:
    sys.path.append('..//')
    
#import sqlite3
#import xconfig
from ahconfig import const

class DbBase(object):
        
    def resetConnection(self):
        raise Exception, "This method must be overridden!"      
        
    def close(self):
        self.cnn.close()
        
    def commit(self):
        self.cnn.commit()
        
    def fields(self):
        raise Exception, "This method must be overridden!"

    def fieldTypes(self):
        raise Exception, "This method must be overridden!"
            
    def __del__(self):
        if self.cnn:
            self.close()
            

class This_Db(DbBase):
    
    def __init__(self, dbname, user, pwd):
        """This is an example of unit test::
            >>> db=Rcl_Db()
            >>> 
        """
        super(This_Db, self)
        self.__user = user
        self.__pwd = pwd
        try:
            #if it has been set donot try to reset
            const.dbname = dbname
        except: pass

        self.cnn = None                         
        self.cnn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % 
                                   (const.host, dbname, 
                                    user, pwd))
        self.c = self.cnn.cursor()
        self.db_name = 'no name set'
        
    def resetConnection(self):
        "When the db thorws back an error this needs to be reset."
        self.cnn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % 
                                   (const.host, const.dbname, 
                                    self.__user, self.__pwd))
        self.c = self.cnn.cursor()        
        
    def fields(self):
        return [r[0]for r in self.c.description]

    def fieldTypes(self):
        #print [type(r[1]) for r in self.c.description], "Field Types"
        def check(typus):
            if typus==23:
                return 'INTEGER'
            elif typus==1043:
                return 'VARCHAR'
            elif typus==25:
                return 'TEXT'
            elif typus==1700:
                return 'NUMERIC'
            elif typus==1082:
                return 'DATE'
            elif typus==701:
                return 'DOUBLE'
            else:
                return 'NOT DEFINED'
        #print  [r for r in self.c.description]
        return [check(r[1]) for r in self.c.description]
        
# from sqlalchemy.sql import text
# from sqlalchemy import create_engine, MetaData

class Sqlite(DbBase):
    
    
    
    def __init__(self,dbname, user, pwd):
        super(Sqlite, self)

        self.__user = user
        self.__pwd = pwd
        
        
        db = 'sqlite:////home/alex/workspace/test_01.db'
        
        engine = create_engine(db, echo=True)
        metadata = MetaData()
        #metadata.create_all(engine) 
        
        self.cnn = None                         
        self.cnn = engine.connect()
        print "sqlite conn", self.cnn
        #self.c = self.cnn.cursor()
        self.db_name = 'no name set'
        
    #def resetConnection(self): pass
    def selectSQL(self, sqlText):
        
        sql = text(sqlText)
        
        return self.cnn.execute(sql)
        
def quote(string): raise Exception, ("must be overridden")


def _quoteAccess(string):
    """To set the quote for Access
    """
    
    if string:
        #print string
        try:
            return string.replace("'", "''")
        except:
            #print "Exception string", string, type(string)
            return string
    else:
        return string

def _quotePostgress(string):
    """To set the quote for Postgress
    """
    if string:
        return string.replace("'", "\\'")
    else:
        return string
    
def _quoteNone(string):
    """If _quotePostgress is not needed, if client and db is utf-8
    """

    if string:
        return string.replace("'", "''")
    else:
        return string
            
def setQuote(Driver):
    if Driver=='Access':
        globals()['quote'] = _quoteAccess
        
        
    elif Driver=='PostgreSQL':
        globals()['quote'] = _quoteNone
        
    elif Driver=='Postgress':
        globals()['quote'] = _quoteNone
        
    elif Driver=='sqlite':
        globals()['quote'] = _quoteAccess
        
    else: raise("Quotation not set for database")
    print "Database quotation set to ", globals()['quote']
        
def dictToInsert(dict, tablename):
    "USE the one in UTILS returns an INSERT statement"
    db_keys = []
    db_values = []
    for (key, value) in dict.items():
        typ = type(value)
        if value == None:
            continue
        elif value == '':
            continue 
        elif typ == unicode:
            db_values.append("'%s'" % quote (value.encode('utf-8')))
        elif typ == datetime.date:
            db_values.append("'" + value.strftime('%Y-%m-%d') + "'")
        elif typ == datetime.datetime:
            db_values.append("'" + value.strftime('%Y-%m-%d') + "'") 
        elif typ == int:
            db_values.append(repr(value))
        elif typ == float:
            db_values.append(repr(value))
        elif typ == bool:
            db_values.append(repr(value))
        elif typ == decimal.Decimal:
            db_values.append(repr(float(value)))
        else:
            #db_values.append(repr(value))
            #trying something new
            #db_values.append(quote (repr(value)) )
            s = quote(value)    #do the escapes for db insert
            s = "'" + s + "'"   #add apostrophes for sql statement
            db_values.append(s)
        db_keys.append(key)

    stmt = 'INSERT INTO %s (%s) VALUES (%s);' % (
                    tablename,
                    join(db_keys, ','),
                    join(db_values, ',')
                    )

    return stmt

def dictToUpdate(dict, tablename, **upd_id):
    "returns an UPDATE statement"
    #print upd_id.keys()[0], upd_id.values()[0]
    
    db_keys = []
    db_values = []
    lstStr = []
    for (key, value) in dict.items():
        if type(key)==unicode:
            key = key.encode('ascii')
        typ = type(value)

        if value == None:
            continue       
        elif typ == list:
            continue
        elif typ == unicode:
            #print "Test for unicode"

            db_values.append("""'%s'""" % quote (value.encode('utf-8')))
        elif typ == datetime.date:
            db_values.append("'" + value.strftime('%Y-%m-%d') + "'")
        elif typ == datetime.datetime:
            db_values.append("'" + value.strftime('%Y-%m-%d') + "'")            
        elif typ == int:
            db_values.append(repr(value))
        elif typ == float:
            db_values.append(repr(value))
        elif typ == bool:
            db_values.append(repr(value))
        else:
            s = quote(value)    #do the escapes for db insert
            s = "'" + s + "'"   #add apostrophes for sql statement
            db_values.append(s)            

        db_keys.append(key)
    
    for i in range(len(db_keys)):

        lstStr.append((db_keys[i] + '=' + db_values[i]))
        i+=1
          
    str = lstStr[0]
    for x in lstStr[1:]:
        str = str +', '+ x
        
    stmt = "UPDATE %s SET %s where %s=%s;" % (
                    tablename,
                    str, upd_id.keys()[0], upd_id.values()[0])
    return stmt

def insertBlobSql(fname, pathWithFileName, object_id, base_table):
    import base64
    print "pathWithFileName", pathWithFileName
    file = open(pathWithFileName, 'rb').read()

    file = file.strip()

    sql = """insert into tbl_meta (filename, parent_id, base_table, blob) 
    values ('%s', %d, '%s', %s)""" \
                % (fname, object_id, base_table, 
                   QuotedString (base64.b64encode(file))) 
    return sql


def initPostgres(db_name, usr, pwd):
    setQuote('Postgress')
    globals()['Db'] = This_Db(db_name, usr, pwd)
    return globals()['Db']


    
def test():
    print "test" 
    
    Db = Sqlite('test_01', 'ahetland', 123)
    
    from sqlalchemy.sql import text
    
    sql="""select * from tbl_views 
        inner join tbl_users_view on tbl_views.id = tbl_users_view.view_id 
        where tbl_users_view.user='ahetland' order by tbl_views.sorted"""
        
    for r in Db.selectSQL(sql).all():
        print r
             
if __name__=='__main__':
    
    test()

    
    