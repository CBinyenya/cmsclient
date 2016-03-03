import os
import wx 
import wx.wizard
import cPickle as pickle
from twisted.internet import wxreactor
try:
    wxreactor.install()
except:
    pass
from ObjectListView import ObjectListView, ColumnDefn
from ObjectListView import Filter
from functions import Datahandler, PhoneNumber
from serverManager import ServerAccess


class UserDetailsClass(wx.wizard.WizardPageSimple):
    def __init__(self, parent, title):
        self.func = Datahandler()
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)               
        self.SetSizer(self.sizer)                           
        titleText = wx.StaticText(self, -1, title)          
        titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
# -----------------------------------------------------------
        '''Panel content'''

        nameLbl = wx.StaticText(self, -1, "First Name:")
        self.fname = wx.TextCtrl(self, -1, "", size=(80, 22))
        nameLb3 = wx.StaticText(self, -1, "Last Name:")
        self.lname = wx.TextCtrl(self, -1, "")
        nameLb4 = wx.StaticText(self, -1, "Phone Number:")
        self.phone = wx.TextCtrl(self, -1, "")
        nameLb5 = wx.StaticText(self, -1, "Email:")
        self.email = wx.TextCtrl(self, -1, "")
        nameLb6 = wx.StaticText(self, -1, "Address :")
        self.address = wx.TextCtrl(self, -1, "")
        nameLb7 = wx.StaticText(self, -1, "City :")
        self.city = wx.TextCtrl(self, -1, "")
        nameLb8 = wx.StaticText(self, -1, "Group:")
        self.name8 = wx.Choice(self, -1, choices=[], size=(270, -1))
        save = wx.Button(self, -1, "Save")
        self.refresh_button = wx.Button(self, -1, "Refresh List")

        self.Bind(wx.EVT_BUTTON, self.OnSave, save)
        
        addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addrSizer.AddGrowableCol(1)
        addrSizer.Add(nameLbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.fname, 0, wx.EXPAND)
        
        addrSizer.Add(nameLb3, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.lname, 0, wx.EXPAND)

        addrSizer.Add(nameLb4, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.phone, 0, wx.EXPAND)
        addrSizer.Add(nameLb5, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.email, 0, wx.EXPAND)
        addrSizer.Add(nameLb6, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.address, 0, wx.EXPAND)
        addrSizer.Add(nameLb7, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.city, 0, wx.EXPAND)
        addrSizer.Add(nameLb8, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.name8, 0, wx.EXPAND)        
        addrSizer.Add(save, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.refresh_button, 0, wx.EXPAND)
       
        self.Bind(wx.EVT_BUTTON, self.OnSave, save)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.refresh_button)
        
        border = wx.BoxSizer()
        border.Add(addrSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(border)
        self.initialize()

    def initialize(self):
        groups = self.func.get_groups()
        print self.name8.AppendItems(groups)
        self.Refresh()

    def OnSave(self, evt):
        groupname = self.name8.GetStringSelection()
        if not self.fname.GetValue() or not self.phone.GetValue():
            wx.MessageBox("'First Name' and 'Phone number' must be filled", "Value Error", wx.ICON_ERROR)
            return
        if not groupname:
            wx.MessageBox("Please select a group to insert new member", "Value Error", wx.ICON_ERROR)
            return
        
        dlg = wx.MessageBox("Do you want to add this member?", "Confirmation", wx.ICON_INFORMATION | wx.YES_NO)
        if dlg == wx.NO:
            return
        newlist = []
        label = self.fname, self.lname, self.phone, self.email, self.address
        for i in label:            
            newlist.append(str(i.GetValue()))
        newlist.append(str(groupname))
        server = ServerAccess(newlist)
        server.add_group_member()
        return

    def OnRefresh(self, evt):
        self.name8.Clear()
        server = ServerAccess()
        server.get_appfiles()
        groups = self.func.get_groups()
        self.name8.AppendItems(groups)
        self.Refresh()


        
class GroupClass(wx.wizard.WizardPageSimple): 
    def __init__(self, parent, title):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.font = wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.font2 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)               
        self.SetSizer(self.sizer)                           
        titleText = wx.StaticText(self, -1, title)          
        titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)

        nameLbl = wx.StaticText(self, -1, "Group Name:")
        self.name1 = wx.TextCtrl(self, -1, "", size=(300,22))
        save = wx.Button(self, -1, "Save Group")
        
        addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addrSizer.AddGrowableCol(1)
        addrSizer.Add(nameLbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.name1, 0, wx.EXPAND)
        addrSizer.Add(save, 5, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.OnSave, save)
        
        border = wx.BoxSizer()
        border.Add(addrSizer, 1, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(border)

    def OnSave(self, evt):
        name = self.name1.GetValue()
        if name == "":
            return wx.MessageBox("Empty Field","Value Error",wx.ICON_ERROR)
        dlg = wx.MessageBox("Do you want to add this group", "Confirmation", wx.ICON_INFORMATION | wx.YES_NO)
        if dlg == wx.YES:
            server = ServerAccess(name)
            server.add_group()
        
class ManageUsers(wx.wizard.WizardPageSimple): 
    def __init__(self, parent, title):                      
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.func = Datahandler()
        self.font = wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.font2 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)                           
        titleText = wx.StaticText(self, -1, title)          
        titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        
        self.search = wx.SearchCtrl(self, size=(200,-1), style=wx.TE_PROCESS_ENTER)
        self.search.SetFont(self.font)
        image = os.path.join(os.getcwd(), "images", "user16.png")
        self.list = ObjectListView(self, wx.ID_ANY,size=(400,100), style=wx.LC_REPORT|wx.SUNKEN_BORDER)        
        userImageIndex = self.list.AddNamedImages("music", image)
        self.list.SetColumns([
                ColumnDefn("Name", "left", 200, "Name", autoCompleteCellEditor=True, imageGetter=userImageIndex),
                ColumnDefn("Phone", "left", 150, "Phone", isSpaceFilling=True),
                ColumnDefn("Group", "left", 50, "Group", isSpaceFilling=True)
            ])
        self.selectall = wx.Button(self, -1, "Select All")
        self.selectall.SetFont(self.font)
        self.deselectall = wx.Button(self, -1, "Deselect All")
        self.deselectall.SetFont(self.font)
        self.refresh_button = wx.Button(self, -1, "Refresh List")
        self.delete = wx.Button(self, -1, "Delete")

        glabel = wx.StaticText(self, -1, "Group:")
        self.groups = wx.Choice(self, -1, choices=[], size=(270, -1))
        self.deleteGroup = wx.Button(self, -1, "Delete Group")

        boxsizer.Add(self.search)
        boxsizer.Add(self.selectall)
        boxsizer.Add(self.deselectall)   
        addrSizer = wx.FlexGridSizer(cols=1, hgap=5, vgap=5)        
        addrSizer.Add(boxsizer, 0, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.list, 0, wx.ALIGN_CENTER_VERTICAL)
        
        boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        boxsizer.Add(self.refresh_button, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        boxsizer.Add(self.delete, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        addrSizer.Add(boxsizer, 0, wx.ALIGN_CENTER_VERTICAL)

        boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        boxsizer.Add(glabel, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        boxsizer.Add(self.groups, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        addrSizer.Add(boxsizer, 0, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.deleteGroup, 0, wx.ALIGN_CENTER_VERTICAL)

        self.Bind(wx.EVT_BUTTON, self.OnSelectaAll, self.selectall)
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, self.deselectall)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, self.delete)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.refresh_button)
        self.Bind(wx.EVT_BUTTON, self.OnDeleteGroup, self.deleteGroup)
        border = wx.BoxSizer()
        border.Add(addrSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(border)
        self.InitSearchCtrls()
        self.initialize()

    def initialize(self):
        groups = self.func.get_groups()
        self.groups.AppendItems(groups)
        members = self.func.get_group_members()
        self.list.SetObjects(members)
        self.list.RepopulateList()
        self.Refresh()

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
        self.groups.Refresh()
        members = self.func.get_group_members()
        self.list.SetObjects(members)
        self.list.RepopulateList()
        
    def OnRefresh(self, evt):
        self._refresh()

    def OnDeleteGroup(self, evt):
        name = self.groups.GetStringSelection()
        if not name:
            wx.MessageBox("No group has been selected", "Value Error", wx.ICON_ERROR)
            return            
        dlg = wx.MessageBox("Deleting this group will delete all its members", "WARNING", wx.ICON_WARNING | wx.YES_NO)
        if dlg == wx.YES:
            server = ServerAccess(name)
            server.delete_group()

    def OnDelete(self , evt):
        selected = self.list.GetSelectedObjects()        
        if len(selected) > 0:            
            item = 0
            last = len(selected) 
            for i in range(0, last):
                phn = selected[item]['Phone']
                server = ServerAccess(phn)
                server.delete_group_member()
                item += 1
        else:
            wx.MessageBox("No member selected", "Value Error", wx.ICON_ERROR)
            return
        self._refresh()
        return

# ----------------------------------------------------------

def runDialogue():
    app = wx.App()
    wizard = wx.wizard.Wizard(None, -1, "Groups Panel")
    page1 = GroupClass(wizard, "New Group")
    page2 = UserDetailsClass(wizard, "Member Details")
    page3 = ManageUsers(wizard, "Manage Group Members")
    page1.sizer.Add(wx.StaticText(page1, -1, 
            "Please fill all the fields")) 
    wx.wizard.WizardPageSimple_Chain(page1, page2)
    wx.wizard.WizardPageSimple_Chain(page2, page3)
    wizard.FitToPage(page1)   
    if wizard.RunWizard(page1):   
        pass
    app.MainLoop()
if __name__ == "__main__":
    runDialogue()
