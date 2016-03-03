import wx
import os
import sys
import time
import string
from threading import Thread
import cPickle as pickle
from twisted.internet import reactor
from twisted.cred import credentials
import wx.lib.agw.pybusyinfo as PBI
import  wx.lib.popupctl as  pop
import  wx.calendar as wxcal
from ObjectListView import ObjectListView, ColumnDefn
from ObjectListView import Filter
from time import clock

from functions import GroupClassFunctions
import generate as gn
import printer
klass = GroupClassFunctions()
flags = [(wx.ICON_INFORMATION, "ICON_INFORMATION")]
from serverManager import classClient
def informer(message,delay=0,title = "Creation Process"):    
    busy = PBI.PyBusyInfo(message, parent=None, title=title)
    time.sleep(delay)
    wx.Yield()
    del busy


class Letters( wx.Panel,pop.PopupControl) :
    def __init__(self, parent, Type):
        wx.Panel.__init__(self, parent=parent,size=(400,400))
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.type = Type        
        self.font=wx.Font(10,wx.DECORATIVE,wx.NORMAL,wx.NORMAL);self.font2=wx.Font(12,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)  
        gps = klass.get_group_names("groups")
        label1 =wx.StaticText(self,-1,"Groups");label1.SetFont(self.font2)
        
        self.groups = wx.Choice(self, -1,choices=gps, size=(270, -1));self.groups.SetFont(self.font)
        if self.type =="quicktxt":
            hsbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Category'), orient=wx.HORIZONTAL)
            msg = ""
        elif self.type =="general":
            hsbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Category'), orient=wx.HORIZONTAL)
            self.members = klass.get_group_clients("all")
            msg = ""
            
        else:
            pass
        
        self.info = wx.InfoBar(self)    
        action = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Action Panel'), orient=wx.VERTICAL)
        self.search = wx.SearchCtrl(self, size=(200,-1), style=wx.TE_PROCESS_ENTER);self.search.SetFont(self.font)
        
        self.selectall = wx.Button(self,-1,"Select All");self.selectall.SetFont(self.font)        
        self.sms = wx.TextCtrl(self, -1, msg, style=wx.TE_MULTILINE,size=(500,74));self.sms.SetFont(self.font)
        self.createEnv = wx.Button(self, 101, "Create Letters");self.createEnv.SetFont(self.font)
        self.createLet = wx.Button(self, 102, "Create Envelopes");self.createLet.SetFont(self.font)        
        self.Bind(wx.EVT_CHOICE,self.OnGroup,self.groups)
        
        
        if Type == "quicktxt":
            self.list = ObjectListView(self, wx.ID_ANY,size=(510,100), style=wx.LC_REPORT|wx.SUNKEN_BORDER)        
            userImageIndex = self.list.AddNamedImages("music", self._imagePath("user16.png"))
            self.list.SetColumns([
                ColumnDefn("Name", "left",200,"Name",autoCompleteCellEditor=True,imageGetter=userImageIndex),
                ColumnDefn("Address", "left", 150, "Address", isSpaceFilling=True),
                ColumnDefn("Group", "left", 50, "Group", isSpaceFilling=True),
                ColumnDefn("City", "left", 100, "City", isSpaceFilling=True)              
                
            ])            
        else:            
            self.list = ObjectListView(self, wx.ID_ANY,size=(900,230), style=wx.LC_REPORT|wx.SUNKEN_BORDER)        
            userImageIndex = self.list.AddNamedImages("music", self._imagePath("user16.png"))        
            self.list.SetColumns([
                ColumnDefn("Name", "left",200,"Name",autoCompleteCellEditor=True,imageGetter=userImageIndex ,isSpaceFilling=True),
                ColumnDefn("Address", "left", 150, "Address", isSpaceFilling=True,checkStateGetter = "isActive"),
                ColumnDefn("Group", "left", 50, "Group", isSpaceFilling=True),
                ColumnDefn("City", "left", 100, "City", isSpaceFilling=True)              
                
            ])          
            
        self.list.SetFont(self.font)
        if self.type == "quicktxt":
            self.list.SetObjects(None)
        else:self.list.SetObjects(self.members)
        self.Bind(wx.EVT_BUTTON, self.OnSelectaAll,self.selectall)        
        self.Bind(wx.EVT_BUTTON, self.OnCreate,id = 101)
        self.Bind(wx.EVT_BUTTON, self.OnCreate,id=102)        
        
