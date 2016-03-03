import wx,os,sys,shelve
from contextlib import closing
import wx.lib.agw.gradientbutton as GB
import wx.lib.platebtn as platebtn

class ConfigurePanel(wx.Frame): 
    def __init__(self): 
        wx.Frame.__init__(self, None, -1, 'Configuration Panel',size=(450, 450))
        bitmapDir = "images/"
        bitmap = wx.Bitmap(os.path.normpath(bitmapDir+"tick16.png"), wx.BITMAP_TYPE_PNG)
        process = wx.Bitmap(os.path.normpath(bitmapDir+"process.png"), wx.BITMAP_TYPE_PNG)
        exitmap =wx.Bitmap(os.path.normpath(bitmapDir+"exit.png"), wx.BITMAP_TYPE_PNG)
        #panel = GradientPanel(self)
        panel = wx.Panel(self) 
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(panel, -1, " LOGIN  FORM ")
        #label.SetHelpText("This is the help text for the label")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, -1, "User Name:")       
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.name = wx.TextCtrl(panel, -1, "", size=(80,-1))
        self.name.SetHelpText("Name for the user of this computer")
        box.Add(self.name, 1, wx.ALIGN_CENTRE|wx.ALL, 5)


        label = wx.StaticText(panel, -1, "Password:")        
        box.Add(label, 2, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.password = wx.TextCtrl(panel, -1, "", style=wx.TE_PASSWORD,size=(80,-1))
        label.SetHelpText("Password for the user of this computer.\nNote:This note the database password")
        box.Add(self.password, 3, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        

        label = wx.StaticText(panel, -1, "Server Name:")        
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.servername = wx.TextCtrl(panel, -1, "", size=(80,-1))
        self.servername.SetHelpText("Name of the server to use")
        box.Add(self.servername, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, -1, "Database User Name:")        
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.dbusername = wx.TextCtrl(panel, -1, "", size=(80,-1))
        self.dbusername.SetHelpText("User of the database as set by the Database Administrator")
        box.Add(self.dbusername, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, -1, "Port No")        
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.port = wx.TextCtrl(panel, -1, "", size=(80,-1))
        self.port.SetHelpText("Port of the server")
        box.Add(self.port, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, -1, "Database Password")
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.dbpassword = wx.TextCtrl(panel, -1, "", style=wx.TE_PASSWORD,size=(80,-1))
        self.dbpassword.SetHelpText("Password for the user as set by the Database Administrator")
        box.Add(self.dbpassword, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, -1, "Database:")        
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.dbname = wx.TextCtrl(panel, -1, "", size=(80,-1))
        self.dbname.SetHelpText("Databse name")
        box.Add(self.dbname, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    

        line = wx.StaticLine(panel, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.RIGHT|wx.BOTTOM, 5)
        login = GB.GradientButton(panel,-1,bitmap, "Save")
        cancel = GB.GradientButton(panel, -1,exitmap, "Cancel")
        config = GB.GradientButton(panel, -1, process, "Back")
        self.Bind(wx.EVT_BUTTON, self.OnSave,login)
        self.Bind(wx.EVT_BUTTON, self.OnCancel,cancel)
        self.Bind(wx.EVT_BUTTON, self.OnBack,config)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(login, 0, wx.ALIGN_CENTRE|wx.ALL, 5);box.Add(config, 1, wx.ALIGN_CENTRE|wx.ALL, 5);box.Add(cancel, 2, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        panel.SetSizer(sizer)

    def OnSave(self, evt):
        name = self.name.GetValue(); password = self.password.GetValue();server = self.servername.GetValue()
        dbuser = self.dbusername.GetValue();port = self.port.GetValue();dbpassword = self.dbpassword.GetValue()
        database = self.dbname.GetValue()
        list_ = [name,password,server,dbuser,port,dbpassword,database]
        dat = ([x for x in list_ if x ==""])
        try:dat.pop();wx.MessageBox("please fill in the all the fields")
        except:
            with closing(shelve.open('appinfo.db')) as s:                         
                         s["userdetails"] = {'username':list_[0],'password':list_[1]}
                         s['Appsettings'] = {'server':list_[2],'user':list_[3],'port':list_[4],'dbpassword':list_[5],'database':list_[6]}
                         
            with closing(shelve.open('appinfo.db')) as s:
                    name2,password2 = s['userdetails']['username'],s['userdetails']['password']
                    data = s['Appsettings']
            for keys,values in data.items():
                print keys,values
            
                        
            
                
        
    def OnCancel(self , evt):
        self.Close()
        sys.exit()
    def OnBack(self , evt):
        self.Close()
        import login
        sys.exit()
        
        
        

def runConfig():
        app = wx.PySimpleApp()
        frame = ConfigurePanel()
        frame.Show() 
        app.MainLoop() 

#runConfig()
