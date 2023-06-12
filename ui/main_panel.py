import wx
import os

import numpy as np
import nrrd
# import pyvista as pv
import threading

import dice_coef

# This is the main window content layout and logic including the button, dialog, message box, etc.

# file types of file dialog
wildcard = "NRRD files (*.nrrd)|*.nrrd|" \
            "All files (*.*)|*.*"

class MainPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super(MainPanel, self).__init__(*args, **kw)

        sizer = wx.GridBagSizer(5, 5)

        self.currentDirectory = os.getcwd()

        # file loader
        self.file_dialog_lb = []
        self.file_dialog_text = []
        self.file_dialog_btn = []
        for i in range(2):
            self.file_dialog_lb.append(wx.StaticText(self, label="3D model (NRRD file):"))
            self.file_dialog_text.append(wx.TextCtrl(self))
            self.file_dialog_btn.append(wx.Button(self, label="Browse..."))
            sizer.Add(self.file_dialog_lb[i], pos=(i, 0), flag=wx.LEFT|wx.TOP, border=10)
            sizer.Add(self.file_dialog_text[i], pos=(i, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
            sizer.Add(self.file_dialog_btn[i], pos=(i, 4), flag=wx.TOP|wx.RIGHT, border=5)

        # user options
        static_box_options = wx.StaticBox(self, label="Options")
        boxsizer_options = wx.StaticBoxSizer(static_box_options, wx.VERTICAL)
        self.user_options = []
        user_options_name = ["Display 3D model (not available now)"]
        for i in range(len(user_options_name)):
            self.user_options.append(wx.CheckBox(self, label=user_options_name[i]))
            boxsizer_options.Add(self.user_options[i],flag=wx.LEFT|wx.BOTTOM, border=5)
        sizer.Add(boxsizer_options, pos=(2, 0), span=(1, 5), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)

        self.user_options[0].SetValue(False)
        self.user_options[0].Disable()

        # coef display panel
        static_box_coef = wx.StaticBox(self, label="Comparison Output")
        boxsizer_coef = wx.StaticBoxSizer(static_box_coef, wx.VERTICAL)
        gridsizer_coef = wx.GridBagSizer(5, 5)
        self.coef_label = []
        coef_name = ["DICE coefficient"]
        for i in range(len(coef_name)):
            self.coef_label.append(wx.StaticText(self, label=coef_name[i]))
            gridsizer_coef.Add(self.coef_label[i], pos=(i, 0),flag=wx.LEFT|wx.BOTTOM, border=5)
        
        self.coef_value = []
        for i in range(len(coef_name)):
            self.coef_value.append(wx.StaticText(self, label=str(0)))
            gridsizer_coef.Add(self.coef_value[i], pos=(i, 3),flag=wx.LEFT|wx.BOTTOM, border=5)
        boxsizer_coef.Add(gridsizer_coef, flag=wx.LEFT|wx.TOP, border=5)

        sizer.Add(boxsizer_coef, pos=(3, 0), span=(1, 5), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)

        btn_select_all = wx.Button(self, label="Select All")
        btn_select_all.Disable()
        btn_start = wx.Button(self, label="Start")
        btn_reset = wx.Button(self, label="Reset")

        sizer.Add(btn_select_all, pos=(4,0), flag=wx.LEFT, border=10)
        sizer.Add(btn_start, pos=(4,3))
        sizer.Add(btn_reset, pos=(4,4), span=(1, 1), flag=wx.BOTTOM|wx.RIGHT, border=10)

        # extend the column (or row)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableRow(3)

        self.SetSizer(sizer)
        sizer.Fit(self)

        # on click function for buttons
        self.Bind(wx.EVT_BUTTON, self.on_select_all, btn_select_all)
        self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
        self.Bind(wx.EVT_BUTTON, self.on_start, btn_start)

        for file_id in range(len(self.file_dialog_lb)):
            self.Bind(wx.EVT_BUTTON, self.get_on_open_file(file_id), self.file_dialog_btn[file_id])

    def on_select_all(self, event):
        for option in self.user_options:
            option.SetValue(True)

    def on_reset(self, event):
        for option in self.user_options:
            option.SetValue(False)
        for text in self.file_dialog_text:
            text.SetValue("")

    def on_start(self, event):
        ## start the application
        # wx.MessageBox("This is the message of start.", "Message title", wx.OK|wx.ICON_INFORMATION)
        coef_arr = []
        
        ## load the NRRD file
        # not use the STL file
        nrrd_file_1 = self.file_dialog_text[0].GetValue()
        nrrd_file_2 = self.file_dialog_text[1].GetValue()
        model_npy_1, fileheader1 = nrrd.read(nrrd_file_1)   # index_order='C'
        model_npy_1, fileheader1 = nrrd.read(nrrd_file_2)

        ## calculate the DICE coef
        dice_coef_value = dice_coef.dice_coef_calculation(model_npy_1, model_npy_2)
        coef_arr.append(dice_coef_value)

        ## display the 3D model
        # not use at this moment
        # point_cloud = output.to('cpu').detach().numpy()
        # # display_pv(point_cloud)
        # if self.user_options[0].GetValue():
        #     display_thread = threading.Thread(target=display_pv, args=(point_cloud[0], stl_path))
        #     display_thread.start()

        # display the value
        for i, coef in enumerate(self.coef_value):
            coef.SetLabel(coef_arr[i])
        
        # wx.MessageBox("This is the message of finish.", "Message title", wx.OK|wx.ICON_INFORMATION)

    # generator of "on_open_file" function
    def get_on_open_file(self, file_id):
        # open file loading dialog
        def on_open_file(event):
            # Open FileDialog
            # print(file_id)
            dlg = wx.FileDialog(
                self, message="Choose a file",
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
            )
            if dlg.ShowModal() == wx.ID_OK:
                paths = dlg.GetPaths()
                self.file_dialog_text[file_id].SetValue('/'.join(paths))
            dlg.Destroy()
        return on_open_file
    