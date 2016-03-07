import os
import wx 
import wx.wizard
import cPickle as pickle
from ObjectListView import ObjectListView, ColumnDefn
from ObjectListView import Filter
from twisted.internet import reactor
from twisted.cred import credentials
from serverManager import Administration
from serverManager import ServerAccess
from functions import Datahandler


class UserDetailsClass(wx.wizard.WizardPageSimple): 
    def __init__(self, parent, title):                      
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)               
        self.SetSizer(self.sizer)                           
        titleText = wx.StaticText(self, -1, title)          
        titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))  
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)        
# -----------------------------------------------------------
        '''Panel content'''

        nameLbl = wx.StaticText(self, -1, "User name:")
        self.user_name = wx.TextCtrl(self, -1, "", size=(80, 22))
        nameLb2 = wx.StaticText(self, -1, "First Name:")
        self.fname = wx.TextCtrl(self, -1, "", size=(80, 22))       
        nameLb3 = wx.StaticText(self, -1, "Last Name:")
        self.lname = wx.TextCtrl(self, -1, "")
        nameLb4 = wx.StaticText(self, -1, "Phone Number:")
        self.phone_no = wx.TextCtrl(self, -1, "")
        nameLb5 = wx.StaticText(self, -1, "Password: ")
        self.password1 = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        nameLb6 = wx.StaticText(self, -1, "Confirm Password: ")
        self.password2 = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        save = wx.Button(self, -1, "Save", size=(270, 30))
        
        addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addrSizer.AddGrowableCol(1)
        addrSizer.Add(nameLbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.user_name, 0, wx.EXPAND)
        
        addrSizer.Add(nameLb2, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.fname, 0, wx.EXPAND)
        addrSizer.Add(nameLb3, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.lname, 0, wx.EXPAND)

        addrSizer.Add(nameLb4, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.phone_no, 0, wx.EXPAND)
        addrSizer.Add(nameLb5, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.password1, 0, wx.EXPAND)
        addrSizer.Add(nameLb6, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.password2, 0, wx.EXPAND)        
        addrSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(save, 0, wx.EXPAND)
       
        self.Bind(wx.EVT_BUTTON, self.on_save, save)
        
        border = wx.BoxSizer()
        border.Add(addrSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(border)
        
    def on_save(self, evt):
        details_list = []
        label = self.user_name, self.password1, self.fname, self.lname, self.phone_no, self.password2
        for i in label:
            if i.GetValue() == "":
                return wx.MessageBox("Please fill in all the fields", "Value Error", wx.ICON_ERROR)
                
            details_list.append(i.GetValue())
        if self.password1.GetValue() != self.password2.GetValue():
            return wx.MessageBox("Password does not match!", "Password Error", wx.ICON_ERROR)
        
        dlg = wx.MessageBox("Do you want to create account for this User?", "Confirmation",
                            wx.ICON_INFORMATION | wx.YES_NO)
        if dlg == wx.YES:                
            server = ServerAccess(details_list)
            server.add_user()
            
    def on_refresh(self, evt):
        pass
    
        
class ManageUsers(wx.wizard.WizardPageSimple): 
    def __init__(self, parent, title):                      
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.func = Datahandler()
        self.font=wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.font2=wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)                           
        titleText = wx.StaticText(self, -1, title)          
        titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        
        self.search = wx.SearchCtrl(self, size=(200,-1), style=wx.TE_PROCESS_ENTER)
        self.search.SetFont(self.font)
        image=os.path.join(os.getcwd(), "images", "user16.png")
        self.list = ObjectListView(self, wx.ID_ANY,size=(400,150), style=wx.LC_REPORT|wx.SUNKEN_BORDER)        
        userImageIndex = self.list.AddNamedImages("music", image)
        self.list.SetColumns([
                ColumnDefn("Username", "left", 130, "username", autoCompleteCellEditor=True, imageGetter=userImageIndex),
                ColumnDefn("User", "left", 75, "fname", isSpaceFilling=True),
                ColumnDefn("Other", "left", 75, "lname", isSpaceFilling=True),
        ])

        self.list.SetEmptyListMsg("No Accounts Available")              
        self.selectall = wx.Button(self, -1, "Select All")
        self.selectall.SetFont(self.font)
        self.deselectall = wx.Button(self, -1, "Deselect All")
        self.deselectall.SetFont(self.font)
        self.refresh = wx.Button(self, -1, "Refresh List")
        self.delete = wx.Button(self, -1, "Delete")

        boxsizer.Add(self.search);boxsizer.Add(self.selectall)
        boxsizer.Add(self.deselectall)   
        addrSizer = wx.FlexGridSizer(cols=1, hgap=5, vgap=5)        
        addrSizer.Add(boxsizer, 0, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.list, 0, wx.ALIGN_CENTER_VERTICAL)
        
        boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        boxsizer.Add(self.refresh, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        boxsizer.Add(self.delete, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        addrSizer.Add(boxsizer, 0, wx.ALIGN_CENTER_VERTICAL)

        self.Bind(wx.EVT_BUTTON, self.OnSelectaAll, self.selectall)
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, self.deselectall)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, self.delete)
        border = wx.BoxSizer()
        border.Add(addrSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(border)
        self._init()
        self.InitSearchCtrls()
        self.initialize()

    def initialize(self):
        members = self.func.get_users()
        self.list.SetObjects(members)
        self.list.RepopulateList()

    def OnSelectaAll(self, olv):
        self.list.SelectAll()

    def OnDeselectAll(self, olv):
        self.list.DeselectAll()        
    
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
        olv.GetFilter().SetText(searchCtrl.GetValue())
        olv.RepopulateList()
        
    def OnCancelSearchCtrl(self, event, searchCtrl, olv):
        searchCtrl.SetValue("")
        self.OnTextSearchCtrl(event, searchCtrl, olv)

    def OnDoSearch(self, value):
        self.list.GetFilter().SetText(value)
        self.list.RepopulateList()

    def _refresh(self):
        pass
        
    def on_refresh(self, evt):
        self._refresh()

    def OnDelete(self, evt):
        objects = self.list.GetObjects()
        selected = self.list.GetSelectedObjects()
        if len(selected) > 0:            
            item = 0
            last = len(selected)
            dlg = wx.MessageBox("Do you want to delete this user(s) User?", "Confirmation",
                                wx.ICON_INFORMATION | wx.YES_NO)
            if dlg == wx.NO:
                return
            for i in range(0, last):
                name = selected[item]['username']
                creds = credentials.UsernamePassword(self._user()[0],self._user()[1])
                classs = Administration(creds,"delete user",name)                            
                classs.runEngine()
                try:
                    reactor.run()
                except:
                    pass      
            
                item += 1
        else:
            return wx.MessageBox("No user has been selected", "Value Error", wx.ICON_ERROR)
        self._refresh()
        
    def _user(self):
        with open("appfiles/authorization.dat","rb") as confidential:            
            details = pickle.load(confidential)
            if not details:
                wx.MessageBox("User Details unavailable","AUTHENTIFICATION ERROR",wx.ICON_ERROR)                        
            for user,passwd in details.items():
                username = user
                password = passwd
            return username, password

    def _init(self):
        try:
            with open("bin/admin/allusers.dat","rb") as newfile:
                data = pickle.load(newfile)
        except IOError, e:
            return
        for i in data:
            print i
        self.list.SetObjects(data)


def runAccounts():
    app = wx.App()
    wizard = wx.wizard.Wizard(None, -1, "User Accounts Panel")
    
    page1 = UserDetailsClass(wizard, "Create Account")
    page2 = ManageUsers(wizard, "Manage User Accounts")
    page1.sizer.Add(wx.StaticText(page1, -1, "Please fill all the fields"))
    wx.wizard.WizardPageSimple_Chain(page1, page2)
    
    wizard.FitToPage(page1)   
    if wizard.RunWizard(page1):   
        pass
    app.MainLoop()
if __name__ == "__main__":
    runAccounts()
