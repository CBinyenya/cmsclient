__author__ = 'Monte'
import os
import wx
import wx.lib.masked as masked
import wx.lib.popupctl as pop
import wx.calendar as wxcal
from ObjectListView import ObjectListView, ColumnDefn, Filter
from serverManager import ServerAccess
import datetime
import functions as fun


class ManageChequePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.banks = self.payee_list = list()

        self.search = wx.SearchCtrl(self, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        self.search.SetFont(self.font)

        image = os.path.join(os.getcwd(), "images", "user16.png")
        self.clients = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        userImageIndex = self.clients.AddNamedImages("music", image)
        self.clients.SetColumns([
            ColumnDefn("Name", "left", 200, "Name", autoCompleteCellEditor=True, imageGetter=userImageIndex),
            ColumnDefn("Number", "left", 100, "Number", isSpaceFilling=True),
            ColumnDefn("Type", "left", 100, "Type", isSpaceFilling=True),
            ColumnDefn("Payee", "left", 150, "Payee", isSpaceFilling=True),
            ColumnDefn("Bank", "left", 100, "Bank", isSpaceFilling=True),
            ColumnDefn("Due", "left", 150, "Due", isSpaceFilling=True),
            ColumnDefn("Amount", "left", 100, "Amount", isSpaceFilling=True),
        ])

        self.clients.SetEmptyListMsg("No clients available")

        name_label = wx.StaticText(self, -1, "NAME: ")
        name_label.SetFont(self.font)
        self.name = wx.StaticText(self, -1, size=(200, -1))
        self.name.SetFont(self.font)
        self.name.SetForegroundColour(wx.BLUE)

        cheque_no_label = wx.StaticText(self, -1, "CHEQUE NUMBER: ")
        cheque_no_label.SetFont(self.font)
        self.cheque_no = wx.StaticText(self, -1, size=(150, -1))
        self.cheque_no.SetFont(self.font)
        self.cheque_no.SetForegroundColour(wx.BLUE)

        type_label = wx.StaticText(self, -1, "CHEQUE TYPE: ")
        type_label.SetFont(self.font)

        self.cheque_type = wx.StaticText(self, -1)
        self.cheque_type.SetFont(self.font)
        self.cheque_type.SetForegroundColour(wx.BLUE)

        amount_label = wx.StaticText(self, -1, "Amount")
        amount_label.SetFont(self.font)
        self.amount = masked.NumCtrl(self, -1, size=(300, -1))
        self.amount.SetFont(self.font)

        insu_recpt_label = wx.StaticText(self, -1, "Insures Receipt")
        insu_recpt_label.SetFont(self.font)

        self.insu_recpt = wx.TextCtrl(self, -1, size=(300, -1))
        self.insu_recpt.SetFont(self.font)
        payee_label = wx.StaticText(self, -1, "Payee")
        payee_label.SetFont(self.font)
        self.payee = wx.Choice(self, -1, choices=self.payee_list, size=(300, -1))
        self.payee.Disable()
        self.payee.SetFont(self.font)
        due_date_label = wx.StaticText(self, -1, "Due Date")
        due_date_label.SetFont(self.font)
        self.due_date = pop.PopupControl(self, -1, size=(300, -1))
        win1 = wx.Window(self.due_date, -1, pos=(0, 0))
        self.cal = wxcal.CalendarCtrl(win1, -1, pos=(0, 0))
        bz = self.cal.GetBestSize()
        win1.SetSize(bz)
        self.due_date.SetPopupContent(win1)

        self.due_date.SetFont(self.font)
        kbima_receipt_label = wx.StaticText(self, -1, "K-BIMA Receipt")
        kbima_receipt_label.SetFont(self.font)
        self.kbima_receipt = wx.TextCtrl(self, -1, size=(300, -1))
        self.kbima_receipt.SetFont(self.font)
        kbima_payment_no_label = wx.StaticText(self, -1, "K-BIMA payment No.")
        kbima_payment_no_label.SetFont(self.font)
        self.kbima_payment_no = wx.TextCtrl(self, -1, size=(300, -1))
        self.kbima_payment_no.SetFont(self.font)
        bank_label = wx.StaticText(self, -1, "Bank")
        bank_label.SetFont(self.font)
        self.bank = wx.Choice(self, -1, choices=self.banks, size=(300, -1))
        self.bank.Disable()
        self.bank.SetFont(self.font)
        update = wx.Button(self, -1, "UPDATE")
        update.SetFont(self.font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.search, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sizer.Add(self.clients, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        subsizer = wx.GridBagSizer(vgap=10, hgap=5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(name_label, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(self.name, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(cheque_no_label, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(self.cheque_no, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(type_label, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(self.cheque_type, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        subsizer.Add(hbox, pos=(0, 0), span=(1, 4))

        subsizer.Add(amount_label, pos=(1, 0))
        subsizer.Add(self.amount, pos=(1, 1))

        subsizer.Add(insu_recpt_label,pos=(2, 0))
        subsizer.Add(self.insu_recpt, pos=(2, 1))

        subsizer.Add(payee_label, pos=(3, 0))
        subsizer.Add(self.payee, pos=(3, 1))

        subsizer.Add(due_date_label, pos=(4, 0))
        subsizer.Add(self.due_date, pos=(4, 1))

        subsizer.Add(kbima_receipt_label, pos=(5, 0))
        subsizer.Add(self.kbima_receipt, pos=(5, 1))

        subsizer.Add(kbima_payment_no_label, pos=(6, 0))
        subsizer.Add(self.kbima_payment_no, pos=(6, 1))

        subsizer.Add(bank_label, pos=(7, 0))
        subsizer.Add(self.bank, pos=(7, 1))

        subsizer.Add(update, pos=(8, 1), span=(1, 2))

        sizer.Add(subsizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        self.clients.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_select)
        self.cal.Bind(wxcal.EVT_CALENDAR, self.on_cal_selected)
        self.Bind(wx.EVT_BUTTON, self.on_update, update)

        self.SetSizer(sizer)
        self.InitSearchCtrls()
        self.initialize()

    def initialize(self):
        func = fun.Datahandler()
        clients = func.get_cheque()
        self.clients.SetObjects(clients)

    def InitSearchCtrls(self):
        for (searchCtrl, olv) in [(self.search, self.clients)]:
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

    def on_cal_selected(self, evt):
        self.due_date.PopDown()
        date_ = self.cal.GetDate()
        self.due_date.SetValue('%02d/%02d/%04d' % (date_.GetDay(), date_.GetMonth()+1, date_.GetYear()))
        evt.Skip()

    def on_select(self, evt):
        client = self.clients.GetSelectedObject()
        self.name.SetLabelText(client['Name'])
        self.cheque_no.SetLabelText(client['Number'])
        self.cheque_type.SetLabelText(client['Type'])
        self.amount.SetValue(client['Amount'])
        self.insu_recpt.SetValue(client['Recpt'])
        self.payee.SetStringSelection(client['Payee'])
        self.due_date.SetValue(client['Due'].strftime("%d-%b,%Y"))
        self.kbima_payment_no.SetValue(client['Kbimarecpt'])
        self.kbima_receipt.SetLabelText(client['Kbimarecpt'])
        self.bank.SetLabel(client['Bank'])

    def on_update(self, evt):
        client = self.clients.GetSelectedObject()
        date = self.cal.GetDate()
        if date.IsValid():
            dt = datetime.datetime.today()
            dt = dt.date()
            ymd = map(int, date.FormatISODate().split('-'))
            date = datetime.date(*ymd)
            if dt == date or date < dt:
                wx.MessageBox("Invalid date!", "Date Error", wx.ICON_ERROR)
                return

        new_dict = dict()
        list1 = [self.amount.GetValue(), self.insu_recpt.GetValue(), date, self.kbima_payment_no.GetValue(),
                 self.kbima_receipt.GetValue()]
        list2 = [client['Amount'], client['Recpt'], client['Due'].date(), client['Kbimarecpt'], client['Kbimarecpt']]
        list3 = ["amount", "insu_recpt", "due_date", "kbima_recpt", "kbima_recpt_no"]
        for value in enumerate(list1):
            if value[1] != list2[value[0]]:
                print value[1], list2[value[0]]
                new_dict[list3[value[0]]] = value[1]
        if new_dict:
            msg = "Do you want to update information for %s" % client['Name']
            dg = wx.MessageBox(msg, "Confirmation", wx.ICON_WARNING | wx.YES_NO)
            if dg == wx.YES:
                server = ServerAccess((client['Number'], new_dict))
                server.update_cheque()
        else:
            wx.MessageBox("No changes detected", "Information", wx.ICON_WARNING)
            return


class AddChequePanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.payee_list = self.banks = self.cheque_type_list = []
        self.initializer()
        self.search = wx.SearchCtrl(self, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        self.search.SetFont(self.font)

        image = os.path.join(os.getcwd(), "images", "user16.png")
        self.clients = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER, size=(450, 80))
        userImageIndex = self.clients.AddNamedImages("music", image)
        self.clients.SetColumns([
            ColumnDefn("Id", "left", 70, "Id", autoCompleteCellEditor=True, imageGetter=userImageIndex),
            ColumnDefn("Name", "left", 100, "Name", isSpaceFilling=True),
            ColumnDefn("Phone", "left", 150, "Phone", isSpaceFilling=True),
        ])
        self.clients.SetObjects(self.get_clients())
        self.clients.SetEmptyListMsg("No clients available")

        self.name = wx.TextCtrl(self, -1, size=(240, -1))
        self.name.SetFont(self.font)

        cheque_no_label = wx.StaticText(self, -1, "Cheque Number")
        cheque_no_label.SetFont(self.font)
        self.cheque_no = wx.TextCtrl(self, -1, size=(300, -1))
        self.cheque_no.SetFont(self.font)

        type_label = wx.StaticText(self, -1, "Cheque Type")
        type_label.SetFont(self.font)
        self.cheque_type = wx.Choice(self, -1, choices=self.cheque_type_list, size=(300, -1))
        self.cheque_type.SetFont(self.font)
        amount_label = wx.StaticText(self, -1, "Amount")
        amount_label.SetFont(self.font)
        self.amount = masked.NumCtrl(self, -1, size=(300, -1))
        self.amount.SetFont(self.font)
        insu_recpt_label = wx.StaticText(self, -1, "Insures Receipt")
        insu_recpt_label.SetFont(self.font)
        self.insu_recpt = wx.TextCtrl(self, -1, size=(300, -1))
        self.insu_recpt.SetFont(self.font)
        payee_label = wx.StaticText(self, -1, "Payee")
        payee_label.SetFont(self.font)
        self.payee = wx.Choice(self, -1, choices=self.payee_list, size=(300, -1))
        self.payee.SetFont(self.font)
        due_date_label = wx.StaticText(self, -1, "Due Date")
        due_date_label.SetFont(self.font)
        self.due_date = pop.PopupControl(self, -1, size=(300, -1))
        win1 = wx.Window(self.due_date, -1, pos=(0, 0))
        self.cal = wxcal.CalendarCtrl(win1, -1, pos=(0, 0))
        bz = self.cal.GetBestSize()
        win1.SetSize(bz)
        self.due_date.SetPopupContent(win1)

        self.due_date.SetFont(self.font)
        kbima_receipt_label = wx.StaticText(self, -1, "K-BIMA Receipt")
        kbima_receipt_label.SetFont(self.font)
        self.kbima_receipt = wx.TextCtrl(self, -1, size=(300, -1))
        self.kbima_receipt.SetFont(self.font)
        kbima_payment_no_label = wx.StaticText(self, -1, "K-BIMA payment No.")
        kbima_payment_no_label.SetFont(self.font)
        self.kbima_payment_no = wx.TextCtrl(self, -1, size=(300, -1))
        self.kbima_payment_no.SetFont(self.font)
        bank_label = wx.StaticText(self, -1, "Bank")
        bank_label.SetFont(self.font)
        self.bank = wx.Choice(self, -1, choices=self.banks, size=(300, -1))
        self.bank.SetFont(self.font)
        self.save = wx.Button(self, -1, "Save")
        self.save.SetFont(self.font)
        self.clear = wx.Button(self, -1, "Clear")
        self.clear.SetFont(self.font)

        self.cal.Bind(wxcal.EVT_CALENDAR, self.on_cal_selected)
        self.save.Bind(wx.EVT_BUTTON, self.on_save, self.save)
        self.clear.Bind(wx.EVT_BUTTON, self.on_clear, self.clear)
        self.clients.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_select)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.search, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(self.name, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox)
        vbox.Add(self.clients, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        sizer = wx.GridBagSizer(hgap=10, vgap=10)
        sizer.Add(vbox, pos=(0, 0), span=(0,2), border=10)

        sizer.Add(cheque_no_label, pos=(1, 0))
        sizer.Add(self.cheque_no, pos=(1, 1))

        sizer.Add(type_label, pos=(2, 0))
        sizer.Add(self.cheque_type, pos=(2, 1))

        sizer.Add(amount_label, pos=(3, 0))
        sizer.Add(self.amount, pos=(3, 1))
        sizer.Add(insu_recpt_label, pos=(4, 0))
        sizer.Add(self.insu_recpt, pos=(4, 1))
        sizer.Add(payee_label, pos=(5, 0))
        sizer.Add(self.payee, pos=(5, 1))
        sizer.Add(due_date_label, pos=(6, 0))
        sizer.Add(self.due_date, pos=(6, 1))
        sizer.Add(kbima_receipt_label, pos=(7, 0))
        sizer.Add(self.kbima_receipt, pos=(7, 1))
        sizer.Add(kbima_payment_no_label, pos=(8, 0))
        sizer.Add(self.kbima_payment_no, pos=(8, 1))
        sizer.Add(bank_label, pos=(9, 0))
        sizer.Add(self.bank, pos=(9, 1))
        sizer.Add(self.save, pos=(10, 0))
        sizer.Add(self.clear, pos=(10, 1))

        supersizer = wx.BoxSizer(wx.VERTICAL)
        supersizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 20)
        self.SetSizer(supersizer)
        self.InitSearchCtrls()

    def initializer(self):
        print "Updating system"
        func = fun.Datahandler()
        self.payee_list = func.get_payee()
        self.banks = func.get_banks()
        self.cheque_type_list = func.get_chequetype()
        
    def InitSearchCtrls(self):        
        for (searchCtrl, olv) in [(self.search, self.clients)]:            
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

    def get_clients(self):
        clients = fun.Datahandler()
        return clients.allClients()

    def on_select(self, evt):
        client = self.clients.GetSelectedObject()
        self.name.SetValue(client['Name'])

    def on_cal_selected(self, evt):
        self.due_date.PopDown()
        date_ = self.cal.GetDate()
        self.due_date.SetValue('%02d/%02d/%04d' % (date_.GetDay(), date_.GetMonth()+1, date_.GetYear()))
        evt.Skip()

    def on_save(self, evt):
        selected = self.clients.GetSelectedObject()
        client = name = self.name.GetValue()
        if not selected and not client:
            wx.MessageBox("Please select a client", "Field Error", wx.ICON_ERROR)
            return
        elif client:
            pass
        elif selected:
            name = selected["Name"]
            if len(selected) > 1:
                wx.MessageBox("You have selected more than one client", "Field Error", wx.ICON_ERROR)
                return
        try:
            phone = selected["Phone"]
        except TypeError:
            dlg = wx.TextEntryDialog(self, 'Enter Phone Number', 'PHONE NUMBER', 'Entry')
            if dlg.ShowModal() == wx.ID_OK:
                phone = dlg.GetValue()
                if len(phone) < 10:
                    wx.MessageBox("Invalid phone number! Press save button to try again", "ERROR", wx.ICON_ERROR)
                    return
            else:
                return
        amount = self.amount.GetValue()
        insu_recpt = self.insu_recpt.GetValue()
        cheque_no = self.cheque_no.GetValue()
        payee = self.payee.GetStringSelection()
        date = self.cal.GetDate()
        kbima_recpt = self.kbima_receipt.GetValue()
        kbima_recpt_no = self.kbima_payment_no.GetValue()
        bank = self.bank.GetStringSelection()
        cheque_type = self.cheque_type.GetStringSelection()
        if date.IsValid():
            dt = datetime.datetime.today()
            dt = dt.date()
            ymd = map(int, date.FormatISODate().split('-'))
            date = datetime.date(*ymd)
            if dt == date or date < dt:
                wx.MessageBox("Invalid date!", "Date Error", wx.ICON_ERROR)
                return
        if len(cheque_no) > 6:
            wx.MessageBox("Cheque number can only have six numbers", "Field Error", wx.ICON_ERROR)
            return
        if not name or not amount or not payee or not date or not bank or not cheque_type:
            wx.MessageBox("Some details are missing", "Empty Field", wx.ICON_ERROR)
            return

        details_list = [name, cheque_no, amount, insu_recpt, payee, datetime.datetime.now(), date, kbima_recpt,
                        kbima_recpt_no, bank, phone, cheque_type]

        save = ServerAccess(details_list)
        dlg = wx.MessageBox("Do you want to save cheque details for %s" % name, "Cofirmation",
                            wx.ICON_INFORMATION | wx.YES_NO)
        if dlg == wx.NO:
            return
        save.add_cheque()
        save.get_appfiles()

    def on_clear(self, evt):
        self.amount.Clear()
        self.insu_recpt.Clear()
        self.cheque_no.Clear()
        self.payee.Clear()
        self.due_date.SetValue("")
        self.kbima_receipt.Clear()
        self.kbima_payment_no.Clear()
        self.bank.Clear()
        self.name.Clear()



class ChequeSettings(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.func = fun.Datahandler()
        self.bank_list = self.payee_list = self.type_list = []

        self.name_label = wx.StaticText(self, -1, "Name:")
        self.name_label.SetFont(self.font)
        self.payee_name = wx.TextCtrl(self, -1, "", size=(150, -1))
        self.payee_choice = wx.Choice(self, -1, choices=self.payee_list, size=(150, -1))
        self.payee_name.SetFont(self.font)
        self.payee_choice.SetFont(self.font)
        self.save_payee = wx.Button(self, -1, "Save")
        self.save_payee.SetFont(self.font)
        self.delete_payee = wx.Button(self, -1, "Delete")
        self.delete_payee.SetFont(self.font)

        self.bank_label = wx.StaticText(self, -1, "Name:")
        self.bank_label.SetFont(self.font)
        self.bank_name = wx.TextCtrl(self, -1, "", size=(150, -1))
        self.bank_name.SetFont(self.font)
        self.bank_choice = wx.Choice(self, -1, choices=self.bank_list, size=(150, -1))
        self.bank_choice.SetFont(self.font)
        self.payee_name.SetFont(self.font)
        self.save_bank = wx.Button(self, -1, "Save")
        self.save_bank.SetFont(self.font)
        self.delete_bank = wx.Button(self, -1, "Delete")
        self.delete_bank.SetFont(self.font)

        self.type_label = wx.StaticText(self, -1, "Cheque Type")
        self.type_label.SetFont(self.font)
        self.type_name = wx.TextCtrl(self, -1, "")
        self.type_name.SetFont(self.font)
        self.type_choice = wx.Choice(self, -1, choices=self.type_list)
        self.type_choice.SetFont(self.font)
        self.save_type = wx.Button(self, -1, "Save")
        self.save_type.SetFont(self.font)
        self.delete_type = wx.Button(self, -1, "Delete")
        self.delete_type.SetFont(self.font)

        self.message = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE, size=(700, 60))
        self.msg_update = wx.Button(self, -1, "Update")
        self.msg_default = wx.Button(self, -1, "Default")

        self.spin1_label = wx.StaticText(self, -1, "Interval 1")
        self.spin1_label.SetFont(self.font)
        self.spin1 = wx.SpinCtrl(self, -1, "", (30, 50))
        self.spin1.SetFont(self.font)
        self.spin1.SetRange(2, 15)
        self.spin1.SetValue(2)

        self.spin2_label = wx.StaticText(self, -1, "Interval 2")
        self.spin2_label.SetFont(self.font)
        self.spin2 = wx.SpinCtrl(self, -1, "", (30, 50))
        self.spin2.SetFont(self.font)
        self.spin2.SetRange(0, 1)
        self.spin2.SetValue(0)

        self.spin3_label = wx.StaticText(self, -1, "Interval 3")
        self.spin3_label.SetFont(self.font)
        self.spin3 = wx.SpinCtrl(self, -1, "", (30, 50))
        self.spin3.SetFont(self.font)
        self.spin3.SetRange(10, 30)
        self.spin3.SetValue(0)
        self.spin3.Disable()

        self.spin_save = wx.Button(self, -1, "Save")
        self.spin_save.SetFont(self.font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        subsizer = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Message'), orient=wx.VERTICAL)
        vbox.Add(self.message, 0, wx.ALIGN_BOTTOM | wx.ALL, 10)
        hbox = wx.GridBagSizer(hgap=10, vgap=5)
        hbox.Add(self.msg_update, pos=(0, 0))
        hbox.Add(self.msg_default, pos=(0, 1))
        vbox.Add(hbox)
        subsizer.Add(vbox, 0, wx.ALIGN_TOP | wx.ALL, 10)

        sizer.Add(subsizer)
        line = wx.StaticLine(self, -1, size=(780, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line)
        subsizer = wx.BoxSizer(wx.HORIZONTAL)

        vbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Payee'), orient=wx.VERTICAL)
        hbox = wx.GridBagSizer(hgap=10, vgap=5)
        hbox.Add(self.name_label, pos=(0, 0))
        hbox.Add(self.payee_name, pos=(0, 1))
        hbox.Add(self.payee_choice, pos=(0, 2))
        hbox.Add(self.save_payee, pos=(1, 0), span=(1, 2))
        hbox.Add(self.delete_payee, pos=(1, 2))
        vbox.Add(hbox)
        subsizer.Add(wx.StaticText(self, -1, ""))
        subsizer.Add(vbox, 0, wx.ALIGN_TOP | wx.ALL, 10)

        vbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Bank'), orient=wx.VERTICAL)
        hbox = wx.GridBagSizer(hgap=10, vgap=5)
        hbox.Add(self.bank_label, pos=(0, 0))
        hbox.Add(self.bank_name, pos=(0, 1))
        hbox.Add(self.bank_choice, pos=(0, 2))
        hbox.Add(self.save_bank, pos=(1, 0),  span=(1, 2))
        hbox.Add(self.delete_bank, pos=(1, 2))
        vbox.Add(hbox)
        subsizer.Add(vbox, 0, wx.ALIGN_TOP | wx.ALL, 10)

        sizer.Add(subsizer, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

        subsizer = wx.BoxSizer(wx.HORIZONTAL)

        vbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Frequency'), orient=wx.VERTICAL)
        hbox = wx.GridBagSizer(hgap=10, vgap=5)
        hbox.Add(self.spin1_label, pos=(0, 0))
        hbox.Add(self.spin1, pos=(1, 0))
        hbox.Add(self.spin2_label, pos=(0, 1))
        hbox.Add(self.spin2, pos=(1, 1))
        hbox.Add(self.spin3_label, pos=(0, 2))
        hbox.Add(self.spin3, pos=(1, 2))
        vbox.Add(hbox)
        vbox.Add(self.spin_save, 0, wx.ALIGN_BOTTOM | wx.ALL, 10)
        subsizer.Add(vbox, 0, wx.ALIGN_LEFT | wx.ALL, 10)

        vbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Types'), orient=wx.VERTICAL)
        hbox = wx.GridBagSizer(hgap=10, vgap=5)
        hbox.Add(self.type_label, pos=(0, 0))
        hbox.Add(self.type_name, pos=(0, 1))
        hbox.Add(self.type_choice, pos=(0, 2))
        hbox.Add(self.save_type, pos=(1, 0), span=(1, 2))
        hbox.Add(self.delete_type, pos=(1, 2))
        vbox.Add(hbox)
        subsizer.Add(vbox, 10, wx.ALIGN_RIGHT | wx.ALL, 10)

        sizer.Add(subsizer)
        
        self.Bind(wx.EVT_BUTTON, self.update_message_method, self.msg_update)
        self.Bind(wx.EVT_BUTTON, self.default_message_method, self.msg_default)
        self.Bind(wx.EVT_BUTTON, self.save_payee_method, self.save_payee)
        self.Bind(wx.EVT_BUTTON, self.delete_payee_method, self.delete_payee)
        self.Bind(wx.EVT_BUTTON, self.save_bank_method, self.save_bank)
        self.Bind(wx.EVT_BUTTON, self.delete_bank_method, self.delete_bank)
        self.Bind(wx.EVT_BUTTON, self.save_type_method, self.save_type)
        self.Bind(wx.EVT_BUTTON, self.delete_type_method, self.delete_type)
        self.Bind(wx.EVT_BUTTON, self.update_frequency, self.spin_save)
        self.Bind(wx.EVT_CHOICE, self.payee_choice_method, self.payee_choice)
        self.Bind(wx.EVT_CHOICE, self.bank_choice_method, self.bank_choice)
        self.Bind(wx.EVT_CHOICE, self.type_choice_method, self.type_choice)

        self.SetSizer(sizer)
        self.initializer()

    def initializer(self):        
        messages = self.func.get_messages()
        if messages:
            for message in messages:
                if message['Type'] == "cheque":
                    txt = message['Message']
                    self.message.SetValue(txt)
        self.bank_list = self.func.get_banks()
        self.payee_list = self.func.get_payee()
        self.type_list = self.func.get_chequetype()
        self.bank_choice.Clear()
        self.payee_choice.Clear()
        self.type_choice.Clear()
        self.bank_choice.AppendItems(self.bank_list)
        self.type_choice.AppendItems(self.type_list)
        self.payee_choice.AppendItems(self.payee_list)

    def payee_choice_method(self, evt):
        payee = self.payee_choice.GetStringSelection()
        self.payee_name.SetValue(payee)

    def bank_choice_method(self, evt):
        bank = self.bank_choice.GetStringSelection()
        self.bank_name.SetValue(bank)

    def type_choice_method(self, evt):
        type_ = self.type_choice.GetStringSelection()
        self.type_name.SetValue(type_)
        
    def update_message_method(self, evt):
        msg = self.message.GetValue()
        arg = ('cheque', 'message', msg)
        server = ServerAccess(arg)
        server.update_message()
        server.get_appfiles()
    
    def default_message_method(self, evt):
        msg = self.message.GetValue()
        dlg = wx.MessageBox("Do you want to restore the default message for %s?" % msg, "Confirmation",
                            wx.ICON_WARNING | wx.YES_NO)
        if dlg == wx.NO:
            return
        print msg
        
    def save_payee_method(self, evt):
        payee = self.payee_name.GetValue()
        if not payee:
            wx.MessageBox("Empty field", "Error", wx.ICON_ERROR)
            return
        if payee in self.payee_list:
            wx.MessageBox("%s already exists!" % payee, "Error", wx.ICON_ERROR)
            return
        server = ServerAccess(payee)
        print server.add_payee()
    
    def delete_payee_method(self, evt):
        payee = self.payee_choice.GetStringSelection()
        if not payee:
            wx.MessageBox("Please select a payee to delete", "Error", wx.ICON_ERROR)
            return
        dlg = wx.MessageBox("Do you want to delete %s from the system" % payee, "Confirmation", wx.ICON_WARNING | wx.YES_NO)
        if dlg == wx.NO:
            return
        server = ServerAccess(payee)
        print server.delete_payee()
        server.get_appfiles()
        self.initializer()
        
    def save_bank_method(self, evt):
        bank = self.bank_name.GetValue()
        if not bank:
            wx.MessageBox("Empty field", "Error", wx.ICON_ERROR)
            return
        if bank in self.bank_list:
            wx.MessageBox("%s already exists" % bank, "Error", wx.ICON_ERROR)
            return
        server = ServerAccess(bank)
        server.add_bank()
        server.get_appfiles()
        self.initializer()
    
    def delete_bank_method(self, evt):
        bank = self.bank_choice.GetStringSelection()
        if not bank:
            wx.MessageBox("Select bank to delete", "Error", wx.ICON_ERROR)
            return
        dlg = wx.MessageBox("Do you want to delete %s from the system" % bank, "Confirmation", wx.ICON_WARNING
                            | wx.YES_NO)
        if dlg == wx.NO:
            return
        server = ServerAccess(bank)
        server.delete_bank()
        self.initializer()
        
    def save_type_method(self, evt):
        type_ = self.type_name.GetValue()
        if not type_:
            wx.MessageBox("Empty field", "Error", wx.ICON_ERROR)
            return
        if type_ in self.type_list:
            wx.MessageBox("%s already exists" % type_, "Error", wx.ICON_ERROR)
            return
        server = ServerAccess(type_)
        server.add_cheque_type()
        server.get_appfiles()
        self.initializer()
    
    def delete_type_method(self, evt):
        type_ = self.type_choice.GetStringSelection()
        if not type_:
            wx.MessageBox("Select cheque type to delete", "Error", wx.ICON_ERROR)
            return
        dlg = wx.MessageBox("Do you want to delete %s from the system" % type_, "Confirmation", wx.ICON_WARNING | wx.YES_NO)
        if dlg == wx.NO:
            return
        server = ServerAccess(type_)
        server.delete_cheque_type()
        server.get_appfiles()
        self.initializer()

    def update_frequency(self, evt):
        val1 = self.spin1.GetValue()
        val2 = self.spin2.GetValue()
        server = ServerAccess(('cheque', 'interval', [val1, val2]))
        server.update_config()


class MessagesSettings(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.type_list = list()

        type_label = wx.StaticText(self, -1, "Type: ")
        self.type_choice = wx.Choice(self, -1, choices=self.type_list)
        self.type = wx.StaticText(self, -1, "", size=(100, -1))
        self.type.SetForegroundColour(wx.BLUE)

        self.message = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE, size=(700, 60))
        self.msg_update = wx.Button(self, -1, "Update")
        self.msg_default = wx.Button(self, -1, "Default")

        spin1_label = wx.StaticText(self, -1, "Interval 1")
        self.spin1 = wx.SpinCtrl(self, -1, "", (30, 50))
        self.spin1_choice = wx.Choice(self, -1, choices=["ACTIVE", "INACTIVE"])
        self.spin1.SetFont(self.font)
        self.spin1.SetRange(0, 3)
        self.spin1.SetValue(0)

        spin2_label = wx.StaticText(self, -1, "Interval 2")
        self.spin2 = wx.SpinCtrl(self, -1, "", (30, 50))
        self.spin2_choice = wx.Choice(self, -1, choices=["ACTIVE", "INACTIVE"])
        self.spin2.SetFont(self.font)
        self.spin2.SetRange(4, 10)
        self.spin2.SetValue(5)

        spin3_label = wx.StaticText(self, -1, "Interval 3")
        self.spin3 = wx.SpinCtrl(self, -1, "", (30, 50))
        self.spin3_choice = wx.Choice(self, -1, choices=["ACTIVE", "INACTIVE"])
        self.spin3.SetFont(self.font)
        self.spin3.SetRange(10, 30)
        self.spin3.SetValue(0)

        self.spin_save = wx.Button(self, -1, "Save")
        self.spin_save.SetFont(self.font)

        min_label = wx.StaticText(self, -1, "Min: ")
        self.min_amount = masked.NumCtrl(self, -1, size=(300, -1))

        max_label = wx.StaticText(self, -1, "Max: ")
        self.max_amount = masked.NumCtrl(self, -1, size=(300, -1))

        self.save_amount = wx.Button(self, -1, "Save")

        status_label = wx.StaticText(self, -1, "Status")
        self.status_choice = wx.Choice(self, -1, choices=["ACTIVE", "INACTIVE"])
        self.status = wx.StaticText(self, -1, "", size=(70, -1))

        self.Bind(wx.EVT_CHOICE, self.change_type, self.type_choice)
        self.Bind(wx.EVT_CHOICE, self.change_status, self.status_choice)
        self.Bind(wx.EVT_BUTTON, self.update_message, self.msg_update)
        self.Bind(wx.EVT_BUTTON, self.default_message, self.msg_default)
        self.Bind(wx.EVT_BUTTON, self.save_frequency, self.spin_save)
        self.Bind(wx.EVT_BUTTON, self.save_amount_method, self.save_amount)

        sizer = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(type_label, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(self.type_choice, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(self.type, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hbox.Add(status_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hbox.Add(self.status_choice, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        hbox.Add(self.status, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        vbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Message'), orient=wx.VERTICAL)
        vbox.Add(hbox)
        vbox.Add(self.message)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.msg_update, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        hbox.Add(self.msg_default, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        vbox.Add(hbox)
        sizer.Add(vbox, 0, wx.ALIGN_TOP | wx.ALL, 5)

        vbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Frequency'), orient=wx.VERTICAL)
        subsizer = wx.FlexGridSizer(hgap=10, vgap=5, cols=3)
        subsizer.Add(spin1_label)
        subsizer.Add(spin2_label)
        subsizer.Add(spin3_label)
        subsizer.Add(self.spin1)
        subsizer.Add(self.spin2)
        subsizer.Add(self.spin3)
        subsizer.Add(self.spin1_choice)
        subsizer.Add(self.spin2_choice)
        subsizer.Add(self.spin3_choice)
        vbox.Add(subsizer, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
        vbox.Add(self.spin_save, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
        sizer.Add(vbox, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

        vbox = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Amount'), orient=wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(min_label, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(self.min_amount, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(max_label, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        hbox.Add(self.max_amount, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        vbox.Add(hbox)
        vbox.Add(self.save_amount)
        sizer.Add(vbox, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

        self.SetSizer(sizer)
        self.initialize()

    def initialize(self):
        msgs = fun.Datahandler().get_messages()
        message_types = set()
        for msg in msgs:
            message_types.add(msg["Type"].capitalize())
        self.type_list = list(message_types)
        self.type_choice.AppendItems(self.type_list)
        for msg in msgs:
            if msg["Type"] == "renewal":
                message = msg["Message"]
                self.message.SetValue(message)
                break
        self.type.SetLabelText("RENEWAL")
        self.initialize_widgets("renewal")

    def initialize_widgets(self, _type):
        frequency = [self.spin1, self.spin2, self.spin3, self.spin1_choice, self.spin2_choice, self.spin3_choice,
                     self.spin_save]
        amount = [self.min_amount, self.max_amount, self.save_amount]
        conf = fun.Datahandler.get_configurations()
        if _type.lower() in ["quicktxt", "general"]:
            return wx.MessageBox("%s messages do not require configuring" % _type.capitalize(), "Informations",
                                 wx.ICON_WARNING)
        elif not _type.lower() in conf.keys():
            return wx.MessageBox("Configurations for %s are missing" % _type, "File Error", wx.ICON_ERROR)
        config = conf[_type.lower()]
        if "interval" in config.keys():
            for widget in frequency:
                widget.Enable()
        else:
            for widget in frequency:
                widget.Disable()
        if "min" in config.keys():
            for widget in amount:
                widget.Enable()
        else:
            for widget in amount:
                widget.Disable()
        self.type.SetLabelText(_type.upper())
        if config["status"]:
            self.status.SetLabelText("ACTIVE")
            self.status.SetForegroundColour(wx.GREEN)
        else:
            self.status.SetLabelText("INACTIVE")
            self.status.SetForegroundColour(wx.RED)
        msgs = fun.Datahandler().get_messages()
        for msg in msgs:
            if msg["Type"] == _type.lower():
                message = msg["Message"]
                self.message.SetValue(message)
                break
        self.Refresh()

    def change_type(self, evt):
        _type = self.type_choice.GetStringSelection()
        self.initialize_widgets(_type)

    def update_message(self, evt):
        _type = self.type.GetLabelText()
        msgs = fun.Datahandler().get_messages()
        message = ""
        for msg in msgs:
            if msg["Type"] == _type.lower():
                message = msg["Message"]
                break
        msg = self.message.GetValue()
        if msg == message:
            return wx.MessageBox("No changes have been detected", "Warning", wx.ICON_WARNING)
        args = (_type.lower(), "message", msg)
        server = ServerAccess(args)
        server.update_message()

    def default_message(self, evt):
        dlg = wx.MessageBox("Do you want to restore the default message?", "Confirmation", wx.ICON_WARNING | wx.YES_NO)
        if dlg == wx.NO:
            return
        _type = self.type.GetLabelText()
        server = ServerAccess(_type)
        server.set_default_message()

    def save_frequency(self, evt):
        frequency = list()
        status = [(self.spin1_choice.GetStringSelection(),self.spin1.GetValue()),
                  (self.spin2_choice.GetStringSelection(),self.spin2.GetValue()),
                  (self.spin3_choice.GetStringSelection(),self.spin3.GetValue())]
        for spin in status:
            if spin[0] == "ACTIVE":
                frequency.append(spin[1])
        _type = self.type.GetLabelText().lower()
        server = ServerAccess((_type, 'interval', frequency))
        server.update_config()

    def save_amount_method(self, evt):
        amounts = list()
        _type = self.type.GetLabelText().lower()
        min = self.min_amount.GetValue()
        max = self.max_amount.GetValue()
        if min:
            amounts.append((_type, "min", min))
        if max:
            amounts.append((_type, "max", max))
        print amounts
        if not amounts:
            return wx.MessageBox("Minimum or maximum amount has not been specified", "Missing details", wx.ICON_WARNING)
        server = ServerAccess(amounts)
        server.update_amount()

    def change_status(self, evt):
        _type = self.type.GetLabelText().lower()
        status = self.status_choice.GetStringSelection()
        if status == "ACTIVE":
            server = ServerAccess((_type, "status", True))
            server.update_config()
            self.status.SetLabelText("ACTIVE")
            self.status.SetForegroundColour(wx.GREEN)
        else:
            server = ServerAccess((_type, "status", False))
            server.update_config()
            self.status.SetLabelText("INACTIVE")
            self.status.SetForegroundColour(wx.RED)
        self.status.Refresh()


class ControlPanel(wx.Notebook):
    def __init__(self, parent, id=-1):
        wx.Notebook.__init__(self, parent, id, size=(21, 21), style= wx.BK_DEFAULT)
        win = MessagesSettings(self)
        self.AddPage(win, "Messages")
        win = ChequeSettings(self)
        self.AddPage(win, "Cheques Settings")
        # win = wx.Panel(self, -1)
        # self.AddPage(win, "SMS settings")


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Title", size=(850, 600))
        #ChequeSettings(self)
        # AddChequePanel(self)
        ControlPanel(self)
        #ManageChequePanel(self)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame().Show()
    app.MainLoop()
