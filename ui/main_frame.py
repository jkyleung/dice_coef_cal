import wx
from ui.main_panel import MainPanel

# This is the main window layout including the menu, status bar, etc.

class MainFrame(wx.Frame):

    def __init__(self, version, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        
        panel = MainPanel(self)
        # button position in format (x, y) starting from (top, left)
        # b = wx.Button(pnl, -1, "This is a button", (150,280))

        self.make_menu_bar()

        self.CreateStatusBar()
        self.SetStatusText(version + " Development in progress")

    def make_menu_bar(self):
        
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        help_menu = wx.Menu()

        exit_menu_item = file_menu.Append(wx.ID_EXIT)
        about_menu_item = help_menu.Append(wx.ID_ABOUT)

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

        # set the on click function to the menu item
        self.Bind(wx.EVT_MENU, self.on_exit, exit_menu_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_menu_item)

    def on_exit(self, event):
        # close the window (frame)
        self.Close(True)

    def on_about(self, event):
        # show the message box
        wx.MessageBox("This is the information about the application.", "Message title", wx.OK|wx.ICON_INFORMATION)