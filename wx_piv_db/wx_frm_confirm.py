import wx




class MsgConfirmFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """A confirmation form."""
        wx.Frame.__init__(self, None, title="Db update mode.",
                          size=(250,160))
        
        panel = wx.Panel(self, -1)
        
        self.btn_yes = wx.Button(panel, -1, "Yes", pos=(20, 60))
        self.btn_no = wx.Button(panel, -1, "No", pos=(120, 60))
        
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnYes, self.btn_yes)
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnNo, self.btn_no)
        
        self.Center()
        self.Show()
        self.Raise()
        
    def OnClickBtnYes(self, event):
        print "yes"
        return True
    
    def OnClickBtnNo(self, event):
        print "no"
        return False

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MsgConfirmFrame()
    app.MainLoop()