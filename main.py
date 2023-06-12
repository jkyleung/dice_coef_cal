
# GUI program

# pre-install the library if not yet installed
# select the STL file of skull(mandible)
# choose display the 3D model or not
# display the output landmark coordinates (and 3D model)

import wx
import ui.app
from ui.main_frame import *

# constant
APP_NAME = "Segmentation Comparison Application"
VERSION = 'v0.1'
WINDOW_SIZE = wx.Size(600,800)

def main():
    print("=============================")
    print("|| This is the Debug panel ||")
    print("=============================")
    
    # application object
    app = ui.app.App()
    # the actual window object
    frame = MainFrame(parent=None, title=APP_NAME+' '+VERSION, size=WINDOW_SIZE, version=VERSION)

    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()