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
        return 'sz'
    else:
        return None

def createFile():
    "Compiple the file. Rename the file first though!!!"
    import py_compile
    py_compile.compile('pwd.py')



import uuid
import hashlib
 
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def test():
    new_pass = raw_input('Please enter a password: ')
    hashed_password = hash_password(new_pass)
    print('The string to store in the db is: ' + hashed_password)
    old_pass = raw_input('Now please enter the password again to check: ')
    if check_password(hashed_password, old_pass):
        print('You entered the right password')
    else:
        print('I am sorry but the password does not match')
    
  
if __name__=='__main__':
    #createFile()
    test()