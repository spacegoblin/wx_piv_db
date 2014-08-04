Expense report tool
===================
A web tool to assist in the expense reporting.


Background and working concept
------------------------------
The general idea is to create a tool that can be used for expense and travel reporting. The working
model will be a tool that can be used on the local server at AF (Argelsrieder Feld), but also on a company server. 
The local AF version will then be able to read excel expense reports and process them from there. In the company
sever version one can create ones expense report without using excel (the expense report will be an additional 
product).



Tools used
----------
Pyramid web stack as detailed from the documentation on 
http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/project.html#project-narr

To run
-------

cd C:\Users\hetland\Documents\Development\repository\wx_piv_db\wx_piv_db\webapp\ExpReport
C:\Python27\Scripts\pserve development.ini

Added Waitress
Added paste
run C:\Python27\python setup.py develop
