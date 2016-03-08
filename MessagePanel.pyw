import wx
import os
import string
import datetime
from time import sleep
from twisted.internet import wxreactor
try:
    wxreactor.install()
except:
    pass
from twisted.internet import reactor
from functions import Datahandler
from serverManager import ServerAccess
import wx.lib.agw.pybusyinfo as PBI
import wx.lib.popupctl as pop
import wx.calendar as wxcal
from ObjectListView import ObjectListView, ColumnDefn
from ObjectListView import Filter

flags = [(wx.ICON_INFORMATION, "ICON_INFORMATION")]


class Messages(wx.Panel, pop.PopupControl):
    def __init__(self, parent, Type):
        self.func = Datahandler()
        wx.Panel.__init__(self, parent=parent, size=(400, 400))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.type = Type
        self.font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.font2 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.labels = ["Location", "Occupation", "Type"]
        TypeOfClient = ["ACTIVE", "INACTIVE"]
        self.selected = False

        Towns = self.func.fun_get_location()
        Occ = self.func.fun_get_occupation()
        label1 = wx.StaticText(self, -1, self.labels[0])
        label1.SetFont(self.font2)
        label2 = wx.StaticText(self, -1, self.labels[1])
        label2.SetFont(self.font2)
        label3 = wx.StaticText(self, -1, self.labels[2])
        label3.SetFont(self.font2)
        self.towns = wx.Choice(self, -1, choices=Towns, size=(120, -1))
        self.towns.SetFont(self.font)
        self.occ = wx.Choice(self, -1, choices=Occ, size=(120, -1))
        self.occ.SetFont(self.font)
        self.clienttype = wx.Choice(self, -1, choices=TypeOfClient, size=(120, -1))
        self.clienttype.SetFont(self.font)
        self.selAll = wx.CheckBox(self, -1, 'Select by Category', size=(150, -1))
        self.selAll.SetFont(self.font2)
        
        if Type == "balance":
            hsbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Category'), orient=wx.HORIZONTAL)
            self.packages = self.func.balanceClients()
            msg = "Dear Client, your outstanding insurance premium balance is Ksh $AMOUNT. Kindly send your payment."
        elif Type == "renewal":
            hsbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Category'), orient=wx.HORIZONTAL)
            self.From = pop.PopupControl(self, -1)
            self.To = pop.PopupControl(self, -1)
            self.win1 = wx.Window(self.From, -1, pos=(0, 0), style = 0)
            self.cal1 = wxcal.CalendarCtrl(self.win1, -1, pos=(0, 0))
            bz = self.cal1.GetBestSize()
            self.win1.SetSize(bz)
            self.From.SetPopupContent(self.win1)
            self.win2 = wx.Window(self.To, -1, pos=(0, 0), style = 0)
            self.cal2 = wxcal.CalendarCtrl(self.win2, -1, pos=(0, 0))
            bz = self.cal2.GetBestSize()
            self.win2.SetSize(bz)
            self.To.SetPopupContent(self.win2)
            self.cal1.Bind(wxcal.EVT_CALENDAR, self.OnCalSelected1)
            self.cal2.Bind(wxcal.EVT_CALENDAR, self.OnCalSelected2)
            self.packages = self.func.expiryClients()
            msg = "Dear Client your $POLICY policy expires on $DATE. Kindly send us the renewal instructions."
        elif Type == "newinvoice" or Type == "extensions":
            hsbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Category'), orient=wx.HORIZONTAL)
            if Type == "extensions":
                self.packages = self.func.extensionClients()
            else:
                self.packages = self.func.renewalClients()
            msg = "Dear Client. We have renewed your $POLICY policy. Kindly let us have your payment of Ksh:$AMOUNT."
        elif Type == "quicktxt":
            hsbox = wx.BoxSizer(wx.HORIZONTAL)
            self.phn_number = wx.TextCtrl(self, -1, "")
            self.phn_number.SetFont(self.font)
            self.towns.Hide()
            self.occ.Hide()
            self.clienttype.Hide()
            self.selAll.Hide()
            label1.Hide()
            label2.Hide()
            label3.Hide()
            self.packages = []
            msg = ""
        elif Type == "general":
            hsbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Category'), orient=wx.HORIZONTAL)
            self.packages = self.func.allClients()
            msg = ""

        elif Type == "birthday":
            hsbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Category'), orient=wx.HORIZONTAL)
            msg = "Happy birthday!"
            self.packages = self.func.birthdayClients()
            self.towns.Hide()
            self.occ.Hide()
            self.clienttype.Hide()
            self.selAll.Hide()
            label1.Hide()
            label2.Hide()
            label3.Hide()
            self.tdate = wxcal.GenericCalendarCtrl(self, -1, wx.DateTime.Today(), size=(200, 150))
            self.tdate.Bind(wxcal.EVT_CALENDAR, self.OnCalSelected)
            self.tdate.Bind(wxcal.EVT_CALENDAR_MONTH, self.OnChangeMonth)
            self.tdate.Bind(wxcal.EVT_CALENDAR_SEL_CHANGED, self.OnCalSelChanged)
            self.tdate.Bind(wxcal.EVT_CALENDAR_WEEKDAY_CLICKED, self.OnCalWeekdayClicked)
            
        else:
            pass
        self.info = wx.InfoBar(self)    
        action = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Action Panel'), orient=wx.VERTICAL)
        self.search = wx.SearchCtrl(self, size=(290, -1), style=wx.TE_PROCESS_ENTER)
        self.search.SetFont(self.font)
        
        self.selectall = wx.Button(self, -1, "Select All")
        self.selectall.SetFont(self.font)
        if Type == "renewal":
            self.sms = wx.TextCtrl(self, -1, msg, style=wx.TE_MULTILINE, size=(500, 74))
            self.sms.SetFont(self.font)
        elif Type == "birthday":
            self.sms = wx.TextCtrl(self, -1, msg, style=wx.TE_MULTILINE, size=(400, 74))
            self.sms.SetFont(self.font)
        else:
            self.sms = wx.TextCtrl(self, -1, msg, style=wx.TE_MULTILINE, size=(594, 74))
            self.sms.SetFont(self.font)
        self.clearSms = wx.Button(self, -1, "Clear")
        self.clearSms.SetFont(self.font)
        self.sendSms = wx.Button(self, -1, "Send")
        self.sendSms.SetFont(self.font)
        self.Bind(wx.EVT_BUTTON, self.OnsendSms, self.sendSms)

        if Type == "balance":
            self.list = ObjectListView(self, wx.ID_ANY, size=(973, 244), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
            self.list.SetColumns([
                ColumnDefn("Id", "left", 70, "Id", autoCompleteCellEditor=True, checkStateGetter="isActive"),
                ColumnDefn("Name", "left", 100, "Name", isSpaceFilling=True),
                ColumnDefn("Phone", "left", 150, "Phone", isSpaceFilling=True),
                ColumnDefn("Occ", "left", 100, "Occ", isSpaceFilling=True),
                ColumnDefn("Location", "left", 50, "Town", isSpaceFilling=True),                
                ColumnDefn("Balance", "right", 100, "Amount", isSpaceFilling=False),
                ColumnDefn("Domant", "right", 50, "type", isSpaceFilling=False)
            ])
        elif (Type == "newinvoice") or (Type =="extensions"):
            self.list = ObjectListView(self, wx.ID_ANY,size=(973,244), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
            self.list.SetColumns([
                ColumnDefn("Id", "left", 70, "Id", autoCompleteCellEditor=True,checkStateGetter="isActive"),
                ColumnDefn("TransNo", "left", 100, "TransNo", isSpaceFilling=True),
                ColumnDefn("Name", "left", 100, "Name", isSpaceFilling=True),
                ColumnDefn("Phone", "left", 150, "Phone", isSpaceFilling=True),
                ColumnDefn("Policy", "left", 50, "Policy", isSpaceFilling=True),
                ColumnDefn("Amount", "left", 100, "Amount", isSpaceFilling=True)
            ])

        elif Type == "birthday":
            self.list = ObjectListView(self, wx.ID_ANY,size=(678, 230), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
            userImageIndex = self.list.AddNamedImages("music", self._imagePath("user16.png"))        
            self.list.SetColumns([                
                ColumnDefn("Name", "left", 100, "Name", isSpaceFilling=True, imageGetter=userImageIndex),
                ColumnDefn("Phone", "left", 150, "Phone", isSpaceFilling=True),
                ColumnDefn("DOB", "left", 100, "dob", isSpaceFilling=True)
            ])

        elif Type =="renewal":
            self.list = ObjectListView(self, wx.ID_ANY,size=(973,230), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
            self.list.SetColumns([
                ColumnDefn("Id", "left", 70, "Id", autoCompleteCellEditor=True, checkStateGetter="isActive"),
                ColumnDefn("Name", "left", 100, "Name", isSpaceFilling=True),
                ColumnDefn("Phone", "left", 150, "Phone", isSpaceFilling=True),
                ColumnDefn("Policy", "left", 50, "Policy", isSpaceFilling=True),
                ColumnDefn("Date", "left", 50, "To", isSpaceFilling=True)
                
            ])
        elif Type == "quicktxt":
            self.list = ObjectListView(self, wx.ID_ANY,size=(510,100), style=wx.LC_REPORT|wx.SUNKEN_BORDER)        
            userImageIndex = self.list.AddNamedImages("music", self._imagePath("user16.png"))
            self.list.SetColumns([
                ColumnDefn("Name", "left", 200, "Name", autoCompleteCellEditor=True, imageGetter=userImageIndex),
                ColumnDefn("Phone", "left", 150, "Phone", isSpaceFilling=True)
            ])
            
        else:
            self.list = ObjectListView(self, wx.ID_ANY,size=(973, 244), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
            userImageIndex = self.list.AddNamedImages("music", self._imagePath("user16.png"))        
            self.list.SetColumns([
                ColumnDefn("Id", "left", 70, "Id", autoCompleteCellEditor=True, checkStateGetter="isActive"),
                ColumnDefn("Name", "left", 100, "Name", isSpaceFilling=True),
                ColumnDefn("Phone", "left", 150, "Phone", isSpaceFilling=True),
                ColumnDefn("Occ", "left", 100, "Occ", isSpaceFilling=True),
                ColumnDefn("Location", "left", 50, "Town", isSpaceFilling=True),                
                
                
            ])
        
        self.list.SetObjects(self.packages)        
        self.list.SetFont(self.font)
        if self.type == "quicktxt":
            self.search.Bind(wx.EVT_TEXT, self.OnSearchctrl)
            self.list.SetObjects(None)
        self.Bind(wx.EVT_CHOICE, self.OnTowns, self.towns)
        self.Bind(wx.EVT_CHOICE, self.OnOccu, self.occ)
        self.Bind(wx.EVT_CHOICE, self.OnType, self.clienttype)
        self.Bind(wx.EVT_BUTTON, self.OnSelectaAll, self.selectall)
        self.Bind(wx.EVT_BUTTON, self.OnclearSms, self.clearSms)
        self.Bind(wx.EVT_BUTTON, self.OnsendSms, self.sendSms)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.selAll)

#=======LAYOUT MANAGEMENT=========================================================================================
        hsbox1 = wx.BoxSizer(wx.VERTICAL)
        hsbox2 = wx.BoxSizer(wx.VERTICAL)
        hsbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox4 = wx.BoxSizer(wx.HORIZONTAL)
        if Type == "birthday":
            hsbox2.Add(self.tdate, 0, wx.ALIGN_LEFT, 5)
        elif Type == "quicktxt":
            pass
        elif Type == "renewal":
            label4 = wx.StaticText(self, -1, "From")
            label4.SetFont(self.font2)
            label5 = wx.StaticText(self, -1, "To:")
            label5.SetFont(self.font2)
            hsbox1.Add(label1, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            hsbox1.Add(label2, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            hsbox1.Add(label3, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            hsbox3.Add(label4, 0, wx.ALIGN_LEFT | wx.ALL, 2)
            hsbox3.Add(self.From, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            
            hsbox1.Add(self.selAll, 0, wx.ALIGN_LEFT | wx.ALL, 10)
            hsbox1.Add(hsbox3)        
            hsbox.Add(hsbox1)
            
            hsbox2.Add(self.towns, 0, wx.ALIGN_LEFT | wx.ALL, 2)
            hsbox2.Add(self.occ, 0, wx.ALIGN_LEFT | wx.ALL, 4)
            hsbox2.Add(self.clienttype, 0, wx.ALIGN_LEFT | wx.ALL, 4)
            hsbox2.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_LEFT | wx.ALL, 4)
            hsbox4.Add(label5, 0, wx.ALIGN_LEFT | wx.ALL, 9)
            hsbox4.Add(self.To, 0, wx.ALIGN_LEFT | wx.ALL, 9)
            hsbox2.Add(hsbox4)
        else:
            hsbox1.Add(label1, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            hsbox1.Add(label2, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            hsbox1.Add(label3, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            hsbox1.Add(self.selAll, 0, wx.ALIGN_LEFT | wx.ALL, 10)
            hsbox.Add(hsbox1)        
            hsbox2.Add(self.towns, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            hsbox2.Add(self.occ, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            hsbox2.Add(self.clienttype, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hsbox.Add(hsbox2)
        hsbox3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        hsbox3Sizer.Add(self.selectall, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        hsbox3Sizer.Add(self.search, 0, wx.ALIGN_BOTTOM | wx.ALL, 10)

        hsbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox4.Add(self.clearSms, 0, wx.ALIGN_LEFT | wx.ALL, 4)
        hsbox4.Add(self.sendSms, 0, wx.ALIGN_LEFT | wx.ALL, 4)

        sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridBagSizer(hgap=50, vgap=5)
        sizer.Add(self.info, 0, wx.EXPAND)
        if self.type == "quicktxt":
            phn_ = wx.BoxSizer(wx.HORIZONTAL)
            phn_.Add(wx.StaticText(self, -1, "Phone Number:"), 0, wx.ALIGN_LEFT | wx.ALL, 10)
            phn_.Add(self.phn_number, 0, wx.ALIGN_LEFT | wx.ALL, 10)
            action.Add(phn_)
            action.Add(self.sms, 0, wx.ALIGN_LEFT | wx.ALL, 4)
            action.Add(hsbox4, 0, wx.ALIGN_LEFT | wx.ALL, 4)
            grid_sizer.Add(action, pos=(0, 0))
        else:
            action.Add(self.sms, 0, wx.ALIGN_LEFT | wx.ALL, 4)
            action.Add(hsbox4, 0, wx.ALIGN_LEFT | wx.ALL, 4)
            grid_sizer.Add(hsbox, pos=(0, 0))
            grid_sizer.Add(action, pos=(0, 1), span=(1, 2))
        grid_sizer.Add(hsbox3Sizer, pos=(1, 0), span=(1, 2))
        grid_sizer.Add(self.list, pos=(2, 0), span=(1, 2))
        sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        self.SetSizer(sizer)
        self.GetSizer().Layout()
        if self.type != "quicktxt":
            self.InitSearchCtrls()
        self.initialize()

    def initialize(self):
        messages = self.func.get_messages()
        if messages:
            for message in messages:
                if message['Type'] == self.type:
                    txt = message['Message']
                    self.sms.SetValue(txt)
        
    def OnCalSelected(self, evt):
        pass
       
    def OnCalWeekdayClicked(self, evt):
        pass
    
    def OnCalSelChanged(self, evt):
        newlist = []
        date1 = (evt.GetDate().GetDay(), evt.GetDate().GetMonth()+1)
        for i in self.packages:
            date2 = (i['dob'].date().day, i['dob'].date().month)
            if date1 == date2:                
                newlist.append(i)
        self.list.SetObjects(newlist)
        self.list.RepopulateList()
        
    def OnChangeMonth(self, evt=None):        
        newlist = []
        date1 = (evt.GetDate().GetMonth()+1,)
        for i in self.packages:
            date2 = (i['dob'].date().month,)
            if date1 == date2:                
                newlist.append(i)
        self.list.SetObjects(newlist)
        self.list.RepopulateList()
        
    def OnSearchctrl(self, evt):
        newlist = []
        value = self.search.GetValue()
        if value == "":
            self.list.SetObjects(None)
            return
        for client in self.func.fun_search_clients(value):
            newlist.append(client)
        self.list.SetObjects(newlist)
        self.list.RepopulateList()
        
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
        
    def EvtCheckBox(self, event):
        pass
            
    def OnDoSearch(self, value):
        self.list.GetFilter().SetText(value)
        self.list.RepopulateList()
        
    def OnType(self, event):
        objects = self.list.GetObjects()
        value=self.clienttype.GetStringSelection()        
        if value == "INACTIVE":
            self.packages = self.func.fun_get_active_clients(True, self.type)
            self.list.SetObjects(self.packages)            
            self.list.SetEmptyListMsg("There are no Inactive Clients")              
            
        else:
            self.selected = True
            self.packages = self.func.fun_get_active_clients(False, self.type)
            self.list.SetObjects(self.packages)            
            self.list.SetEmptyListMsg("There are no Active Clients")              
                    
    def OnOccu(self, event):
        if self.selAll.IsChecked() == 1:                        
            town = self.towns.GetStringSelection()
            occu = self.occ.GetStringSelection()            
            self.packages = self.func.fun_get_clients_by_occupation(occu, self.type, town)
            self.list.SetObjects(self.packages)            
            return
        else:
            self.selected = True
            self.packages = self.func.fun_get_clients_by_occupation(self.occ.GetStringSelection(), self.type)
            self.list.SetObjects(self.packages)
            self.list.RepopulateList()
            self.list.SetEmptyListMsg("No such Clients")
            return

    def OnTowns(self, event):
        if self.selAll.IsChecked() == 1:            
            self.OnDoSearch(self.towns.GetStringSelection())
            occu = self.occ.GetStringSelection()
            town = self.towns.GetStringSelection()            
            self.packages = self.func.fun_get_clients_by_location(town, self.type, occu)
            self.list.SetObjects(self.packages)            
            return
        else:
            self.selected = True
            self.packages = self.func.fun_get_clients_by_location(self.towns.GetStringSelection(), self.type)
            self.list.SetObjects(self.packages)
            self.list.RepopulateList()
            self.list.SetEmptyListMsg("No inactive Clients")
            return        
        
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

    def OnclearSms(self, evt):
        self.sms.Clear()

    def OnsendSms(self, evt):
        selected = self.list.GetSelectedObjects()
        tday = datetime.datetime.now()
        lists = []
        looker = False
        if len(selected) < 2:
            selected = self.list.GetCheckedObjects()
        if self.type == "quicktxt":
            phn = self.phn_number.GetValue()
            sms = self.sms.GetValue()
            if phn != "":
                if sms == "":
                    return wx.MessageBox("Please write a message to send", "Error", wx.ICON_ERROR)
                lists.append(("Anonymous", str(phn), "waiting", sms, tday))
                looker = True
                busy = PBI.PyBusyInfo("Please wait...", parent=None, title="Queueing Message")
                wx.Yield()
                sleep(5)
                del busy
                server = ServerAccess(lists)
                server.send_message()
        if len(selected) > 0:
            item = 0
            last = len(selected)
            for i in range(last):                
                try:
                    if self.type == "renewal" or self.type == "extensions":
                        phone, policy, date = (selected[item]['Phone']), (selected[item]['Policy']),\
                                              (selected[item]['To'])
                        name = (selected[item]['Name'])
                        try:
                            values = dict()
                            values['POLICY'] = policy
                            values['DATE'] = date.date()
                        except:
                            continue
                        t = string.Template(str(self.sms.GetValue()))
                        if phone is not None:
                            phone = phone.replace(' ', "")
                        lists.append((name, phone, "waiting", t.substitute(values), tday))
                    elif self.type == "newinvoice":
                        phone, policy, amount = (selected[item]['Phone']), (selected[item]['Policy']),\
                                                (selected[item]['Amount'])
                        name = (selected[item]['Name'])
                        amount = Messages.insert_comma(float(amount))
                        values = dict()
                        values['POLICY'] = policy
                        values['AMOUNT'] = amount
                        t = string.Template(str(self.sms.GetValue()))
                        if phone:
                            phone = phone.replace(' ', "")
                        lists.append((name, phone, "waiting", t.substitute(values), tday))
                        
                    elif self.type == "balance":
                        phone, amount = (selected[item]['Phone']),(selected[item]['Amount'])
                        amount = Messages.insert_comma(float(amount))
                        name = (selected[item]['Name'])
                        values = dict()
                        values['AMOUNT'] = amount
                        t = string.Template(str(self.sms.GetValue()))
                        if phone:
                            phone = phone.replace(' ', "")
                        lists.append((name, phone, "waiting", t.substitute(values), tday))
                    elif self.type == "quicktxt":
                        phn = self.phn_number.GetValue()
                        if phn != "":
                            lists.append((["Anonymouse", phn], self.sms.GetValue()))
                        phone = (selected[item]['Phone'])
                        name = (selected[item]['Name'])
                        if phone:
                            phone=phone.replace(' ', "")
                        if self.sms.GetValue() == "":
                            wx.MessageBox("Please write a message to send", "Error", wx.ICON_ERROR)
                            return
                        lists.append((name, phone, "waiting", str(self.sms.GetValue()), tday))
                    else:
                        phone = (selected[item]['Phone'])
                        name = (selected[item]['Name'])
                        if phone:
                            phone = phone.replace(' ', "")
                        if self.sms.GetValue() == "":
                            wx.MessageBox("Please write a message to send", "Error", wx.ICON_ERROR)
                            return
                        lists.append((name, phone, "waiting", str(self.sms.GetValue()), tday))
                    looker = True                    
                except IOError:
                        wx.MessageBox("Draft " + self.type + " " + "cannot be found", "Error", wx.ICON_ERROR)
                        break
                item += 1        
            if looker:
                if len(lists) == 1:
                    message = "One message has been queued"
                else:
                    message = "%d messages have been queued" % len(lists)
                busy = PBI.PyBusyInfo(message, parent=None, title="Server Request..")
                wx.Yield()
                sleep(5)
                del busy
                server = ServerAccess(lists)
                server.send_message()
            else:
                return wx.MessageBox("Please select recipients!", "Value Error", wx.ICON_ERROR)
        else:
            if not looker:
                return wx.MessageBox("Please select recipients!", "Value Error", wx.ICON_ERROR)

    def _imagePath(self, imageFile):
        return os.path.join(os.getcwd(), "images", imageFile)
    
    @staticmethod
    def insert_comma(arg):
        if isinstance(arg, float):
            arg = int(round(arg))
        arg = str(arg)
        counter = 0
        new_string = ""
        for number in enumerate(arg):
            if counter in [3, 6, 9, 12, 15]:
                if len(arg) > counter:
                    value = "," + arg[-(number[0] + 1)]
                else:
                    value = ""
                counter = 1
            else:
                value = arg[-(number[0] + 1)]
                counter += 1
            new_string += value
        return "".join(reversed(str(new_string)))

    def OnCalSelected1(self, evt):
        newlist = list()
        self.From.PopDown()
        date = self.cal1.GetDate()
        self.From.SetValue('%02d/%02d/%04d' % (date.GetDay(),
                                          date.GetMonth()+1,
                                          date.GetYear()))
        evt.Skip()       
        if date.IsValid():
            ymd = map(int, date.FormatISODate().split('-'))
            date = datetime.date(*ymd)
        counter = 0
        for i in self.packages:
            try:
                if i["To"].date() > date:
                    newlist.append(i)                
                counter += 1
            except:
                pass
                
        self.list.SetObjects(newlist)
        self.list.RepopulateList()

    def OnCalSelected2(self,evt):
        one_day = datetime.timedelta(days=1)
        self.To.PopDown()
        date1 = self.cal1.GetDate()
        date2 = self.cal2.GetDate()
        newlist = list()
        self.To.SetValue('%02d/%02d/%04d' % (date2.GetDay(),
                                          date2.GetMonth()+1,
                                          date2.GetYear()))
        evt.Skip()        
        if date2.IsValid() and date2.IsValid():
            ymd1 = map(int, date1.FormatISODate().split('-'))
            ymd2 = map(int, date2.FormatISODate().split('-'))
            date1 = datetime.date(*ymd1)
            date2 = datetime.date(*ymd2)
            date2 += one_day

        for i in self.packages:
            try:
                if i["To"].date() > date1 and i["To"].date() < date2:
                    newlist.append(i)
            except:
                pass
        self.list.SetObjects(newlist)
        self.list.RepopulateList()
        
        
class Letter(wx.Frame):
    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, -1, title, pos, size, style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW)
        Messages(self, "balance")

app = wx.App()
try:
    reactor.registerWxApp(app)
except:
    pass
if __name__ == '__main__':
    frame = Letter("Messages", (200, 100), (960, 500))
    frame.Show()
app.MainLoop()
