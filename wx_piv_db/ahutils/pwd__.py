#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


def pwd(windowsUser):
    """Returns the compiled password if the user name matches the windows log-inn."""
    if windowsUser==os.environ.get( "USERNAME" ):
        return 'your password'
    else:
        return None

def createFile():
    "Compiple the file. Rename the file first though!!!"
    import py_compile
    py_compile.compile('pwd.py')
     
if __name__=='__main__':
    createFile()
    pass