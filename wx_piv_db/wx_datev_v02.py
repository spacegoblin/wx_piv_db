#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
print wx.version() 

import wx.dataview as dv

from wx_forms import CtrWCloseUtil

class DatevPanel(wx.Panel):
    def __init__(self, parent, obj):
        
        self.parent = parent 
        wx.Panel.__init__(self, parent, -1)
        
        self.obj = obj
        self.create()
        
        
        
    def create(self):
        """initialise the panel"""
        
        TXT_SIZE_HIGH = 20
        TXT_SIZE_LNGTH = 250
        fontSmall = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, encoding=wx.FONTENCODING_ISO8859_1)
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, encoding=wx.FONTENCODING_ISO8859_1)
        fontBold = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        ###
        box_1 = wx.StaticBox(self, -1, "Account entry")
        bsizer_1 = wx.StaticBoxSizer(box_1, wx.VERTICAL)
        
        
        finstatem_txt = wx.StaticText(self, -1, '%s - %s' % (self.obj.fin_statement, self.obj.hgb_acc_sort_code), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH))
        finstatem_txt.SetFont(font)
        
        datev_txt = wx.StaticText(self, -1, '%s - %s' % (self.obj.account_datev, self.obj.name_datev), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH*2))
        datev_txt.SetFont(fontBold)
        
        amount_txt = wx.StaticText(self, -1, "Amount: {:,.2f}".format(self.obj.amount), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH))
        amount_txt.SetFont(fontBold)
        
        
        
        period_txt = wx.StaticText(self, -1, "Period: %d" % self.obj.period, size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH))
        period_txt.SetFont(fontBold)
 
        #print lambda (yy): "%s" % self.obj.costcenter.project_code if (self.obj.costcenter.project_code) else 'lambda worked'
        #print self.obj
        cc_txt_1 = wx.StaticText(self, -1, 'Project code:\n%s' % (self.obj.project_code), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH*2))
        cc_txt_1.SetFont(fontBold)
        
        buchungstext_1 = wx.StaticText(self, -1, 'Buchungstext:\n%s' % (self.obj.buchungstext), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH*3))
        
        ggkonto_1 = wx.StaticText(self, -1, 'Gegenkonto: %s' % (self.obj.gegenkonto), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH))
                
        bsizer_1.Add(finstatem_txt, 0, wx.TOP|wx.LEFT, 0)
        bsizer_1.AddSpacer(10,10)
        
        bsizer_1.Add(datev_txt, 0, wx.TOP|wx.LEFT, 0)
        
        bsizer_1.Add(period_txt, 0, wx.TOP|wx.LEFT, 0)
        bsizer_1.Add(amount_txt, 0, wx.TOP|wx.LEFT, 0)

        bsizer_1.AddSpacer(10,10)
        
        bsizer_1.Add(cc_txt_1, 0, wx.TOP|wx.LEFT, 0)
        bsizer_1.Add(buchungstext_1, 0, wx.TOP|wx.LEFT, 0)
        bsizer_1.Add(ggkonto_1, 0, wx.TOP|wx.LEFT, 0)
        

        ###
        box_2 = wx.StaticBox(self, -1, "Account other details")
        bsizer_2 = wx.StaticBoxSizer(box_2, wx.VERTICAL)
        
        #buchungstext_2 = wx.StaticText(self, -1, 'Buchungstext:\n%s' % (self.obj.buchungstext), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH*2))
        
        company_txt = wx.StaticText(self, -1, 'Company: %s' % (self.obj.company), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH))
        
        ssc_txt = wx.StaticText(self, -1, 'SSC: %s - %s' % (self.obj.account.accounts_ssc, self.obj.account.acc_description_ssc), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH*2))
        
        if self.obj.costcenter:
            cc_txt = wx.TextCtrl(self, -1, 'Cost/project code:\n%s %s\n%s' % (self.obj.costcenter.project_code, self.obj.costcenter.costcenternr,
                                                                            self.obj.costcenter.description), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH*3), style=wx.TE_MULTILINE|wx.TE_READONLY)
            cc_txt.SetFont(fontSmall)
            cc_txt.SetBackgroundColour('Light-Grey')
        
        
        
        datum_txt = wx.StaticText(self, -1, 'Date: %s' % (self.obj.datum), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH))
        stapel_txt = wx.StaticText(self, -1, 'Stapel nr.: %s' % (self.obj.stapel_nr), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH))
        beleg_txt = wx.StaticText(self, -1, 'Belegfeld: %s' % (self.obj.belegfeld1), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH))
        
       # bsizer_2.Add(buchungstext_2, 0, wx.TOP|wx.LEFT, 0)

        bsizer_2.Add(company_txt, 0, wx.TOP|wx.LEFT, 0)
        bsizer_2.Add(ssc_txt, 0, wx.TOP|wx.LEFT, 0)
        if self.obj.costcenter:
            bsizer_2.Add(cc_txt, 0, wx.TOP|wx.LEFT, 0)
        #bsizer_2.Add(cc_descr_txt, 0, wx.TOP|wx.LEFT, 0)
        bsizer_2.Add(datum_txt, 0, wx.TOP|wx.LEFT, 0)
        bsizer_2.Add(stapel_txt, 0, wx.TOP|wx.LEFT, 0)
        bsizer_2.Add(beleg_txt, 0, wx.TOP|wx.LEFT, 0)
                
        ###
        box_3 = wx.StaticBox(self, -1, "Added comments")
        bsizer_3 = wx.StaticBoxSizer(box_3, wx.VERTICAL)
        
