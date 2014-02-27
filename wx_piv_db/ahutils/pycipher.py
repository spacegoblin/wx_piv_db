r"""
An implementation of several well-known classical cipher algorithms.

Encipher and decipher the message "Attack at dawn." with "King" as the key using
the Vigenere cipher:

  >>> from pycipher import *
  >>> plaintext = 'Attack at dawn.'
  >>> key = 'King'
  >>> ciphertext = Vigenere(plaintext).encipher(key)
  >>> ciphertext
  'Kbggms nz nijt.'
  >>> Vigenere(ciphertext).decipher(key)
  'Attack at dawn.'

Note:

  1. Non-alphabetic input (e.g. " " and "." above) is left as-is.
  2. The input (plaintext/ciphertext) case is preserved through output
     (ciphertext/plaintext).

The case of the key doesn't matter, as the case of each of its character is made
to conform with the corresponding character in the input (plaintext/ciphertext).

  >>> Vigenere(plaintext).encipher('king') ==\
  ... Vigenere(plaintext).encipher('KING') ==\
  ... Vigenere(plaintext).encipher('KiNg')
  True
  >>> Vigenere(ciphertext).decipher('kInG') ==\
  ... Vigenere(ciphertext).decipher('KIng') ==\
  ... Vigenere(ciphertext).decipher('kiNG')
  True

Both the encipher() and decipher() methods return a cipher object of the same
type of the one they belong to. This makes things like the following possible:

  >>> Vigenere(plaintext).encipher(key).decipher(key)
  'Attack at dawn.'
  >>> Caesar(plaintext).encipher(3).decipher(2).decipher(1)
  'Attack at dawn.'

Since each cipher is a subclass of the str built-in class, any cipher object can
be treated as a string. For instance:

  >>> Vigenere(plaintext)[:-1].replace(' ', '').lower()
  'attackatdawn'
"""

__name__ = 'PyCipher'
__version__ = '0.2' # history available at the end of this file
__date__ = 'Sat, 15 Oct 2005'
__author__ = 'Aggelos Orfanakos <csst0266atcsdotuoidotgr>'
__url__ = 'http://pycipher.sourceforge.net/'

#===============================================================================
# History
# -------
#
# Sat, 15 Oct 2005 0.2
#
#     * Added support for the Vernam (a.k.a. one-time pad) cipher.
#     * All ciphers now accept non-alphabetic input and leave it as-is.
#
# Fri, 23 Sep 2005 0.1
#
#     * Initial release.
#
# License
# -------
#
# Copyright (c) 2005, Aggelos Orfanakos <csst0266atcsdotuoidotgr>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
#===============================================================================

class Atbash(str):

    """An implementation of the Atbash cipher."""

    def encipher(self):
        """Encipher input (plaintext) using the Atbash cipher and return it (ciphertext)."""
        ciphertext = []

        for p in self:
            if p.isalpha():
                ciphertext.append(chr(ord('Aa'[int(p.islower())]) + ord('Zz'[int(p.islower())]) - ord(p)))
            else:
                ciphertext.append(p)

        return Atbash(''.join(ciphertext))

    def decipher(self):
        """Decipher input (ciphertext) using the Atbash cipher and return it (plaintext)."""
        return self.encipher()

class Autokey(str):

    """An implementation of the Autokey cipher."""

    def encipher(self, key):
        """Encipher input (plaintext) using the Autokey cipher and return it (ciphertext)."""
        ciphertext = []
        k = 0
        n = len(key)

        for i in range(len(self)):
            p = self[i]

            if p.isalpha():
                ciphertext.append(chr((ord(p) + ord((key[k % n].upper(), key[k % n].lower())[int(p.islower())]) - 2 * ord('Aa'[int(p.islower())])) % 26 + ord('Aa'[int(p.islower())])))
                k += 1
            else:
                ciphertext.append(p)

            if k == n:
                j = i
                key = []

                while k > 0:
                    p = self[j]

                    if p.isalpha():
                        key.insert(0, p)
                        k -= 1

                    j -= 1

                key = ''.join(key)

        return Autokey(''.join(ciphertext))

    def decipher(self, key):
        """Decipher input (ciphertext) using the Autokey cipher and return it (plaintext)."""
        plaintext = []
        k = 0
        n = len(key)

        for i in range(len(self)):
            c = self[i]

            if c.isalpha():
                plaintext.append(chr((ord(c) - ord((key[k % n].upper(), key[k % n].lower())[int(c.islower())])) % 26 + ord('Aa'[int(c.islower())])))
                k += 1
            else:
                plaintext.append(c)

            if k == n:
                j = i
                key = []

                while k > 0:
                    p = plaintext[j]

                    if p.isalpha():
                        key.insert(0, p)
                        k -= 1

                    j -= 1

                key = ''.join(key)

        return Autokey(''.join(plaintext))

