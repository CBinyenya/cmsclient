import os
import wx
import time
import math
import datetime
import threading
import cPickle as pickle
from twisted.internet import reactor
from twisted.cred import credentials
from serverManager import Administration
from ObjectListView import ObjectListView, ColumnDefn
from ObjectListView import Filter
class AuditPanel(wx.Notebook):
    def __init__(self, parent, id=-1):
        wx.Notebook.__init__(self, parent, id=-1,  style= wx.BK_DEFAULT)
        self.Email()

    def Email(self):
        pass

class SimpleLog( wx.Panel ) :
    def __init__(self, parent, id, pos=wx.DefaultPosition, size=(600,200),
                 style=wx.NO_BORDER | wx.TAB_TRAVERSAL):        
        wx.Panel.__init__(self, parent, id, pos, size, style)
        self.font=wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)  
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.months=["January","February","March","April","May","June","July","August","September","October","November","December"]        
        self.Day=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        self.font1=wx.Font(14,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        self.font2=wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        self.Day_ = wx.StaticText(self, -1,"Day");self.Day_.SetFont(self.font2)
        self.Day = wx.ComboBox(self, wx.ID_ANY,"Day",(15,20), (150,-1),self.Day, 0)
        self.MonthName1_ = wx.StaticText(self, -1,"Month");self.MonthName1_.SetFont(self.font2)       
        self.Month = wx.ComboBox(self, wx.ID_ANY,"January",(15,20), (150,-1),self.months, 0)
        self.refresh = wx.Button(self, -1, "Refresh")
        
        self.search = wx.SearchCtrl(self, size=(200,-1), style=wx.TE_PROCESS_ENTER);self.search.SetFont(self.font)
        imgpath = os.path.join(os.getcwd(), "images", "process.png")
        self.list = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER,size=(600,700))
        userImageIndex = self.list.AddNamedImages("user", imgpath)        
        self.list.SetColumns([
            ColumnDefn("Time", "left",100,"Time",autoCompleteCellEditor=True,imageGetter=userImageIndex ,isSpaceFilling=True),
            ColumnDefn("User", "left", 50, "User", isSpaceFilling=True),
            ColumnDefn("Task", "left", 450, "Task", isSpaceFilling=True),
            
        ])
        self.list.SetObjects(self.get_logs())
        self.list.SetEmptyListMsg("There are no records ")
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.refresh)
        self.Bind(wx.EVT_COMBOBOX, self.OnDay , self.Day)
        self.Bind(wx.EVT_COMBOBOX, self.OnMonth , self.Month)

        self.layout()
        self.GetSizer().Layout()

    def layout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL);hsbox1 = wx.BoxSizer(wx.HORIZONTAL);hsbox = wx.BoxSizer(wx.VERTICAL)
        hsbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox1.Add(self.Day_, 0, wx.ALIGN_LEFT|wx.ALL, 5);hsbox1.Add(self.Day, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        hsbox1.Add(self.MonthName1_, 0, wx.ALIGN_LEFT|wx.ALL, 5);hsbox1.Add(self.Month, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        hsbox1.Add(self.refresh, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        hsbox2.Add(self.search, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        
        hsbox.Add(hsbox1);hsbox.Add(hsbox2);hsbox.Add(self.list)
        sizer.Add(hsbox)
        self.SetSizer(sizer)
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
        olv.GetFilter().SetText(searchCtrl.GetValue())
        olv.RepopulateList()    
        
    def OnCancelSearchCtrl(self, event, searchCtrl, olv):
        searchCtrl.SetValue("")
        self.OnTextSearchCtrl(event, searchCtrl, olv)

    def get_logs(self):
        with open("bin/admin/audit.dat","rb") as newfile:
            data = pickle.load(newfile)
        return data
    def OnRefresh(self, evt):
        condition = threading.Condition()        
        th1 = threading.Thread(name="Audit locator",target=self.data_handler,
                                args = (condition,))
        th2 = threading.Thread(name="Audit collector",target=self.data_collector,
                                args = (condition,))
        th2.start()
        th1.start()
    def returnday(self,day):        
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        for i in enumerate(days):
            if i[1] == day:
                return i[0]

    def OnDay(self, evt):
        choice = self.Day.GetValue()
        tday  = time.ctime()[:3]        
        span = self.returnday(tday) - self.returnday(choice[:3])
        if span < 0:
            wx.MessageBox("Logs for %s are not available"%choice,"INVALID CHOICE",wx.ICON_ERROR)
            return
        span = int(math.fabs(span))
        tday = datetime.date.today()
        date_span = datetime.timedelta(days=span)
        the_day = tday - date_span
        tdate = str(the_day)[-2:]        
        data = self.get_logs()
        newlist = []
        for every in data:
            if every["Time"][:2] == tdate:
                newlist.append(every)
        self.list.SetObjects(newlist)
    def OnMonth(self, evt):
        choice = self.Month.GetValue()
        data = self.get_logs()
        newlist = []
        for every in data:            
            if every["Time"][3:6] == choice[:3]:
                newlist.append(every)
        self.list.SetObjects(newlist)
                
    def data_handler(self,cond):
        with cond:                        
            try:
                with open("appfiles/authorization.dat","rb") as confidential:            
                    details = pickle.load(confidential)
                    if not details:
                        wx.MessageBox("You are not Authorized to Access this files!","ACCESS ERROR",wx.ICON_ERROR)                        
                    for user,passwd in details.items():
                        username = user
                        password = passwd
            except:
                return
            
            creds = credentials.UsernamePassword(username, password)        
            classs = Administration(creds,"audit trail","dictionary")
            classs.runEngine()
            try:
                reactor.run()
            except:
                pass
            cond.notifyAll()
    def data_collector(self,cond):
        with cond:
            time.sleep(2)        
            cond.wait()        
            data = self.get_logs()            
            self.list.SetObjects(data)
            wx.MessageBox("Update")
                
            
                
    def EvtChoice(self, evt):
        DeptName=self.Day.GetStringSelection()
        self.Month.Clear()
        for i in fun.retvMonthName(DeptName):
            self.Month.Append(i)     
class MainFrame(wx.Frame):
    def __init__(self,title,pos,size):
        wx.Frame.__init__(self,None,-1,title,pos,size,style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW)
        SimpleLog(self,wx.ID_ANY)
        
if __name__ == '__main__':
    class MyApp(wx.App):
        def OnInit(self):
            frame =MainFrame("Mainframe",(200,100),(600,500))
            frame.Show(True)
            self.SetTopWindow(frame)
            return True


    app = MyApp(False)
    app.MainLoop()