#         buchungstext_3 = wx.StaticText(self, -1, 'Buchungstext:\n%s' % (self.obj.buchungstext), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH*2))
#         bsizer_3.Add(buchungstext_3, 0, wx.TOP|wx.LEFT, 0)

        comment_3 = wx.TextCtrl(self, -1, unicode( self.obj.comment ), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH*2) ,style=wx.EXPAND|wx.TE_MULTILINE)
        bsizer_3.Add(comment_3, 0, wx.TOP|wx.LEFT, 0)   

        comment_3_2 = wx.TextCtrl(self, -1, unicode( self.obj.comment_2 ), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH*2) ,style=wx.EXPAND|wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        bsizer_3.Add(comment_3_2, 0, wx.TOP|wx.LEFT, 0)   
        
#        bsizer_3.AddSpacer(10)


        ###
        box_4 = wx.StaticBox(self, -1, "Person data")
        bsizer_4 = wx.StaticBoxSizer(box_4, wx.VERTICAL)
        if self.obj.full_name:
            pcode_4 = wx.StaticText(self, -1, '%s - %s' % (self.obj.person.code, self.obj.full_name), size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH))
            buchungstext_4 = wx.StaticText(self, -1, 'Standard cost data:', size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH*2))
            
            dvlc = dv.DataViewListCtrl(self)
            dvlc.AppendTextColumn('account', width=70)
            dvlc.AppendTextColumn('project_code', width=100)            
            dvlc.AppendTextColumn('amount', width=70)
            
            #for itemvalues in musicdata:
            from dbtable.person import PersonStdCost
            qry = self.obj.session.query(PersonStdCost).filter(PersonStdCost.code==unicode(self.obj.pers_code))
            
            for x in qry:
                l = list((x.datev_full, x.project_code, "{:,.2f}".format(x.amount)))
     
                dvlc.AppendItem(l)

            
            bsizer_4.Add(pcode_4, 0, wx.TOP|wx.LEFT, 0)
            bsizer_4.Add(buchungstext_4, 0, wx.TOP|wx.LEFT, 0)
            bsizer_4.Add(dvlc, 1, wx.EXPAND)
            
        else:
            txt_na = wx.StaticText(self, -1, 'n.a', size=(TXT_SIZE_LNGTH, TXT_SIZE_HIGH*2))
            bsizer_4.Add(txt_na, 0, wx.TOP|wx.LEFT, 0)

                  
        ###

                
        border = wx.BoxSizer(wx.VERTICAL)
        
        inner_horizont_1 = wx.BoxSizer(wx.HORIZONTAL)
        inner_horizont_1.Add(bsizer_1, 1, wx.EXPAND|wx.ALL, 15)
        inner_horizont_1.Add(bsizer_2, 1, wx.EXPAND|wx.ALL, 15)
        
        inner_horizont_2 = wx.BoxSizer(wx.HORIZONTAL)
        inner_horizont_2.Add(bsizer_3, 1, wx.EXPAND|wx.ALL, 15)
        

        inner_horizont_2.Add(bsizer_4, 1, wx.EXPAND|wx.ALL, 15)
        
        border.Add(inner_horizont_1, 1, wx.EXPAND|wx.ALL, 15)
        border.Add(inner_horizont_2, 1, wx.EXPAND|wx.ALL, 15)

        
        self.SetSizer(border)
        


        
class Frm(wx.Frame, CtrWCloseUtil):
    
    def __init__(self, obj):
                               
        wx.Frame.__init__(self, parent=None, id=-1, title='DATEV detail information form',
                          size=(650,600))
        
        CtrWCloseUtil.__init__(self)
        
        panel = DatevPanel(self, obj)
        
        

def showForm(obj):
    print "datev showForm()"        
    frame = Frm( obj )
    frame.Show()        


if __name__=='__main__':

    from dbtable.datev import getSampleObj
    

    
    
    wx.SetDefaultPyEncoding('utf-8')
    app = wx.App()
    frame = Frm( getSampleObj(375779) )
    frame.Show()
    app.MainLoop()
    
    
