#!/usr/bin/python
# -*- coding: utf-8 -*-

#===============================================================================
# This module will check for your windows login name
# if it is the user you specify it will return the password you hard coded into 
# this file.
# To prevent anyone from reading the file you run the file to compile the file
# and it can no longer be read. 
#===============================================================================
import os


def pwd(windowsUser):
    """Returns the compiled password if the user name matches the windows log-inn."""
    if windowsUser==os.environ.get( "USERNAME" ):
        return 'sdfjhio8974sadyxc'
    else:
        return None

def createFile():
    "Compiple the file. Rename the file first though!!!"
    import py_compile
    py_compile.compile('pwd.py')
     
if __name__=='__main__':
    createFile()
    pass