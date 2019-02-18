import wx
from mainframe import MainFrame

app = wx.App()

frame = MainFrame(None, title='Flat File Py')
frame.Show()

app.MainLoop()