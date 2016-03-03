import wx
try:
    from agw import foldpanelbar as fpb
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.foldpanelbar as fpb
import cPickle as pickle
from twisted.internet import wxreactor
try:
    wxreactor.install()
except:pass
from twisted.internet import reactor
from twisted.cred import credentials
from serverManager import Administration
def GetMondrianData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82' 

def GetMondrianBitmap():
    return wx.BitmapFromImage(GetMondrianImage())

def GetMondrianImage():
    import cStringIO
    stream = cStringIO.StringIO(GetMondrianData())
    return wx.ImageFromStream(stream)

def GetMondrianIcon():
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon
class CommonlyUsedMethodes(object):
    def __init__(self):        
        with open("appfiles/authorization.dat","rb") as confidential:            
            details = pickle.load(confidential)
        if not details:
            wx.MessageBox("User Details unavailable","AUTHENTIFICATION ERROR",wx.ICON_ERROR)                        
        for user,passwd in details.items():
            self.username = user
            self.password = passwd
        self.creds = credentials.UsernamePassword(self.username, self.password)
    def configuration(self,args):
        classs = Administration(self.creds,"update protocol",args)
        classs.runEngine()
        try:
            reactor.run()    
        except:
            pass               
        return True

class SmsControlPanel(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(400,300), style=wx.DEFAULT_FRAME_STYLE):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        
        self.SetIcon(GetMondrianIcon())
        #self.SetMenuBar(self.CreateMenuBar())
    
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -4])
        self.statusbar.SetStatusText("Server Interface ", 0)
        self.statusbar.SetStatusText("Access To System Configurations Granted!", 1)

        pnl = fpb.FoldPanelBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                               agwStyle=fpb.FPB_VERTICAL)
        #Default protocol panel
        item = pnl.AddFoldPanel("Default sms Protocol", collapsed=True)       
        newfoldpanel = ProtocolPanel(item, wx.ID_ANY)
        pnl.AddFoldPanelWindow(item, newfoldpanel)

        pnl.AddFoldPanelSeparator(item)
        
        #Sms Leopard panel
        item = pnl.AddFoldPanel("SmsLeopard Configuaration", collapsed=True)       
        newfoldpanel = LeopardPanel(item, wx.ID_ANY)
        pnl.AddFoldPanelWindow(item, newfoldpanel)

        pnl.AddFoldPanelSeparator(item)

        #Ozeki sms panel
        item = pnl.AddFoldPanel("Ozeki sms Configuaration", collapsed=True)       
        newfoldpanel = OzekiPanel(item, wx.ID_ANY)
        pnl.AddFoldPanelWindow(item, newfoldpanel)

        pnl.AddFoldPanelSeparator(item)
        #Nexmo sms Panel
        item = pnl.AddFoldPanel("Nexmo sms Configuaration", collapsed=True)       
        newfoldpanel = NexmoPanel(item, wx.ID_ANY)
        pnl.AddFoldPanelWindow(item, newfoldpanel)

        pnl.AddFoldPanelSeparator(item)

        #Crowney sms Panel
        item = pnl.AddFoldPanel("Crowney Configuaration", collapsed=True)       
        newfoldpanel = CrowneyPanel(item, wx.ID_ANY)
        pnl.AddFoldPanelWindow(item, newfoldpanel)

        pnl.AddFoldPanelSeparator(item)



        self.pnl = pnl
    def OnCollapseMe(self, event):

        item = self.pnl.GetFoldPanel(0)
        self.pnl.Collapse(item)

    def OnExpandMe(self, event):

        self.pnl.Expand(self.pnl.GetFoldPanel(0))
        self.pnl.Collapse(self.pnl.GetFoldPanel(1))
