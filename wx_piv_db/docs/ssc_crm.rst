CRM
===
The CRM module assists in the reporting of CRM data.


Usage
-----
The CRM data is down loaded from CRM and inserted into the database. The data is first flattened so that one can more easily create reports. 
The data flattening is done by making a copy of the CRM record and creating new records for every year and amount in the fields amount1-amount3
and deliverydate1-3. By every import new records are added (manual delete is necessary if one does not need the history), so old records are
marked as "Old" and new as "Current"  

.. literalinclude:: ..//ssc_crm//db//crm.py