class Beaufort(str):

    """An implementation of the Beaufort cipher."""

    def encipher(self, key):
        """Encipher input (plaintext) using the Beaufort cipher and return it (ciphertext)."""
        ciphertext = []
        k = 0
        n = len(key)

        for i in range(len(self)):
            p = self[i]

            if p.isalpha():
                ciphertext.append(chr((ord((key[k % n].upper(), key[k % n].lower())[int(p.islower())]) - ord(p)) % 26 + ord('Aa'[int(p.islower())])))
                k += 1
            else:
                ciphertext.append(p)

        return Beaufort(''.join(ciphertext))

    def decipher(self, key):
        """Decipher input (ciphertext) using the Beaufort cipher and return it (plaintext)."""
        return self.encipher(key)

class Caesar(str):

    """An implementation of the Caesar cipher."""

    def encipher(self, shift):
        """Encipher input (plaintext) using the Caesar cipher and return it (ciphertext)."""
        ciphertext = []

        for p in self:
            if p.isalpha():
                ciphertext.append(chr((ord(p) - ord('Aa'[int(p.islower())]) + shift) % 26 + ord('Aa'[int(p.islower())])))
            else:
                ciphertext.append(p)

        return Caesar(''.join(ciphertext))

    def decipher(self, shift):
        """Decipher input (ciphertext) using the Caesar cipher and return it (plaintext)."""
        return self.encipher(-shift)

class Vigenere(str):

    """An implementation of the Vigenere cipher."""

    def encipher(self, key):
        """Encipher input (plaintext) using the Vigenere cipher and return it (ciphertext)."""
        ciphertext = []
        k = 0
        n = len(key)

        for i in range(len(self)):
            p = self[i]

            if p.isalpha():
                ciphertext.append(chr((ord(p) + ord((key[k % n].upper(), key[k % n].lower())[int(p.islower())]) - 2 * ord('Aa'[int(p.islower())])) % 26 + ord('Aa'[int(p.islower())])))
                k += 1
            else:
                ciphertext.append(p)

        return Vigenere(''.join(ciphertext))

    def decipher(self, key):
        """Decipher input (ciphertext) using the Vigenere cipher and return it (plaintext)."""
        plaintext = []
        k = 0
        n = len(key)

        for i in range(len(self)):
            c = self[i]

            if c.isalpha():
                plaintext.append(chr((ord(c) - ord((key[k % n].upper(), key[k % n].lower())[int(c.islower())])) % 26 + ord('Aa'[int(c.islower())])))
                k += 1
            else:
                plaintext.append(c)

        return Vigenere(''.join(plaintext))

class Vernam(Vigenere):

    """
    An implementation of the Vernam (a.k.a. one-time pad) cipher.

    Note: The Vernam cipher is, in fact, Vigenere with a truly random key of length
          equal to that of the input (plaintext/ciphertext).
    """

    def encipher(self, key):
        """
        Encipher input (plaintext) using the Vernam (a.k.a. one-time pad) cipher and
        return it (ciphertext).
        """
        return Vernam(Vigenere.encipher(self, key))

    def decipher(self, key):
        """
        Decipher input (ciphertext) using the Vernam (a.k.a. one-time pad) cipher and
        return it (plaintext).
        """
        return Vernam(Vigenere.decipher(self, key))

