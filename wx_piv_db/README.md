wx_piv_db
=========

Pivot tables and views in a database

To the Docs
-----------
http://htmlpreview.github.io/?https://github.com/ahetland/wx_piv_db/blob/master/wx_piv_db/docs/_build/html/index.html


Installing from scratch
-----------------------
For windows install the following files using respective the installers. 

+ Get the Python 2.7 version from and install (select 64 version if applicable) http://python.org/downloads/

+ win32All (for Windows COM support) http://sourceforge.net/projects/pywin32/files/ (find the last applicable installer example: pywin32-218.win-amd64-py2.7.exe)

+ wxPython (the GUI) http://www.wxpython.org/download.php#msw

+ psycopg (to connect to database) http://www.stickpeople.com/projects/python/win-psycopg/

+ NumPy (numerical engine) http://sourceforge.net/projects/numpy/files/NumPy/

+ NumPy (numerical engine 64 bit) http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

+ MxDateTime  http://www.egenix.com/products/python/mxBase/ scroll down to select the msi installer

+ matplotlib (drawing and plotting) http://matplotlib.org/downloads.html

Setting up easy_install

+ Install https://pypi.python.org/pypi/setuptools#windows by issuing command 

python ez_setup.py

After you have easy_install installed you can install dateutil by issuing the comand (in cmd.exe)

install pyparsing

C:\Python27\Scripts\easy_install python-dateutil

You should now be able to find all installed software in site-packages

Installing the ODBC driver
--------------------------

We have postgres version 9.1 installed so take this one http://www.postgresql.org/ftp/odbc/versions/msi/
scroll down to bottom of page and install. When installed open the options and un-click "declare fetch"

You should install the 32 bit version even if we are running on 64 machines, this is because we have windows 32 on
our machines. Then you should go and call the odbc manager from the C:\Windows\SysWOW64 folder odbcad32.exe

see also http://stackoverflow.com/questions/6796252/setting-up-postgresql-odbc-on-windows

Initiating a database
---------------------
There is a script in ahutils folder to setup an empty database with example data. To use this first
install postgres and create an empty database with the following parameters:

CREATE DATABASE new_db2
  WITH OWNER = postgres
    ENCODING = 'UTF8'
    TABLESPACE = pg_default
    TEMPLATE = postgres;
    
Go to the config folder and adjust the const.host='localhost' and const.db_lst_dsn='the db' parameters
run db_setup.py

The script will create the needed tables and an example table, enter some data and then open the GUI. You can now start using the database.

Useful Tools
------------
In addition to Python and Postgres I use and have found following tools to be very useful:
Eclipse with the PyDev plugin
Access and Excel via the ODBC driver
EMS Database Manager (I use the freeware light version)
 
test