#=======LAYOUT MANAGEMENT=========================================================================================
        hsbox1 = wx.BoxSizer(wx.VERTICAL);hsbox2 = wx.BoxSizer(wx.VERTICAL);hsbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox.Add(label1,0,wx.ALIGN_LEFT|wx.ALL,5);hsbox.Add(self.groups,0,wx.ALIGN_LEFT|wx.ALL,5)
        hsbox4 = wx.BoxSizer(wx.HORIZONTAL)
        if Type == "quicktxt":
            pass
        else:pass
        hsbox.Add(hsbox2)
        hsbox3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        hsbox3Sizer.Add(self.selectall,0,wx.ALIGN_RIGHT|wx.ALL,10)
        hsbox3Sizer.Add(self.search,0,wx.ALIGN_BOTTOM|wx.ALL,10)

        hsbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox4.Add(self.createEnv,0,wx.ALIGN_LEFT|wx.ALL,4);hsbox4.Add(self.createLet,0,wx.ALIGN_LEFT|wx.ALL,4)
        action.Add(self.sms,0,wx.ALIGN_LEFT|wx.ALL,4)
        action.Add(hsbox4,0,wx.ALIGN_LEFT|wx.ALL,4) 

        
        sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridBagSizer(hgap=50, vgap=5)
        sizer.Add(self.info,0,wx.EXPAND)
        grid_sizer.Add(hsbox,pos=(0,0));grid_sizer.Add(action,pos=(0,1),span=(1,2))
        grid_sizer.Add(hsbox3Sizer,pos=(1,0),span=(1,2))
        grid_sizer.Add(self.list,pos=(2,0),span=(1,2))
        sizer.Add(grid_sizer,0,wx.ALIGN_LEFT|wx.ALL,10)
        self.SetSizer(sizer)
        self.GetSizer().Layout()
        self.InitSearchCtrls()
        
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
        if self.type == "quicktxt":
            if searchCtrl.GetValue() == "":
                self.list.SetObjects(None)
            else:
                self.packages = klass.search_group_clients(searchCtrl.GetValue(),"motphone")            
                self.list.SetObjects(self.packages)
                self.list.RepopulateList()           
        else:     
            olv.GetFilter().SetText(searchCtrl.GetValue())
            olv.RepopulateList()
        
        
    def OnCancelSearchCtrl(self, event, searchCtrl, olv):
        searchCtrl.SetValue("")
        self.OnTextSearchCtrl(event, searchCtrl, olv)
    def OnDoSearch(self , value):
        self.list.GetFilter().SetText(value)
        self.list.RepopulateList()
    def OnGroup(self, evt):
        clients=klass.get_group_clients(self.groups.GetStringSelection())
        self.list.SetObjects(clients)
        self.list.RepopulateList()           
    def OnTowns(self,event):        
        if self.selected:
            self.OnDoSearch(self.towns.GetStringSelection())
            return
        if self.selAll.IsChecked() == 1:
            self.selected = True
            self.packages = fun2.fun_get_clients_by_location(self.towns.GetStringSelection())
            self.list.SetObjects(None)
            self.list.SetObjects(self.packages)
            self.list.RepopulateList()
            self.list.SetEmptyListMsg("No inactive Clients")
            return                
        self.OnDoSearch(self.towns.GetStringSelection())
    def OnSelectaAll(self, olv):
        label = self.selectall.GetLabel()
        if label == "Select All":
            self.list.SelectAll()
            self.selectall.SetLabel("Deselect All")
        else:
            self.list.DeselectAll()
            self.selectall.SetLabel("Select All")

    def OnclearSms(self,evt):
        self.sms.Clear()
    def OnCreate(self , evt):
        identity= evt.GetId()
        if identity == 101:
            dtails = []
        else:
            with open("bin/compdetails","rb") as newfile:
                appinfo = pickle.load(newfile)
            dtails = [appinfo["Name:"],appinfo["return"]]            
        selected = self.list.GetSelectedObjects()
        if len(selected) < 2:
            selected = self.list.GetCheckedObjects()            
        if len(selected) > 0:
            looker = False;lists = []
            item = 0
            last = len(selected) 
            for i in range(0,last):                
                try:
                    name,loc = (selected[item]['Name']),(selected[item]['City'])                         
                    address = (selected[item]['Address'])
                    collect = ("general_let.docx",(str(name),str(address),str(loc)),dtails)
                    if name and loc and address:
                        lists.append(collect)
                    looker = True                    
                except IOError,e:
                        wx.MessageBox("Draft "+let+" "+"cannot be found")
                        
                item += 1        
            if looker == True:
                rem = len(lists)
                if rem == 0:
                    wx.MessageBox("One of important fieds is missing","Error",wx.ICON_ERROR)
                    return
                for i in lists:
                    try:
                        if identity == 102:
                            gn.creator("sample_env.docx",i[1],i[2])
                            rem = rem - 1
                            message = "%d envelopes remaining..."%(rem)
                            informer(message,0.1,"Creating Envelopes")                                                
                        else:
                            gn.creator(i[0],i[1],i[2])
                            rem = rem - 1
                            message = "%d Letters remaining..."%(rem)                            
                            informer(message,0.1,"Creating Letters")                            
                    except:
                        print "Erro"
                        rem = rem - 1
                
                informer("Preparing the printing process...",2,"Printing Process")
                if identity == 102:
                    printer.printing("envelopes")                    
                else:                    
                    printer.printing("letters")
                    
            else:
                wx.MessageBox("Please select reciepints!","Value Error",wx.ICON_ERROR)
            return
        else:
            wx.MessageBox("Please select reciepints!","Value Error",wx.ICON_ERROR)
        

        

    def _imagePath(self, imageFile):
        return os.path.join(os.getcwd(), "images", imageFile)
class Letter(wx.Frame):
    def __init__(self,title,pos,size):
        wx.Frame.__init__(self,None,-1,title,pos,size,style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW)
        Letters(self,"general")
if __name__ == '__main__':
    app = wx.App(False)
    frame = Letter("Messages",(200,100),(960,500))
    frame.Show()
    app.MainLoop()

