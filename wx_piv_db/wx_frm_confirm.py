import wx




class MsgConfirmFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """A confirmation form."""
        wx.Frame.__init__(self, None, title="Db update mode.",
                          size=(250,160))
        
        panel = wx.Panel(self, -1)
        
        self.decisssion = False
        self.close_me = True
        
        self.btn_yes = wx.Button(panel, -1, "Yes", pos=(20, 60))
        self.btn_no = wx.Button(panel, -1, "No", pos=(120, 60))
        
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnYes, self.btn_yes)
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnNo, self.btn_no)
        
        self.Center()
        self.Show()
        self.Raise()
        
    def OnClickBtnYes(self, event):
        print "yes"
        self.decisssion = True
        return True
        self.Close()
        
    
    def OnClickBtnNo(self, event):
        print "no"
        self.decisssion = False
        return False
        self.Close()
        

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MsgConfirmFrame()
    app.MainLoop()