class ProtocolPanel(wx.Panel,CommonlyUsedMethodes):
    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER | wx.TAB_TRAVERSAL):
        
        wx.Panel.__init__(self, parent, id, pos, size, style)
        CommonlyUsedMethodes.__init__(self)
        
        self.CreateControls()        
        self.GetSizer().Fit(self)
        self.GetSizer().SetSizeHints(self)
        self.GetSizer().Layout()

    def CreateControls(self):
        font=wx.Font(10,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        subpanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                            wx.NO_BORDER | wx.TAB_TRAVERSAL)
        sizer.Add(subpanel, 1, wx.GROW | wx.ADJUST_MINSIZE, 5)

        subsizer = wx.BoxSizer(wx.VERTICAL)
        subpanel.SetSizer(subsizer)
        label1 = wx.StaticText(subpanel,wx.ID_ANY,"Default Protocol");label1.SetFont(font)
        dpsendBtn = wx.Button(subpanel, wx.ID_ANY, "Save")
        itemstrings = ["smsleopard", "ozekisms", "nexmo","crowney","bulksms"]
        self.choices = wx.Choice(subpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                          itemstrings, 0)
        self.Bind(wx.EVT_BUTTON,self.OnProtocol,dpsendBtn)
        
        
        supersubsizer = wx.BoxSizer(wx.HORIZONTAL)
        supersubsizer.Add(label1,0,wx.GROW | wx.ALL, 2)
        supersubsizer.Add(self.choices,0,wx.GROW | wx.ALL, 1)
        subsizer.Add(supersubsizer,0,wx.GROW | wx.ALL, 1)        
        subsizer.Add(dpsendBtn,0,wx.LEFT | wx.ALL, 5)
    def OnProtocol(self, evt):
        protocol = str(self.choices.GetStringSelection())
        if protocol == "":
            wx.MessageBox("No Protocol Selected","Error",wx.ICON_ERROR)
            return
        args = ("DProtocol",protocol)        
        self.configuration(args)
        
class LeopardPanel(wx.Panel,CommonlyUsedMethodes):
    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER | wx.TAB_TRAVERSAL):        
        wx.Panel.__init__(self, parent, id, pos, size, style)
        CommonlyUsedMethodes.__init__(self)
        self.CreateControls()
        self.GetSizer().Fit(self)
        self.GetSizer().SetSizeHints(self)
        self.GetSizer().Layout()

    def CreateControls(self):
        
        font=wx.Font(10,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        subpanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                            wx.NO_BORDER | wx.TAB_TRAVERSAL)
        sizer.Add(subpanel, 1, wx.GROW | wx.ADJUST_MINSIZE, 5)

        subsizer = wx.BoxSizer(wx.VERTICAL)
        subpanel.SetSizer(subsizer)
        label1 = wx.StaticText(subpanel,wx.ID_ANY,"User Name");label1.SetFont(font)
        label2 = wx.StaticText(subpanel,wx.ID_ANY,"Key");label1.SetFont(font)
        label3 = wx.StaticText(subpanel,wx.ID_ANY,"Sender ID");label1.SetFont(font)
        self.username = wx.TextCtrl(subpanel,wx.ID_ANY,"",size=(253,-1))
        self.key = wx.TextCtrl(subpanel,wx.ID_ANY,"",size=(300,-1))
        self.sender = wx.TextCtrl(subpanel,wx.ID_ANY,"",size=(300,-1))
        self.button = wx.Button(subpanel, wx.ID_ANY, "Save")

        self.Bind(wx.EVT_BUTTON,self.OnLeopard,self.button)
        supersubsizer = wx.BoxSizer(wx.HORIZONTAL)
        supersubsizer.Add(label1,0,wx.GROW | wx.ALL, 2)
        supersubsizer.Add(self.username,0,wx.GROW | wx.ALL, 1)
        subsizer.Add(supersubsizer, 0, wx.GROW | wx.ALL, 1)
        
        supersubsizer = wx.BoxSizer(wx.HORIZONTAL)
        supersubsizer.Add(label2,0,wx.GROW | wx.ALL, 2)
        supersubsizer.Add(self.key,0,wx.GROW | wx.ALL, 1)        
        subsizer.Add(supersubsizer, 0, wx.GROW | wx.ALL, 1)
        supersubsizer = wx.BoxSizer(wx.HORIZONTAL)
        supersubsizer.Add(label3,0,wx.GROW | wx.ALL, 2)
        supersubsizer.Add(self.sender,0,wx.GROW | wx.ALL, 1)
        
        subsizer.Add(supersubsizer, 0, wx.GROW | wx.ALL, 1)
        subsizer.Add(self.button,0,wx.LEFT | wx.ALL, 5)
    def OnLeopard(self, evt):
        name = self.username.GetValue()
        key = self.key.GetValue()
        sender = self.sender.GetValue()
        if (name=="" or key==""):
            wx.MessageBox("Empty Fields","Error",wx.ICON_ERROR)
            return
        if sender == "":
            sender = None
        args = ("smsleopard",(name,key,sender))
        self.configuration(args)
