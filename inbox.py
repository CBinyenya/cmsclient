import os
import wx
import time
import cPickle as pickle
from twisted.internet import wxreactor
try:
    wxreactor.install()
except:pass
from twisted.internet import reactor
from twisted.cred import credentials
from ObjectListView import ObjectListView, ColumnDefn
import wx.lib.agw.pybusyinfo as Pbi
from functions import InboxManager as inbox
from functions import Datahandler
from serverManager import Administration, ServerAccess
class CommonlyUsedMethodes(object):
    def __init__(self):        
        with open("appfiles/authorization.dat","rb") as confidential:            
            details = pickle.load(confidential)
        if not details:
            wx.MessageBox("User Details unavailable", "AUTHENTIFICATION ERROR", wx.ICON_ERROR)
        for user, passwd in details.items():
            self.username = user
            self.password = passwd
        self.creds = credentials.UsernamePassword(self.username, self.password)

    def getMessages(self,args):
        classs = Administration(self.creds,"get messages",args)
        classs.runEngine()
        try:
            reactor.run()    
        except:
            pass
        return True

    def deleteMessages(self,content):
        classs = Administration(self.creds, "delete messages", content)
        classs.runEngine()
        try:
            reactor.run()    
        except:
            pass                
        
        return True


class InboxPanel(wx.Panel, inbox, CommonlyUsedMethodes):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent,size=(600,700))
        self.func = Datahandler()
        inbox.__init__(self)
        CommonlyUsedMethodes.__init__(self)
        self.font1 = wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.panel1 = wx.Panel(self, -1, size=(600, 135))
        self.panel2 = wx.Panel(self, -1, size=(582, 500))
        self.panel2.SetBackgroundColour('White')
        self.label1 = wx.StaticText(self.panel1, -1, "Outbox Messages")
        self.label1.SetFont(self.font1)
        self.update = wx.Button(self.panel1, 101, "Update")
        self.refresh = wx.Button(self.panel1, 102, "Refresh")
        self.delete = wx.Button(self.panel1, 103, "Delete")
        self.deleteAll = wx.Button(self.panel1, 104, "Delete All")
        self.resend = wx.Button(self.panel1, 105, "Resend")
        self.resendAll = wx.Button(self.panel1, 106, "Resend All")
        self.select = wx.Button(self.panel1, 107, "Select All")
        self.select.SetFont(self.font1)
        self.list = ObjectListView(self.panel2,-1,size=(600,435),style = wx.LC_REPORT|wx.SUNKEN_BORDER)

        self.Bind(wx.EVT_BUTTON, self.OnButton, id=101)
        self.Bind(wx.EVT_BUTTON, self.OnButton, id=102)
        self.Bind(wx.EVT_BUTTON, self.OnButton, id=103)
        self.Bind(wx.EVT_BUTTON, self.OnButton, id=104)
        self.Bind(wx.EVT_BUTTON, self.OnButton, id=105)
        self.Bind(wx.EVT_BUTTON, self.OnButton, id=106)
        self.Bind(wx.EVT_BUTTON, self.OnSelect, id=107)
        self._DoLayout()       
        self.Init()
        
    def Init(self):
        def image_type(dict):
            if dict['status'] == "waiting":
                return "waiting"
            elif dict['status'] == "sent":
                return "sent"
            elif dict['status'] == "failed":
                return "failed"
            else:
                return "new"

        messages = self.func.get_outbox()
        self.list.AddNamedImages("sent", self._imagePath("success.png"))
        self.list.AddNamedImages("waiting", self._imagePath("waiting.png"))
        self.list.AddNamedImages("failed", self._imagePath("failed.png"))
        self.list.AddNamedImages("new", self._imagePath("new.png"))        
        columns = [
            ColumnDefn("Recipient", "left", 100, "name",imageGetter=image_type),
            ColumnDefn("Status", "left", 70, "status"),
            ColumnDefn("Date", "left", 110, "date"),
            ColumnDefn("Message", "left", 300, "message", autoCompleteCellEditor=True, isSpaceFilling=True)
            ]
        self.list.SetColumns(columns)
        self.list.SetObjects(messages)

        if self.username != "Admin" or self.username != "admin":
            self.delete.Disable()
            self.deleteAll.Disable()
        self.resend.Disable()
        self.resendAll.Disable()

    def _DoLayout(self):
        buttons = [self.update, self.refresh, self.delete, self.resendAll,
                   self.resend, self.deleteAll]
        sizer = wx.GridBagSizer(vgap=5, hgap=5)
        box_1 = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridSizer(rows=2, cols=3, hgap=2, vgap=5)
        for i in buttons:
            i.SetFont(self.font1)
            grid.Add(i, 0, 0)
        box_1.Add(self.label1, 1, wx.ALL | wx.CENTER, 1)
        box_1.Add(grid, 1 , wx.ALL | wx.EXPAND, 10)
        box_1.Add(self.select, 1, wx.ALL | wx.LEFT, 4)
        self.panel1.SetSizer(box_1)
        box_2 = wx.BoxSizer(wx.VERTICAL)
        box_2.Add(self.list, 1, wx.ALL | wx.EXPAND, 4)
        self.panel2.SetSizer(box_2)
        sizer.Add(self.panel1, pos=(0, 0))
        sizer.Add(self.panel2, pos=(1, 0))
        self.SetSizer(sizer)
        self.Layout()

    def OnButton(self, evt):
        selected = self.list.GetSelectedObjects()
        id = evt.GetId()
        if id == 101:
            server = ServerAccess("")
            server.get_outbox_messages()
            busy = Pbi.PyBusyInfo("Please wait a moment...", parent=None, title="Server Request..")
            wx.Yield()
            time.sleep(3)
            messages = self.func.get_outbox()
            del busy
            self.list.SetObjects(messages)
            self.list.RepopulateList()
        elif id == 102:
            messages = self.func.get_outbox()
            self.list.SetObjects(messages)
            self.list.RepopulateList()
        elif id == 103:
            print len(selected)
            if len(selected) == 0:
                wx.MessageBox("Select message to delete", "Error", wx.ICON_ERROR)
                return
            else:
                dlg = wx.MessageBox("Are you sure of this process ?", "Confirmation", wx.ICON_INFORMATION | wx.YES_NO)
                if dlg == wx.NO:
                    return
                for msg in selected:
                    details = msg['recipient'], msg['date']
                    self.deleteMessages(details)
        elif id == 104:
            dlg = wx.MessageBox("Are you sure of this process ?", "Confirmation", wx.ICON_INFORMATION | wx.YES_NO)
            if dlg == wx.NO:
                return
            self.deleteMessages("delete all")            
            self.backup()
            self.list.SetObjects(None)
            self.list.RepopulateList()
        
        else:
            with open("appfiles/authorization.dat", "rb") as confidential:
                details = pickle.load(confidential)
            for user, passwd in details.items():
                self.username = user
                self.password = passwd
            dtails = [self.username, self.password]
            wx.MessageBox("Resend protocol has been initiated", "Information", wx.ICON_INFORMATION)

    def OnSelect(self, evt):
        label = self.select.GetLabel()
        if label == "Select All":
            self.list.SelectAll()
            self.select.SetLabel("Deselect All")
        else:
            self.list.DeselectAll()
            self.select.SetLabel("Select All")
        
    def _imagePath(self, image):
        return os.path.join(os.getcwd(), "images", image)


class TheFrame(wx.Frame):
    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        dlg = InboxPanel(self)
        
if __name__ == '__main__':
    app = wx.App()
    frame = TheFrame("New", (300, 200), (600, 500)).Show()
    app.MainLoop()
