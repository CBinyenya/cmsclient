import wx
import cPickle as pickle
from twisted.internet import wxreactor
try:
    wxreactor.install()
except:
    pass
from twisted.internet import reactor
from twisted.cred import credentials
from serverManager import Administration
class WindowsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent,size=(400,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.font=wx.Font(11, wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        self.font2=wx.Font(12, wx.DECORATIVE,wx.NORMAL,wx.NORMAL)

        self.nameLb1 = wx.StaticText(self, -1, "Prev Name:");self.nameLb1.SetFont(self.font)
        self.prevname = wx.TextCtrl(self, -1, "",size=(80,22));self.prevname.SetFont(self.font2)
        self.nameLb2 = wx.StaticText(self, -1, "Prev Password:");self.nameLb2.SetFont(self.font)
        self.prevpass = wx.TextCtrl(self, -1, "",size=(80,22));self.prevpass.SetFont(self.font2)        
        self.nameLb3 = wx.StaticText(self, -1, "Change Name:");self.nameLb3.SetFont(self.font)
        self.curname = wx.TextCtrl(self, -1, "");self.curname.SetFont(self.font2)       
        self.nameLb4 = wx.StaticText(self, -1, "Change Password:");self.nameLb4.SetFont(self.font)
        self.curpass = wx.TextCtrl(self, -1, "");self.curpass.SetFont(self.font2)               
        self.save = wx.Button(self,-1,"Save",size=(80,32))

        addrSizer = wx.FlexGridSizer(cols=4, hgap=5, vgap=5)
        
        addrSizer.AddGrowableCol(3)
        for i in range(0,4):
            addrSizer.Add((0,10)) # some empty space         
        addrSizer.Add(self.nameLb1, 0,
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.prevname, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb2, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.prevpass, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb3, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.curname, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb4, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.curpass, 0, wx.EXPAND)        
        for i in range(0,5):
            addrSizer.Add((0,10)) # some empty space                 
        addrSizer.Add(self.save, 10, wx.EXPAND)        
        
        self.Bind(wx.EVT_BUTTON,self.OnSave,self.save)

        self.init()
        self.SetSizer(addrSizer)
        self.GetSizer().Layout()

    def user_details(self):
        try:
            with open("appfiles/authorization.dat","rb") as confidential:            
                details = pickle.load(confidential)
                if not details:
                    wx.MessageBox("User Details unavailable", "AUTHENTICATION ERROR", wx.ICON_ERROR)
                for user,passwd in details.items():
                    username = user
                    password = passwd
            return (username,password)
        except:
            return wx.MessageBox("Authentication  denied!","File Error",wx.ICON_ERROR)

    def init(self):
        user,passwd = self.user_details()
        self.prevname.SetValue(user)
        self.curname.SetValue(user)

    def OnSave(self, evt):
        prevname = self.prevname.GetValue()
        curname = self.curname.GetValue()
        prevpass = self.prevpass.GetValue()
        curpass = self.curpass.GetValue()
        username,password = self.user_details()
        if prevname == "" or curname == "" or prevpass == "" or curpass == "":
            wx.MessageBox("Please fill in all the Fields","Fields Error",wx.ICON_ERROR)
            return
        if prevpass != password:
            wx.MessageBox("Passwords do not march","Fields Error",wx.ICON_ERROR)
            return
        
        creds = credentials.UsernamePassword(username, password)        
        classs = Administration(creds, "update user", ((username,"password",curpass)))
        classs.runEngine()
        try:
            reactor.run()    
        except:
            pass                
        
        return


#---------------------------------------------------------------------------
class Frame(wx.Frame):
    def __init__(self,title,pos,size):
        wx.Frame.__init__(self,None,-1,title,pos,size,style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW)
        WindowsPanel(self)


if __name__ == '__main__':
    app = wx.App()
    frame = Frame("Messages", (200, 100), (600, 500))
    frame.Show()
    app.MainLoop()
