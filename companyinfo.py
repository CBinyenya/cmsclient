import os
import wx
import cPickle as pickle
from twisted.internet import wxreactor
try:
    wxreactor.install()
except:pass
from twisted.internet import reactor
from twisted.cred import credentials
from serverManager import Administration
class WindowsPanel( wx.Panel ) :
    def __init__(self,parent):       
        wx.Panel.__init__(self, parent=parent,size=(400,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.font=wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        self.font2=wx.Font(12,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)

        self.nameLb1 = wx.StaticText(self, -1, "Name:");self.nameLb1.SetFont(self.font)
        self.name = wx.TextCtrl(self, -1, "",size=(80,22));self.name.SetFont(self.font2)
        self.nameLb2 = wx.StaticText(self, -1, "Address:");self.nameLb2.SetFont(self.font)
        self.address = wx.TextCtrl(self, -1, "",size=(80,22));self.address.SetFont(self.font2)        
        self.nameLb3 = wx.StaticText(self, -1, "H.Quarters:");self.nameLb3.SetFont(self.font)
        self.headq = wx.TextCtrl(self, -1, "");self.headq.SetFont(self.font2)       
        self.nameLb4 = wx.StaticText(self, -1, "Branch:");self.nameLb4.SetFont(self.font)
        self.branch = wx.TextCtrl(self, -1, "");self.branch.SetFont(self.font2)       
        self.nameLb5 = wx.StaticText(self, -1, "Town:");self.nameLb5.SetFont(self.font)
        self.town = wx.TextCtrl(self, -1, "");self.town.SetFont(self.font2)       
        self.nameLb6 = wx.StaticText(self, -1, "Telephone");self.nameLb6.SetFont(self.font)
        self.telephone = wx.TextCtrl(self, -1, "");self.telephone.SetFont(self.font2)       
        self.nameLb7 = wx.StaticText(self, -1, "Mobile:");self.nameLb7.SetFont(self.font)
        self.mobile = wx.TextCtrl(self, -1, "");self.mobile.SetFont(self.font2)       
        self.nameLb8 = wx.StaticText(self, -1, "Fax:");self.nameLb8.SetFont(self.font)
        self.fax = wx.TextCtrl(self, -1, "");self.fax.SetFont(self.font2)       
        self.nameLb9 = wx.StaticText(self, -1, "Website:");self.nameLb9.SetFont(self.font)
        self.website = wx.TextCtrl(self, -1, "");self.website.SetFont(self.font2)       
        self.nameLb9l = wx.StaticText(self, -1, "E-mail:");self.nameLb9l.SetFont(self.font)
        self.email = wx.TextCtrl(self, -1, "");self.email.SetFont(self.font2)       
        self.save = wx.Button(self,-1,"Save",size=(80,32))

        #====================================================================================
        self.title = wx.CheckBox(self, -1, "Use Company name in Application title")
        self.returnad = wx.CheckBox(self, -1, "Use company name in return address ")
        self.apptitle = wx.TextCtrl(self, -1, "",size=(240,22))
        self.returnname = wx.TextCtrl(self, -1, "",size=(240,22))
        
        

        
        action = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Other Settings'), orient=wx.VERTICAL)
        
        
        addrSizer = wx.FlexGridSizer(cols=4, hgap=5, vgap=5)
        #addrSizer.AddGrowableCol(1)
        addrSizer.AddGrowableCol(3)
        for i in range(0,4):
            addrSizer.Add((0,10)) # some empty space         
        addrSizer.Add(self.nameLb1, 0,
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.name, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb2, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.address, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb3, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.headq, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb4, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.branch, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb5, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.town, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb6, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.telephone, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb7, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.mobile, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb8, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.fax, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb9, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.website, 0, wx.EXPAND)
        addrSizer.Add(self.nameLb9l, 0, 
                wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL,border=7)
        addrSizer.Add(self.email, 0, wx.EXPAND)
        for i in range(0,5):
            addrSizer.Add((0,10)) # some empty space                 
        addrSizer.Add(self.save, 10, wx.EXPAND)        
        for i in range(0,3):
            addrSizer.Add((0,10)) # some empty space
        smallsizer = wx.BoxSizer(wx.HORIZONTAL)
        action.Add(self.title)
        #smallsizer.Add(wx.StaticText(self,-1,"Title"))
        smallsizer.Add(self.apptitle)
        action.Add(smallsizer)
        smallsizer = wx.BoxSizer(wx.HORIZONTAL)
        action.Add(self.returnad)

        smallsizer.Add(self.returnname)
        action.Add(smallsizer)
        
        addrSizer.Add(action, 10, wx.EXPAND)       

        self.Bind(wx.EVT_CHECKBOX, self.OnRname, self.returnad)
        self.Bind(wx.EVT_CHECKBOX, self.OnTitle, self.title)
        self.Bind(wx.EVT_BUTTON,self.OnSave,self.save)

        self.init()
        self.SetSizer(addrSizer)
        self.GetSizer().Layout()

    def init(self):
        self.apptitle.Enable(False)
        self.returnname.Enable(False)
        self.title.SetValue(True)
        self.returnad.SetValue(True)
        if not os.path.exists("bin/compdetails.dat"):
            return
        try:
            with open("bin/compdetails.dat","rb") as newfile:
                    data = pickle.load(newfile)
        except:
            print "Company details does not exists"
            return
        self.name.SetValue(data["Name"])
        self.address.SetValue(data["Address"])
        self.headq.SetValue(data["Location"])
        self.branch.SetValue(data["Branches"])
        self.town.SetValue(data["Town"])
        self.telephone.SetValue(data["Telephone"])
        self.mobile.SetValue(data["Mobile"])
        self.website.SetValue(data["Website"])
        self.email.SetValue(data["Email"])
        
    def OnTitle(self, evt):
        if not evt.IsChecked():            
            self.apptitle.Enable(True)
        else:
            self.apptitle.Enable(False)
        
    def OnRname(self, evt):        
        if not evt.IsChecked():            
            self.returnname.Enable(True)
        else:            
            self.returnname.Enable(False)
    def OnSave(self, evt):
        wx.MessageBox("Please use BirthMark system to update this settings")

class Frame(wx.Frame):
    def __init__(self,title,pos,size):
        wx.Frame.__init__(self,None,-1,title,pos,size,style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW)
        WindowsPanel(self)

app = wx.App()
if __name__ == '__main__':
    frame = Frame("Messages",(200,100),(600,500))
    frame.Show()
app.MainLoop()


    

