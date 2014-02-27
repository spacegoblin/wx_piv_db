import string
from random import Random
from pycipher import Vigenere
#from period import Period
from datetime import datetime

def dateConvUS(str):
    "Converts a string of format american date format m/d/y"
    try:
        return datetime.strptime(str, '%m/%d/%y').strftime('%Y-%m-%d')
    except: return None
    
def dateConvEUR(str):
    "Converts a string of format European date format d/m/y"
    try:
        return datetime.strptime(str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except: return None
        
def randomString(strlength=6):
    "Generates a random string of length strlength"
    d = datetime.now()
    dd = d.strftime('%y%m%d')
    return dd+''.join( Random().sample(string.letters+string.digits, strlength) )

def encrypt(str, key='rccl'):
    return Vigenere(str).encipher(key)

def decrypt(str, key):
    return Vigenere(str).decipher(key)

def periodIter(start, stop):
    per = Period(start)
    return per.__iter__(stop)
    
    
#------------------------------------------------------------------------------ 
#pycipher.py demo
#from pycipher import Vigenere
#plaintext = 'Attack at dawn.'
#key = 'King'
#ciphertext = Vigenere(plaintext).encipher(key)
#print ciphertext
#print Vigenere(ciphertext).decipher(key)

def countDict(d, f, c):
    """Returns the dictionary of the form
    d['python']['good'] = 4
    """
    d = d
    assert type ( d ) == dict
    def incr(f, c):
        d.setdefault(f,{})
        d[f].setdefault(c, 0)
        d[f][c]+=1
        return d
    return incr(f, c)

if __name__=='__main__':
#    print randomString()
#    x = encrypt('tacobelle', 'rccl')
#    print x
    print decrypt('kcezckzpivc', 'rccl')
    
    t={}
    countDict(t, 'python', 'good')
    print t
    print t['python']['good']
    countDict(t, 'python', 'good')
    print t