class OzekiPanel(wx.Panel,CommonlyUsedMethodes):
    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER | wx.TAB_TRAVERSAL):        
        wx.Panel.__init__(self, parent, id, pos, size, style)
        CommonlyUsedMethodes.__init__(self)
        
        self.CreateControls()
        self.GetSizer().Fit(self)
        self.GetSizer().SetSizeHints(self)
        self.GetSizer().Layout()

    def CreateControls(self):
        
        font=wx.Font(10,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        subpanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                            wx.NO_BORDER | wx.TAB_TRAVERSAL)
        sizer.Add(subpanel, 1, wx.GROW | wx.ADJUST_MINSIZE, 5)

        subsizer = wx.BoxSizer(wx.VERTICAL)
        subpanel.SetSizer(subsizer)
        label1 = wx.StaticText(subpanel,wx.ID_ANY,"User Name");label1.SetFont(font)
        label2 = wx.StaticText(subpanel,wx.ID_ANY,"Password");label1.SetFont(font)
        self.username = wx.TextCtrl(subpanel,wx.ID_ANY,"",size=(283,-1))
        self.password = wx.TextCtrl(subpanel,wx.ID_ANY,"",size=(300,-1))
        self.button = wx.Button(subpanel, wx.ID_ANY, "Save")
        self.Bind(wx.EVT_BUTTON,self.OnOzeki,self.button)
        supersubsizer = wx.BoxSizer(wx.HORIZONTAL)
        supersubsizer.Add(label1,0,wx.GROW | wx.ALL, 2)
        supersubsizer.Add(self.username,0,wx.GROW | wx.ALL, 1)
        subsizer.Add(supersubsizer, 0, wx.GROW | wx.ALL, 1)
        
        supersubsizer = wx.BoxSizer(wx.HORIZONTAL)
        supersubsizer.Add(label2,0,wx.GROW | wx.ALL, 2)
        supersubsizer.Add(self.password,0,wx.GROW | wx.ALL, 1)
        
        subsizer.Add(supersubsizer, 0, wx.GROW | wx.ALL, 1)
        subsizer.Add(self.button,0,wx.LEFT | wx.ALL, 5)
    def OnOzeki(self, evt):
        name = self.username.GetValue()
        passwd = self.password.GetValue()
        if (name=="" or passwd==""):
            wx.MessageBox("Empty Fields","Error",wx.ICON_ERROR)
            return
        args = ("ozekisms",(name,passwd))
        self.configuration(args)
        
