import wx
import os
import sys
import time
import threading
import cPickle as pickle
from twisted.internet import wxreactor
try:
    wxreactor.install()    
except:    
    pass
from twisted.internet import reactor
import wx.lib.agw.gradientbutton as GB
import wx.lib.platebtn as platebtn
from serverManager import Authorization
class LoginForm(wx.Frame): 
    def __init__(self): 
        wx.Frame.__init__(self, None, -1, 'Log in', 
                size=(450, 250))
        bitmapDir = "images/"
        bitmap = wx.Bitmap(os.path.normpath(bitmapDir+"success.png"), wx.BITMAP_TYPE_PNG)
        process = wx.Bitmap(os.path.normpath(bitmapDir+"process.png"), wx.BITMAP_TYPE_PNG)
        exitmap =wx.Bitmap(os.path.normpath(bitmapDir+"exit.png"), wx.BITMAP_TYPE_PNG)       
        panel = wx.Panel(self) 
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(panel, -1, " LOGIN  FORM ")          
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, -1, "User Name:")
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.name = wx.TextCtrl(panel, -1, "", size=(80,-1))
        self.name.SetHelpText("Here's some help text for field #1")
        box.Add(self.name, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, -1, "Password:")
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.password = wx.TextCtrl(panel, -1, "", style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER,size=(80,-1))
        self.password.SetHelpText("Here's some help text for field #2")
        box.Add(self.password, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(panel, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.RIGHT|wx.BOTTOM, 5)
        login = GB.GradientButton(panel,-1,bitmap, "Log In")
        cancel = GB.GradientButton(panel, -1,exitmap, "Cancel")
        config = GB.GradientButton(panel, -1, process, "Configure!")
        self.Bind(wx.EVT_KEY_DOWN,self.OnLogin,self.password)
        self.Bind(wx.EVT_BUTTON, self.OnLogin,login)
        self.Bind(wx.EVT_BUTTON, self.OnCancel,cancel)
        self.Bind(wx.EVT_BUTTON, self.OnConfig,config)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(login, 0, wx.ALIGN_CENTRE|wx.ALL, 5);
        box.Add(config, 1, wx.ALIGN_CENTRE|wx.ALL, 5);box.Add(cancel, 2, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        panel.SetSizer(sizer)

    def OnLogin(self, evt):
        name = self.name.GetValue(); password = self.password.GetValue()
        if (not name or not password ):
            wx.MessageBox("Please Enter both Username and Password","Value Error",wx.ICON_ERROR)
            return
        dict = {}
        dict[name] = password        
        condition = threading.Condition()        
        th1 = threading.Thread(name="Server client",target=self.data_handler,
                               args =(condition,name,password))
        th2 = threading.Thread(name="Credentials checker",target=self.assert_user,
                               args = (condition,[name,password]))
        th2.start()
        th1.start()
        
        return
    def data_handler(self,cond,name,password):
        refer = {'username':str(name),
                 'password':str(password)}
        with cond:
            classs = Authorization(refer)
            classs.runEngine()
            try:           
                reactor.run()                        
            except: 
                pass
            cond.notifyAll()
            
    def assert_user(self,cond,values):        
        with cond:
            cond.wait()
            time.sleep(2)                        
            try:
                with open("appfiles/authorization.dat","rb") as confidential:            
                    details = pickle.load(confidential)
                    if not details:
                        wx.MessageBox("Wrong Username Or password. Please Try again!","LOGIN ERROR",wx.ICON_ERROR)                        
                    for user,passwd in details.items():
                        if (user==values[0]) and (passwd==values[1]):                                               
                            self.Hide()
                            reactor.stop()
                            self.Close(True)
                            print "Application is loading up"
                            return
                        else:
                            wx.MessageBox("Wrong Username Or password. Please Try again!","LOGIN ERROR",wx.ICON_ERROR)
                            return False
            except:
                wx.MessageBox("Wrong Username Or password. Please Try again!","LOGIN ERROR",wx.ICON_ERROR)
                return False       
    def OnCancel(self , evt):
        self.Hide()
        reactor.stop()
        self.Close(True)
        sys.exit()
        
        
    def OnConfig(self , evt):
        dlg = wx.TextEntryDialog(self, 'Enter server Name','Server Name', 'Server')
        dlg.SetValue("LOCALHOST")
        if dlg.ShowModal() == wx.ID_OK:            
            with open("AppDetails.data","w") as f:
                f.write(dlg.GetValue())
        dlg.Destroy()

        
        
class GradientPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)        
        col1 = wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        col2 = platebtn.AdjustColour(col1, -90)
        col1 = platebtn.AdjustColour(col1, 90)
        rect = self.GetClientRect()
        grad = gc.CreateLinearGradientBrush(0, 1, 0, rect.height - 1, col2, col1)

        pen_col = tuple([min(50, x) for x in platebtn.AdjustColour(col1, -60)])
        gc.SetPen(gc.CreatePen(wx.Pen(pen_col, 1)))
        gc.SetBrush(grad)
        gc.DrawRectangle(0, 1, rect.width - 0.5, rect.height - 1.5)

        evt.Skip()




class MyApp(wx.App):
    def OnInit(self):
        self.SetExitOnFrameDelete(True)        
        frame = LoginForm()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(False)
reactor.registerWxApp(app)   
def runLogin():    
    reactor.run()
    
    app.MainLoop()
runLogin()
