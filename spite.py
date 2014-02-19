"""
This program implements a bare-bones text editor
that can load, modify and save documents.
"""

__author__     = "Toadpipe"
__version__    = "0.1"
__date__       = "$Date: 2009/01/25 $"
__copyright__  = "Never"
__license__    = "Python"

from wxPython.wx import *
from sys import argv
import os
import time

TITLE = "rapid file viewer"
ABOUT_TITLE = "about"
ABOUT_BODY = "a small program to rapidly view the contents of many files, derived from\n\nwxExampleCode: simple text editor\nhttp://aaronland.info/python/wxpython/examples/"

ID_ABOUT = wxNewId()
ID_OPEN = wxNewId()
ID_SAVE = wxNewId()
ID_SAVEAS = wxNewId()
ID_EXIT = wxNewId()

ID_SPLITTER = 300

DIR = '.'

class MyFrame(wxFrame):
 def __init__(self, parent, ID, title):
  self.__filename__ = NULL
  wxFrame.__init__(self, parent, ID, title, wxDefaultPosition, wxSize(800, 600), style=wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE)
  self.CreateStatusBar()
  self.SetStatusText("this is the statusbar")
  FileMenu = wxMenu()
  FileMenu.Append(ID_OPEN, "&open", "open a directory")
  FileMenu.AppendSeparator()
  FileMenu.Append(ID_SAVEAS, "&save as", "save current document to another file")
  FileMenu.AppendSeparator()
  FileMenu.Append(ID_EXIT, "e&xit", "guess what this does")
  HelpMenu = wxMenu()
  HelpMenu.Append(ID_ABOUT, "&about", "useless information")
  menuBar = wxMenuBar()
  menuBar.Append(FileMenu, "&file")
  menuBar.Append(HelpMenu,"&help")
  self.SetMenuBar(menuBar)
  EVT_MENU(self, ID_ABOUT, self.About)
  EVT_MENU(self, ID_SAVEAS, self.SaveAs)
  EVT_MENU(self, ID_OPEN, self.Open)
  EVT_MENU(self, ID_EXIT, self.Quit)

  files = [f for f in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, f))]
  self.path = DIR

  self.splitter = wxSplitterWindow(self, ID_SPLITTER, style=wxSP_BORDER)
  self.list = wxListBox(self.splitter, 26, (-1, -1), (170, 130), files, wxLB_SINGLE|wxLB_SORT)
  self.control = wxTextCtrl(self.splitter, -1, style=wxTE_MULTILINE|wxTE_READONLY)
  self.control.SetFont(wxFont(10, wxFONTFAMILY_MODERN, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_NORMAL))
  if len(argv) > 1:
   if os.path.exists(argv[1]):
    self.Load(argv[1])
   else:
    self.Alert("error",
    argv[1] + "is not a valid file")
  self.splitter.SplitVertically(self.list, self.control, 34)

  EVT_LISTBOX(self, 26, self.OnSelect)

 def OnSelect(self, event):
  index = event.GetSelection()
  filename = self.list.GetString(index)
  if filename:
   #print filename
   self.Load(filename)

 def About(self, event):
  self.Alert(ABOUT_TITLE,ABOUT_BODY)

 def Open(self,event):
  dir = wxDirSelector("choose a directory")
  if dir:
   self.list.Clear()
   self.path = dir
   self.list.AppendItems([f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))])

 def Load(self,filename):
  self.__filename__ = filename
  self.control.LoadFile(os.path.join(self.path, filename))
  self.SetStatusText(filename)

 def SaveAs(self,event) :
  filename = wxFileSelector("save current file as")
  if filename:
   self.control.SaveFile(filename)
   self.__filename__ = filename
  else:
   self.Alert("alert","save cancelled")

 def Quit(self, event):
  if self.control.IsModified:
   answer = wxMessageBox("file was modified\n\nsave it?", "confirm", wxYES_NO | wxCANCEL);
   if (answer == wxYES):
    self.Save(event)
   if (answer == wxCANCEL):
    return false
   self.Close(true)

 def Alert(self,title,msg):
  dlg = wxMessageDialog(self, msg, title, wxOK | wxICON_INFORMATION)
  dlg.ShowModal()
  dlg.Destroy()

class MyApp(wxApp):
 def OnInit(self):
  frame = MyFrame(NULL, -1, TITLE)
  frame.Show(true)
  self.SetTopWindow(frame)
  return true

app = MyApp()
app.MainLoop()