class NexmoPanel(wx.Panel,CommonlyUsedMethodes):
    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER | wx.TAB_TRAVERSAL):        
        wx.Panel.__init__(self, parent, id, pos, size, style)
        CommonlyUsedMethodes.__init__(self)
        
        self.CreateControls()
        self.GetSizer().Fit(self)
        self.GetSizer().SetSizeHints(self)
        self.GetSizer().Layout()

    def CreateControls(self):
        
        font=wx.Font(10,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        subpanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                            wx.NO_BORDER | wx.TAB_TRAVERSAL)
        sizer.Add(subpanel, 1, wx.GROW | wx.ADJUST_MINSIZE, 5)

        subsizer = wx.BoxSizer(wx.VERTICAL)
        subpanel.SetSizer(subsizer)
        label1 = wx.StaticText(subpanel,wx.ID_ANY,"API Key");label1.SetFont(font)
        label2 = wx.StaticText(subpanel,wx.ID_ANY,"API Secrete");label1.SetFont(font)
        self.api_key = wx.TextCtrl(subpanel,wx.ID_ANY,"",size=(281,-1))
        self.api_secrete = wx.TextCtrl(subpanel,wx.ID_ANY,"",size=(270,-1))
        self.button = wx.Button(subpanel, wx.ID_ANY, "Save")
        self.Bind(wx.EVT_BUTTON,self.OnNexmo,self.button)
        supersubsizer = wx.BoxSizer(wx.HORIZONTAL)
        supersubsizer.Add(label1,0,wx.GROW | wx.ALL, 2)
        supersubsizer.Add(self.api_key,0,wx.GROW | wx.ALL, 1)
        subsizer.Add(supersubsizer, 0, wx.GROW | wx.ALL, 1)
        
        supersubsizer = wx.BoxSizer(wx.HORIZONTAL)
        supersubsizer.Add(label2,0,wx.GROW | wx.ALL, 2)
        supersubsizer.Add(self.api_secrete,0,wx.GROW | wx.ALL, 1)
        
        subsizer.Add(supersubsizer, 0, wx.GROW | wx.ALL, 1)
        subsizer.Add(self.button,0,wx.LEFT | wx.ALL, 5)
    def OnNexmo(self,evt):
        key = self.api_key.GetValue()
        sec = self.api_secrete.GetValue()
        if (key=="" or sec==""):
            wx.MessageBox("Empty Fields","Error",wx.ICON_ERROR)
            return
        args = ("nexmo",(key,sec))
        self.configuration(args)
class CrowneyPanel(wx.Panel,CommonlyUsedMethodes):
    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER | wx.TAB_TRAVERSAL):        
        wx.Panel.__init__(self, parent, id, pos, size, style)
        CommonlyUsedMethodes.__init__(self)
        
        self.CreateControls()
        self.GetSizer().Fit(self)
        self.GetSizer().SetSizeHints(self)
        self.GetSizer().Layout()

    def CreateControls(self):
        
        font=wx.Font(10,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        subpanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                            wx.NO_BORDER | wx.TAB_TRAVERSAL)
        sizer.Add(subpanel, 1, wx.GROW | wx.ADJUST_MINSIZE, 5)

        subsizer = wx.BoxSizer(wx.VERTICAL)
        subpanel.SetSizer(subsizer)
        label1 = wx.StaticText(subpanel,wx.ID_ANY,"Server");label1.SetFont(font)
        label2 = wx.StaticText(subpanel,wx.ID_ANY,"Port");label1.SetFont(font)
        self.server = wx.TextCtrl(subpanel,wx.ID_ANY,"",size=(100,-1))
        self.port = wx.TextCtrl(subpanel,wx.ID_ANY,"",size=(114,-1))
        self.button = wx.Button(subpanel, wx.ID_ANY, "Save")
        self.Bind(wx.EVT_BUTTON,self.OnCrowney,self.button)
        supersubsizer = wx.BoxSizer(wx.HORIZONTAL)
        supersubsizer.Add(label1,0,wx.GROW | wx.ALL, 2)
        supersubsizer.Add(self.server,0,wx.GROW | wx.ALL, 1)
        subsizer.Add(supersubsizer, 0, wx.GROW | wx.ALL, 1)
        
        supersubsizer = wx.BoxSizer(wx.HORIZONTAL)
        supersubsizer.Add(label2,0,wx.GROW | wx.ALL, 2)
        supersubsizer.Add(self.port,0,wx.GROW | wx.ALL, 1)
        
        subsizer.Add(supersubsizer, 0, wx.GROW | wx.ALL, 1)
        subsizer.Add(self.button,0,wx.LEFT | wx.ALL, 5)
    def OnCrowney(self, evt):
        server = self.server.GetValue()
        port = self.port.GetValue()
        if (server=="" or port==""):
            wx.MessageBox("Empty Fields","Error",wx.ICON_ERROR)
            return
        if not port.isdigit():
            wx.MessageBox("Port value must be an integer","Error",wx.ICON_ERROR)
            return
        args = ("nexmo",(server,port))
        self.configuration(args)

def runProtocol():
    app = wx.App()
    frame = SmsControlPanel()
    frame.Show()
    app.MainLoop()




























































