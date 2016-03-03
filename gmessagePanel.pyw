import os
import wx
import datetime
from time import sleep
import wx.lib.agw.pybusyinfo as PBI
import wx.lib.popupctl as pop
from ObjectListView import ObjectListView, ColumnDefn
from ObjectListView import Filter
import functions as fun
from functions import Datahandler
flags = [(wx.ICON_INFORMATION, "ICON_INFORMATION")]
from serverManager import ServerAccess


class Messages(wx.Panel, pop.PopupControl):
    def __init__(self, parent, Type):
        wx.Panel.__init__(self, parent=parent, size=(400, 400))
        self.func = Datahandler()
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.type = Type        
        self.font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.font2 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)

        label1 = wx.StaticText(self, -1, "Groups")
        label1.SetFont(self.font2)
        
        self.groups = wx.Choice(self, -1, choices=[], size=(270, -1))
        self.groups.SetFont(self.font)
        if self.type == "quicktxt":
            hsbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Category'), orient=wx.HORIZONTAL)
            msg = ""
        elif self.type == "general":
            hsbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Category'), orient=wx.HORIZONTAL)
            msg = ""

        self.info = wx.InfoBar(self)    
        action = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Action Panel'), orient=wx.VERTICAL)
        self.search = wx.SearchCtrl(self, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        self.search.SetFont(self.font)
        
        self.selectall = wx.Button(self, -1, "Select All")
        self.selectall.SetFont(self.font)
        self.sms = wx.TextCtrl(self, -1, msg, style=wx.TE_MULTILINE, size=(500, 74))
        self.sms.SetFont(self.font)
        self.clearSms = wx.Button(self, -1, "Clear")
        self.clearSms.SetFont(self.font)
        self.sendSms = wx.Button(self, -1, "Send")
        self.sendSms.SetFont(self.font)
        self.Bind(wx.EVT_BUTTON, self.OnsendSms, self.sendSms)
        self.Bind(wx.EVT_CHOICE, self.OnGroup, self.groups)
        
        if Type == "quicktxt":
            self.list = ObjectListView(self, wx.ID_ANY, size=(510, 100), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
            userImageIndex = self.list.AddNamedImages("music", self._imagePath("user16.png"))
            self.list.SetColumns([
                ColumnDefn("Name", "left", 200, "Name", autoCompleteCellEditor=True, imageGetter=userImageIndex),
                ColumnDefn("Phone", "left", 150, "Phone", isSpaceFilling=True, checkStateGetter="isActive"),
                ColumnDefn("Group", "left", 50, "Group", isSpaceFilling=True)
            ])            
        else:            
            self.list = ObjectListView(self, wx.ID_ANY, size=(900, 230), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
            userImageIndex = self.list.AddNamedImages("music", self._imagePath("user16.png"))        
            self.list.SetColumns([
                ColumnDefn("Name", "left", 200, "Name", autoCompleteCellEditor=True, imageGetter=userImageIndex),
                ColumnDefn("Phone", "left", 150, "Phone", isSpaceFilling=True, checkStateGetter="isActive"),
                ColumnDefn("Group", "left", 50, "Group", isSpaceFilling=True),
                
            ])          
            
        self.list.SetFont(self.font)
        self.Bind(wx.EVT_BUTTON, self.OnSelectaAll, self.selectall)
        self.Bind(wx.EVT_BUTTON, self.OnclearSms, self.clearSms)
        self.Bind(wx.EVT_BUTTON, self.OnsendSms, self.sendSms)

#=======LAYOUT MANAGEMENT=========================================================================================
        hsbox1 = wx.BoxSizer(wx.VERTICAL)
        hsbox2 = wx.BoxSizer(wx.VERTICAL)
        hsbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox.Add(label1, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hsbox.Add(self.groups, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hsbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox.Add(hsbox2)
        hsbox3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        hsbox3Sizer.Add(self.selectall, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        hsbox3Sizer.Add(self.search, 0, wx.ALIGN_BOTTOM | wx.ALL, 10)

        hsbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox4.Add(self.clearSms, 0, wx.ALIGN_LEFT | wx.ALL, 4)
        hsbox4.Add(self.sendSms, 0, wx.ALIGN_LEFT | wx.ALL, 4)
        action.Add(self.sms, 0, wx.ALIGN_LEFT | wx.ALL, 4)
        action.Add(hsbox4, 0, wx.ALIGN_LEFT | wx.ALL, 4)

        sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridBagSizer(hgap=50, vgap=5)
        sizer.Add(self.info, 0, wx.EXPAND)
        grid_sizer.Add(hsbox, pos=(0, 0))
        grid_sizer.Add(action, pos=(0, 1), span=(1, 2))
        grid_sizer.Add(hsbox3Sizer, pos=(1, 0), span=(1, 2))
        grid_sizer.Add(self.list, pos=(2, 0), span=(1, 2))
        sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        self.SetSizer(sizer)
        self.GetSizer().Layout()
        self.InitSearchCtrls()
        self.initialize()

    def initialize(self):
        if self.type == "general":
            members = self.func.get_group_members()
            self.list.SetObjects(members)
            self.list.RepopulateList()
        groups = self.func.get_groups()
        self.groups.AppendItems(groups)
        self.groups.Refresh()

    def InitSearchCtrls(self):        
        for (searchCtrl, olv) in [(self.search, self.list)]:            
            def _handleText(evt, searchCtrl=searchCtrl, olv=olv):
                self.OnTextSearchCtrl(evt, searchCtrl, olv)

            def _handleCancel(evt, searchCtrl=searchCtrl, olv=olv):
                self.OnCancelSearchCtrl(evt, searchCtrl, olv)
            searchCtrl.Bind(wx.EVT_TEXT, _handleText)
            searchCtrl.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, _handleCancel)
            olv.SetFilter(Filter.TextSearch(olv, olv.columns[0:8]))

    def OnTextSearchCtrl(self, event, searchCtrl, olv):
        searchCtrl.ShowCancelButton(len(searchCtrl.GetValue()))
        olv.GetFilter().SetText(searchCtrl.GetValue())
        olv.RepopulateList()
        
    def OnCancelSearchCtrl(self, event, searchCtrl, olv):
        searchCtrl.SetValue("")
        self.OnTextSearchCtrl(event, searchCtrl, olv)

    def OnDoSearch(self, value):
        self.list.GetFilter().SetText(value)
        self.list.RepopulateList()

    def OnGroup(self, evt):
        clients = self.func.get_group_clients(str(self.groups.GetStringSelection()))
        self.list.SetObjects(clients)
        self.list.RepopulateList()

    def OnTowns(self, event):
        if self.selected:
            self.OnDoSearch(self.towns.GetStringSelection())
            return
        if self.selAll.IsChecked() == 1:
            self.selected = True
            self.packages = self.func.fun_get_clients_by_location(self.towns.GetStringSelection())
            self.list.SetObjects(None)
            self.list.SetObjects(self.packages)
            self.list.RepopulateList()
            self.list.SetEmptyListMsg("No inactive Clients")
            return                
        self.OnDoSearch(self.towns.GetStringSelection())

    def OnSelectaAll(self, olv):
        label = self.selectall.GetLabel()
        objects = self.list.GetObjects()
        if label == "Select All":
            self.list.SelectAll()
            for obj in objects:
                self.list.SetCheckState(obj, True)
            self.list.RefreshObjects(objects)
            self.selectall.SetLabel("Deselect All")
            
        else:
            self.list.DeselectAll()
            for obj in objects:
                self.list.SetCheckState(obj, False)
            self.list.RefreshObjects(objects)
            self.selectall.SetLabel("Select All")
        
    def OnDeselectAll(self, olv):
        self.list.DeselectAll()        
    
    def OnclearSms(self, evt):
        self.sms.Clear()

    def OnsendSms(self, evt):
        tday = datetime.datetime.now()
        message = self.sms.GetValue()
        if message == "":
            wx.MessageBox("No message to send", "EMTPY FIELD", wx.ICON_ERROR)
            return
        selected = self.list.GetSelectedObjects()
        if len(selected) < 2:
            selected = self.list.GetCheckedObjects()            
        if len(selected) > 0:
            looker = False
            lists = list()
            item = 0
            last = len(selected) 
            for i in range(0, last):
                try:
                    phone = (selected[item]['Phone'])
                    name = (selected[item]['Name'])
                    lists.append((name, phone, "waiting", str(self.sms.GetValue()), tday))
                    looker = True                    
                except IOError:
                        wx.MessageBox("Draft " + "cannot be found")
                        break
                        
                item += 1        
            if looker:
                msg = "Sending "+str(len(lists)) + " message(s) to server..."
                print msg
                if len(lists) == 1:
                    message = "One message has been queued"
                else:
                    message = "%d messages have been queued" % len(lists)
                busy = PBI.PyBusyInfo(message, parent=None, title="Server request...")
                wx.Yield()
                sleep(5)
                del busy
                server = ServerAccess(lists)
                server.send_message()
                
            else:
                return wx.MessageBox("Please select recipients!")

        else:
            return wx.MessageBox("Please select recipients!")

    def _imagePath(self, imageFile):
        return os.path.join(os.getcwd(), "images", imageFile)


class Letter(wx.Frame):
    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, -1, title, pos, size, style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW)
        Messages(self, "general")

if __name__ == '__main__':
    app = wx.App(True)
    frame = Letter("Messages", (200, 100), (960, 500))
    frame.Show()
    app.MainLoop()

