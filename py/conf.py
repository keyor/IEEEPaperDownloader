#filename:ConferenceSearchSystem.py
#encoding=utf-8
import wx
import threading
import wx.lib
import os
import time
import thread
import datetime 
import wx.html as html
import wx.grid as grid
import pprint
from wx.lib.stattext import GenStaticText as StaticText
import confs
class TaskBarIcon(wx.TaskBarIcon):
    ID_Hello = wx.NewId()
    ID_Quit=wx.NewId()
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(name='./icons/search.ico', type=wx.BITMAP_TYPE_ICO), 'TaskBarIcon!')
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)
        self.Bind(wx.EVT_MENU, self.OnHello, id=self.ID_Hello)
        self.Bind(wx.EVT_MENU,self.OnQuit,id=self.ID_Quit)
    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
           self.frame.Iconize(False)
        if not self.frame.IsShown():
           self.frame.Show(True)
        self.frame.Raise()
    def OnQuit(self,event):
        self.Destroy()
        frame.Close(True)

    def OnHello(self, event):
        wx.MessageBox('Hello From TaskBarIcon!', 'Prompt')

    # override
    def CreatePopupMenu(self):
        menu = wx.Menu()
        #menu.Append(self.ID_Hello, 'Hello')
        menu.Append(self.ID_Quit,'Quit')
        return menu
class MyFrame(wx.MDIParentFrame):
    searchpage=0
    def __init__(self):
        MyFrame.Myframe=wx.MDIParentFrame.__init__(self,None,-1,"ConferenceSearchSystem",size=(1024,600))
        png_home=wx.Image('./icons/home.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        png_print=wx.Image('./icons/print.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        png_refresh=wx.Image('./icons/refresh.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        png_search=wx.Image('./icons/search.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        png_stop=wx.Image('./icons/stop.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        png_back=wx.Image('./icons/back.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        png_foward=wx.Image('./icons/foward.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        png_help=wx.Image('./icons/help.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.CreateStatusBar()
        self.SetStatusText("statusbar")
        menuBar=wx.MenuBar()
        filemenu=wx.Menu()
        filemenu.Append(11,"NEW     CTRL+N")
        self.Bind(wx.EVT_MENU, self.OnHomeWindow, id=11)
        filemenu.Append(12,"OPEN     CTRL+O")
        self.Bind(wx.EVT_MENU, self.OnOpen, id=12) 
        filemenu.Append(13,"CLOSE    CTRL+W")
        self.Bind(wx.EVT_MENU, self.OnClose, id=13)
        #self.Bind(wx.EVT_CLOSE,self.OnClose)
        '''
        filemenu.Append(14,"SAVE     CTRL+S")
        self.Bind(wx.EVT_MENU, self.OnSave, id=14)     
        filemenu.Append(15,"Save As        ")
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id=15)        
        filemenu.Append(16,"Print    CTRL+P")
        self.Bind(wx.EVT_MENU, self.OnPrint, id=16)
        filemenu.Append(17,"Recent         ")
        filemenu.Append(18,"Exit      ALT+X")
        self.Bind(wx.EVT_MENU, self.OnExit, id=18)
        '''
        '''
        editmenu=wx.Menu()
        editmenu.Append(21,"Undo     CTRL+Z")
        self.Bind(wx.EVT_MENU, self.OnUndo, id=21) 
        editmenu.Append(22,"CUT      CTRL+X")
        self.Bind(wx.EVT_MENU, self.OnCut, id=22) 
        editmenu.Append(23,"Copy     CTRL+C")
        self.Bind(wx.EVT_MENU, self.OnCopy, id=23) 
        editmenu.Append(24,"Paste    CTRL+V")
        self.Bind(wx.EVT_MENU, self.OnPaste, id=24) 
        
        viewmenu=wx.Menu()        
        subtoolbarmenu=wx.Menu()
        subtoolbarmenu.AppendCheckItem(311,"Standard")
        self.Bind(wx.EVT_MENU, self.OnStandard, id=311) 
        subtoolbarmenu.AppendCheckItem(312,"Customize")
        self.Bind(wx.EVT_MENU, self.OnCustomize, id=312) 
        viewmenu.AppendMenu(31,"Toolbar",subtoolbarmenu)       
        viewmenu.AppendCheckItem(32,"Statusbar")
        self.Bind(wx.EVT_MENU, self.OnStatusbar, id=32) 
        subgotomenu=wx.Menu()
        subgotomenu.Append(321,"Home Page")
        self.Bind(wx.EVT_MENU,self.OnHomeWindow,id=321)
        subgotomenu.Append(322,"Search")
        self.Bind(wx.EVT_MENU,self.OnSearchWindow,id=322)
        subgotomenu.Append(323,"Back")
        self.Bind(wx.EVT_MENU, self.OnBack, id=323) 
        subgotomenu.Append(324,"Forward")
        self.Bind(wx.EVT_MENU, self.OnForward, id=324) 
        viewmenu.AppendMenu(33,"Goto",subgotomenu)
        subtextsizemenu=wx.Menu()
        subtextsizemenu.Append(331,"Largest")
        self.Bind(wx.EVT_MENU, self.OnLargest, id=331) 
        subtextsizemenu.Append(332,"Larger")
        self.Bind(wx.EVT_MENU, self.OnLarger, id=332) 
        subtextsizemenu.Append(333,"Medium")
        self.Bind(wx.EVT_MENU, self.OnMedium, id=333) 
        subtextsizemenu.Append(334,"Smaller")
        self.Bind(wx.EVT_MENU, self.OnSmaller, id=334) 
        subtextsizemenu.Append(335,"Smallest")
        self.Bind(wx.EVT_MENU, self.OnSmallest, id=335) 
        viewmenu.AppendMenu(34,"Textsize",subtextsizemenu)
        viewmenu.Append(35,"stop")
        self.Bind(wx.EVT_MENU, self.OnStop, id=35)     
        viewmenu.Append(36,"refresh")
        self.Bind(wx.EVT_MENU, self.OnRefresh, id=36) 
        subthememenu=wx.Menu()
        subthememenu.AppendCheckItem(341,"Blue")
        self.Bind(wx.EVT_MENU, self.OnBlue, id=341) 
        subthememenu.AppendCheckItem(342,"Native")
        self.Bind(wx.EVT_MENU, self.OnNative, id=342) 
        subthememenu.AppendCheckItem(343,"Tan")
        self.Bind(wx.EVT_MENU, self.OnTan, id=343) 
        subthememenu.AppendCheckItem(344,"Flat 1")
        self.Bind(wx.EVT_MENU, self.OnFlat1, id=344) 
        subthememenu.AppendCheckItem(345,"Flat 2")
        self.Bind(wx.EVT_MENU, self.OnFlat2, id=345) 
        viewmenu.AppendMenu(37,"Theme",subthememenu)
        '''               
        helpmenu=wx.Menu()
        helpmenu.Append(41,"about")
        self.Bind(wx.EVT_MENU,self.OnAbout,id=41)
        databasemenu=wx.Menu()
        databasemenu.Append(51,"create database")
        self.Bind(wx.EVT_MENU,self.OnCreateDatabase,id=51)
        subsearchdatabasemenu=wx.Menu()
        subsearchdatabasemenu.Append(521,"view conferences")
        self.Bind(wx.EVT_MENU,self.OnViewConf,id=521)
        subsearchdatabasemenu.Append(522,"view papers")
        self.Bind(wx.EVT_MENU,self.OnViewPaper,id=522)
        databasemenu.AppendMenu(52,"search database",subsearchdatabasemenu)
        #databasemenu.Append(53,"delete database")
        self.Bind(wx.EVT_MENU,self.OnDeleteDatabase,id=53)
        configmenu=wx.Menu()
        configmenu.Append(61,"download config")
        self.Bind(wx.EVT_MENU,self.OnDownloadConfig,id=61)
        
        menuBar.Append(filemenu,"File ")
        #menuBar.Append(editmenu,"Edit ")
       # menuBar.Append(viewmenu,"View ")
        menuBar.Append(helpmenu,"Help ")
        menuBar.Append(databasemenu,"database")
        menuBar.Append(configmenu,"config")       
        self.SetMenuBar(menuBar)      

        toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.TB_TEXT)     # 创建工具栏    
        toolbar.AddLabelTool(100, 'Home',png_home)
        #toolbar.AddLabelTool(101,'print', png_print)
        #toolbar.AddLabelTool(102, 'refresh',png_refresh)
        toolbar.AddLabelTool(103, 'search',png_search)
        #toolbar.AddLabelTool(104, 'stop',png_stop)
        #toolbar.AddLabelTool(105, 'back',png_back)
        #toolbar.AddLabelTool(106, 'forward',png_foward)
        toolbar.AddLabelTool(107,'help', png_help)
        self.Bind(wx.EVT_TOOL,self.OnHomeWindow,id=100)
        self.Bind(wx.EVT_TOOL,self.OnPrint,id=101)
        self.Bind(wx.EVT_TOOL,self.OnRefresh,id=102)
        self.Bind(wx.EVT_TOOL,self.OnSearchWindow,id=103)
        self.Bind(wx.EVT_TOOL,self.OnStop,id=104)
        self.Bind(wx.EVT_TOOL,self.OnBack,id=105)
        self.Bind(wx.EVT_TOOL,self.OnForward,id=106)
        self.Bind(wx.EVT_TOOL,self.OnAbout,id=107)      
        toolbar.Realize()
        self.SetIcon(wx.Icon('./icons/search.ico',wx.BITMAP_TYPE_ICO))
        self.taskBarIcon=TaskBarIcon(self)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy) # 最小化事件绑定
    
        self.Bind(wx.EVT_TOOL, self.OnExit, id=wx.ID_EXIT)
        toolbar.Realize()
        
        MyFrame.searchpage = wx.MDIChildFrame(self, -1, "SearchPage",size=(1000,480))           # 新建子窗口
        MyFrame.searchpage.SetBackgroundColour((255,255,255))
        MyFrame.myonsearchwindow=OnSearchWindows()

        self.SetForegroundColour((158,208,221))
    def OnHide(self, event):
        self.Hide()
    def OnIconfiy(self, event):
        pass
    def OnHomeWindow(self, evt):        
        homepage= wx.MDIChildFrame(self,-1, "HomePage",size=(1000,480))           # 新建子窗口
        homepage.SetBackgroundColour((158,208,221))
        font1=wx.Font(24,wx.DEFAULT,wx.NORMAL,wx.BOLD,False)
        font2=wx.Font(12,wx.DEFAULT,wx.NORMAL,wx.NORMAL,False)
        font3=wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.NORMAL,True)
        sizer=wx.BoxSizer(wx.VERTICAL)
        homepage.SetSizer(sizer)
        Label1=wx.StaticText(homepage,-1,
        """

                    Conference Search System

        """)
        Label2=wx.StaticText(homepage,-1,"""
                If you want to search the conference from web, click here ---->
        """)
        Label3=wx.StaticText(homepage,-1,"""
                If you want to browse papers in the PC , click here ----> 
        """  )
        Label4=wx.Button(homepage,-1,'Search',(600,205))
        Label4.Bind(wx.EVT_BUTTON,self.OnSearchWindow)
        Label5=wx.Button(homepage,-1,'Browse',(540,260))
        Label5.Bind(wx.EVT_BUTTON,self.OnOpen)
        
        Label1.SetForegroundColour((255,0,0))
        Label2.SetForegroundColour((0,0,255))
        Label3.SetForegroundColour((0,0,255))
        Label4.SetForegroundColour((0,0,255))
        Label5.SetForegroundColour((0,0,255))
        Label1.SetFont(font1)
        Label2.SetFont(font2)
        Label3.SetFont(font2)
        Label4.SetFont(font3)
        Label5.SetFont(font3)
        sizer.Add(Label1,flag=wx.EXPAND)
        sizer.Add(Label2,flag=wx.EXPAND)
        sizer.Add(Label3,flag=wx.EXPAND)
        homepage.Show(True)
    def ShowText(self,evt):
        print "Search"
    def OnClose(self,evt):
        self.taskBarIcon.Destroy()
        self.Close(True)
    def OnOpen(self,evt):
        filterFile = "Python source (*.py)|*.py| All files (*.*)|*.*"         # 过滤文件
        dialog = wx.FileDialog(None, u"选择文件", os.getcwd(), "", filterFile, wx.OPEN)
        dialog.ShowModal()
        dialog.Destroy()  
    def OnSave(self,evt):
        pass
        #self.Close(True)
    def OnSaveAs(self,evt):
        pass
        #self.Close(True)
    def OnPrint(self,evt):
        pass
        #self.Close(True)
    def OnExit(self,evt):
        pass
        #self.Close(True)
    def OnUndo(self,evt):
        pass
        #self.Close(True)
    def OnCut(self,evt):
        pass
        #self.Close(True)
    def OnCopy(self,evt):
        pass
        #self.Close(True)
    def OnPaste(self,evt):
        pass
        #self.Close(True)
    def OnStandard(self,evt):
        pass
        #self.Close(True)
    def OnCustomize(self,evt):
        pass
        #self.Close(True)
    def OnStatusbar(self,evt):
        pass
        #self.Close(True)
    def OnBack(self,evt):
        pass
        #self.Close(True)
    def OnForward(self,evt):
        pass
        #self.Close(True)
    def OnLargest(self,evt):
        pass
        #self.Close(True)
    def OnLarger(self,evt):
        pass
        #self.Close(True)
    def OnMedium(self,evt):
        pass
        #self.Close(True)
    def OnSmaller(self,evt):
        pass
        #self.Close(True)
    def OnSmallest(self,evt):
        pass
        #self.Close(True)
    def OnStop(self,evt):
        pass
        #self.Close(True)
    def OnRefresh(self,evt):
        pass
        #self.Close(True)
    def OnBlue(self,evt):
        pass
        #self.Close(True)
    def OnNative(self,evt):
        pass
        #self.Close(True)
    def OnTan(self,evt):
        pass
        #self.Close(True)
    def OnFlat1(self,evt):
        pass
        #self.Close(True)
    def OnFlat2(self,evt):
        pass
        #self.Close(True)
   
    def OnAbout(self,evt):
    
        dlg=wx.MessageDialog(None,'author geziyang & tangqi \n version 1.0','about',wx.OK)
        dlg.ShowModal()
        
    def OnCreateDatabase(self,evt):
        dlg=wx.TextEntryDialog(None,"input conference id you want to set up database","create database","",style=wx.OK|wx.CANCEL)
        if(dlg.ShowModal()==wx.ID_OK):
            #判断是否存在相应的数据库
            #根据用户输入的名字显示列表
            
            tempdlg=dlg.GetValue()
            print tempdlg
            if(confs.checkUpdate(tempdlg)==False):
                dlg=wx.MessageDialog(None,"database not exist,create it?","create database",wx.YES_NO|wx.ICON_QUESTION)
                if(dlg.ShowModal()==wx.ID_YES):
                    dlg.Destroy()
                    print "creating database"
                    if(self.buildNewDb(tempdlg)):
                        print "build DB successfully!"
                else:
                     print "error"
                    
            if(confs.checkUpdate(tempdlg)==True):
                print "Database Ok!"
    def OnViewConf(self,evt):
        MyGrid1(self)
    def OnViewPaper(self,evt):
        MyGrid2(self)
    def OnDeleteDatabase(self,evt):
        print "delete database"
    def OnDownloadConfig(self,evt):
        downloadconfigdialog=MyDownloadConfigDialog(self,-1,"downloadconfig")
        
    def OnSearchWindow(self,evt):
        MyFrame.searchpage = wx.MDIChildFrame(self, -1, "SearchPage",size=(1000,480))           # 新建子窗口
        MyFrame.searchpage.SetBackgroundColour((255,255,255))
        OnSearchWindows()
class MyCreateDatabase(wx.Frame):                   #显示某个会议的全部信息
    def __init__(self,conf_name):
        wx.Frame.__init__(self,None,-1,"create database",size=(460,320))
        print "searching"
        self.Namelist=confs.getConfName(conf_name)
        print "searching finish!"
        print self.Namelist
        lens=len(self.Namelist)
        self.grid1=wx.grid.Grid(self,-1)
        self.grid1.CreateGrid(lens, 1)
        self.grid1.SetColLabelValue(0,"Name")
        self.grid1.SetRowLabelSize(40)
        self.grid1.SetColSize(0,420)
        row=0
        for key in range(lens):
            self.grid1.SetRowLabelValue(row,str(row+1))
            self.grid1.SetCellValue(row,0,self.Namelist[key][0])
            row+=1
        # 表格的事件
        self.grid1.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)   # 当单击鼠标左键时触发
        self.Show()
        
    def OnCellLeftClick(self,evt):
        conf_home=self.Namelist[evt.GetRow()][1]
        if(confs.checkUpdate(conf_home)==True):
            dlg=wx.MessageDialog(None,"create database will take a long time,go on?","create database",wx.YES_NO|wx.ICON_QUESTION)
            if(dlg.ShowModal()==wx.ID_YES):
                dlg.Destroy()
                print "creating database"
                if(confs.buildNewDb(conf_home)):
                    print "build DB successfully!"
        if(confs.checkUpdate(conf_home)==False):
            dlg=wx.MessageDialog(None,"database already exist","create database",wx.YES_NO|wx.ICON_QUESTION)
            if(dlg.ShowModal()==wx.ID_YES):
                print "creating database"
                dlg.Destroy()
        #buileNewDb(conf_home)

            
class MyGrid1(grid.Grid):                   #显示已索引过的所有的会议

    def __init__(self, parent):

        if(confs.getConfIndex()==False):
            print "No conf indexed!"
        else:
            MyFrame.searchpage.Show(False)
            MyFrame.BackButton=wx.Button(frame,-1,"Back",pos=(900,70),size=(80,25))
            MyFrame.BackButton.Show(False)
            MyFrame.ConfIndex=confs.getConfIndex()
            MyGrid1.lens=len(MyFrame.ConfIndex)
            MyGrid1.colTitles=["ID","Name"]
            grid.Grid.__init__(self, parent, -1,size=(700,300),pos=(300,100))
            self.CreateGrid(MyGrid1.lens, 1)
            self.SetColLabelValue(0,"Name")
            self.SetRowLabelSize(50)
            self.SetColSize(0,650)
            row=0
            for key in MyFrame.ConfIndex:
                self.SetRowLabelValue(row,str(row+1))
                #self.SetCellValue(row,0,key)
                self.SetCellValue(row,0,MyFrame.ConfIndex[key])
                row+=1
        # 表格的事件
            self.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)   # 当单击鼠标左键时触发
    def OnConfDetail(self,evt):
        print self.grid.GetCellValue(evt.GetRow(), evt.GetCol())
        for key in MyFrame.getfiledb:
            if (MyFrame.getfiledb[key].split("###",2)[0]==self.grid.GetCellValue(evt.GetRow(), evt.GetCol())):
                MyFrame.key2=key
                print "key!!!"+MyFrame.key2
        MyConfdetail(frame,MyFrame.key2)
        evt.Skip()
    def Back5(self,evt):
        self.grid.Show(False)
        MyFrame.BackButton.Show(False)
        self.Show(True)
    def OnCellLeftClick(self, evt):
        MyFrame.BackButton.Show(True)
        MyFrame.BackButton.Bind(wx.EVT_BUTTON,self.Back5)
        print "(%d, %d)"%(evt.GetRow(), evt.GetCol())
        print self.GetCellValue(evt.GetRow(), evt.GetCol())
        print self.GetCellValue(evt.GetRow(),0)
        for key in MyFrame.ConfIndex:
            if(self.GetCellValue(evt.GetRow(),0)==MyFrame.ConfIndex[key]):
                MyFrame.key=key
                print "key"+key
        MyFrame.getfiledb=confs.getFileDb(MyFrame.key)

        MyGrid1.lens=len(MyFrame.getfiledb)
        self.Show(False)
        self.grid=wx.grid.Grid(frame,-1,pos=(300,100),size=(700,300))
        self.grid.CreateGrid(MyGrid1.lens, 1)
        self.grid.SetColLabelValue(0,"Name")
        self.grid.SetRowLabelSize(50)
        self.grid.SetColSize(0,650)
       
        row=0
        for i in MyFrame.getfiledb:
           
            self.grid.SetCellValue(row,0,MyFrame.getfiledb[i].split("###",2)[0])
            row+=1
           # 当单击鼠标左键时触发
        self.grid.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, self.OnConfDetail)

        # 表格的事件

        #跳转到指定的会议的页面


class MyGrid2(grid.Grid):                                #显示已下载过的所有的论文

    def __init__(self, parent):
        if(confs.getPaperIndex()==False):
            print "No paper indexed!"
        else:
            MyFrame.searchpage.Show(False)
            MyFrame.PaperIndex=confs.getPaperIndex()
            MyGrid2.lens=len(MyFrame.PaperIndex)
            MyGrid2.colTitles=["ID","title","abstract"]
            grid.Grid.__init__(self, parent, -1,size=(700,300),pos=(300,100))
            self.CreateGrid(MyGrid2.lens, 1)
            self.SetColLabelValue(0,"title")
            self.SetRowLabelSize(50)
            self.SetColSize(0,650)
            row=0
            for key in MyFrame.PaperIndex:
                str1=MyFrame.PaperIndex[key]
                self.key=key
                print (str1)
                self.SetRowLabelValue(row,str(row+1))
                #self.SetCellValue(row,0,key)
                self.SetCellValue(row,0,str1.split("###",2)[0])
                row+=1
        # 表格的事件
            self.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)   # 当单击鼠标左键时触发

    def OnCellLeftClick(self, evt):
        print "(%d, %d)"%(evt.GetRow(), evt.GetCol())
        print self.GetCellValue(evt.GetRow(), evt.GetCol())
        #跳转到指定的会议的页面
        MyPaperdetail(None,self.key)
        evt.Skip()

class MyPaperdetail(wx.Frame):                   #显示某个会议的全部信息
    def __init__(self,parent,conf_home):
        MyPaperdetail.conf_home=conf_home
        wx.Frame.__init__(self,None,-1,size=(460,320))
        label1=wx.StaticText(self,-1,MyFrame.PaperIndex[conf_home].split("###",2)[0],size=(350,40),pos=(20,20))
        button1=wx.Button(self,-1,"open",size=(80,30),pos=(370,20))
        textctrl=wx.TextCtrl(self,-1,MyFrame.PaperIndex[conf_home].split("###",2)[1],style=wx.TE_MULTILINE,size=(400,200),pos=(20,60))
        label2=wx.StaticText(self,-1,"http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber="+conf_home,size=(300,30),pos=(20,280))
        button2=wx.Button(self,-1,"CopyUrl",size=(80,30),pos=(370,280))
        button2.Bind(wx.EVT_BUTTON,self.CopyUrl)
        self.Show(True)
    def CopyUrl(self,URl):
        text=wx.TextDataObject("http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber="+MyPaperdetail.conf_home)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text)
            wx.TheClipboard.Close()
        
class MyConfdetail(wx.Frame):                   #显示某个会议的全部信息
    def __init__(self,parent,conf_home):
        wx.Frame.__init__(self,None,-1,size=(460,320))

        MyFrame.FileDb=confs.getFileDb(conf_home)
        label1=wx.StaticText(self,-1,MyFrame.getfiledb[MyFrame.key2].split("###",2)[0],size=(350,40),pos=(20,20))
        button1=wx.Button(self,-1,"down",size=(80,30),pos=(370,20))
        button1.Bind(wx.EVT_BUTTON,self.Download)
        textctrl=wx.TextCtrl(self,-1,MyFrame.getfiledb[MyFrame.key2].split("###",2)[1],style=wx.TE_MULTILINE,size=(400,200),pos=(20,60))
        self.label2=wx.StaticText(self,-1,"http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber="+MyFrame.key2,size=(300,30),pos=(20,280))
        button2=wx.Button(self,-1,"copy Url",size=(80,30),pos=(370,280))
        button2.Bind(wx.EVT_BUTTON,self.CopyUrl)
        self.Show(True)
    def CopyUrl(self,URl):
        text=wx.TextDataObject("http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber="+MyFrame.key2)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text)
            wx.TheClipboard.Close()
        
    def Download(self,pro_id): 
        OnSearchWindows.key3=pro_id              #####  提供论文下载
        downloadconfigdialog=MyDownloadConfigDialog(MyFrame.searchpage,-1,"downloadconfig")
            
class MyDownloadConfigDialog(wx.Dialog):

    def __init__(self,parent,id,title):
        MyDownloadConfigDialog.downloadhour=""
        MyDownloadConfigDialog.downloadminute=""
        MyDownloadConfigDialog.downloadautoflag=" "
        font=wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.BOLD,False)
        wx.Dialog.__init__(self,parent,id,title,size=(450,150))
        label2=wx.StaticText(self,-1,"time:",(10,30),(60,30))     #用户输入的下载时间
        label2.SetFont(font)
        hourlist=["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
        minutelist=["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59"]
        MyDownloadConfigDialog.choice1=wx.ComboBox(self,-1,str(datetime.datetime.now().hour),(70,30),(60,30),hourlist,wx.CB_DROPDOWN)
        label3=wx.StaticText(self,-1,"hour",(140,35),(50,30))
        MyDownloadConfigDialog.choice2=wx.ComboBox(self,-1,str(datetime.datetime.now().minute),(200,30),(60,30),minutelist)
        label4=wx.StaticText(self,-1,"minute",(270,35),(50,30))
        okbt=wx.Button(self,-1,"OK",(50,70))
        okbt.Bind(wx.EVT_BUTTON,self.OnOK)
        cancelbt=wx.Button(self,-1,"Cancel",(250,70))
        cancelbt.Bind(wx.EVT_BUTTON,self.OnCancel)
        self.ShowModal()
    def timingDown(self,seconds,paper_id):
        time.sleep(seconds)
        #frame.SetStatusText("Starting download...")
        count = 1
        while True:        
            #frame.SetStatusText("trying %d" % count)
            if confs.authCheck("cookies.txt") == True:
                #frame.SetStatusText ("auth success!")
                break
            count += 1
            time.sleep(5)
        if confs.downWithCookies("cookies.txt",paper_id):
            #frame.SetStatusText("download success!")
            return True
        return False

    def threadDown(self,seconds,paper_id):
         thread.start_new_thread(self.timingDown,(seconds,paper_id)) 
    def OnOK(self,evt):
        d1=datetime.datetime.now()
        #print MyDownloadConfigDialog.choice1.GetValue()
        #print MyDownloadConfigDialog.choice2.GetValue()
        d2=d1.replace(hour=int(MyDownloadConfigDialog.choice1.GetValue()),minute=int(MyDownloadConfigDialog.choice2.GetValue())) 
        confs.threadDown((d2-d1).seconds,OnSearchWindows.key3)
        self.Destroy()
        #读取两个文本框的内容和复选框的内容
        
    def OnCancel(self,evt):
        #关闭对话框
        self.Destroy()
        
    def OnPathBrowse(self,evt):
        dirdialog=wx.DirDialog(self,"choose download path","C:\python2.7",wx.DD_DEFAULT_STYLE)
        if dirdialog.ShowModal()==wx.ID_OK:
            self.inputtext1.SetValue(str(dirdialog.GetPath()))
        dirdialog.Destroy()

class OnSearchWindows(wx.MDIParentFrame):

    ResultDict={}    
    def __init__(self):         
        self.Namelist=[]
        MyFrame.searchpage.SetBackgroundColour((158,208,221))
        font1=wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.BOLD,False)
        self.label1=wx.StaticText(MyFrame.searchpage,-1,"Search from web",pos=(20,20))
        self.label1.SetFont(font1)
        self.label1.SetForegroundColour((0,0,255))
        self.button7=wx.Button(MyFrame.searchpage,-1,"Search",pos=(30,135))
        self.button7.Bind(wx.EVT_BUTTON,self.OnSearch)
        self.button8=wx.Button(MyFrame.searchpage,-1,"Exit",pos=(130,135))
        self.button8.Bind(wx.EVT_BUTTON,self.OnExit)
        OnSearchWindows.button9=wx.Button(MyFrame.searchpage,-1,"Back",pos=(900,20),size=(80,25))
        OnSearchWindows.button9.Show(False)
        font2=wx.Font(10,wx.DEFAULT,wx.NORMAL,wx.BOLD,False)    
        label2=wx.StaticText(MyFrame.searchpage,-1,"input conference name",pos=(20,90))
        label2.SetFont(font2)
        self.inputText1=wx.TextCtrl(MyFrame.searchpage,-1,"",pos=(20,110),size=(200,20),style=wx.TE_PROCESS_ENTER)
        self.inputText1.Bind(wx.EVT_TEXT_ENTER,self.OnSearch)
        MyFrame.searchpage.Show(True)
    def OnExit(self,evt):
        print "exit"
        MyFrame.searchpage.Close(True)
    def Download(self,pro_id):               #####  提供论文下载
        downloadconfigdialog=MyDownloadConfigDialog(MyFrame.searchpage,-1,"downloadconfig")
    
    def MoveTo(self,URL):                    #####  跳转到论文下载的界面      第五步
        
        #htmlwin=html.HtmlWindow(frame,-1,pos=(0,22),size=(1024,550))
        print "url  "+self.paperUrl.GetValue()
        text=wx.TextDataObject(self.paperUrl.GetValue())
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text)
            wx.TheClipboard.Close()
        #htmlwin.LoadPage("http://www.google.com")

    def Back4(self,evt):
        self.papertitle.Show(False)
        self.paperabstract.Show(False)
        self.paperUrl.Show(False)
        self.downloadbt.Show(False)
        self.movetobt.Show(False)
        self.grid.Show(True)
        OnSearchWindows.button9.Bind(wx.EVT_BUTTON,self.Back3)
    def detail(self,evt):                 #####   显示论文的全称，摘要和URL                第四步
        OnSearchWindows.button9.Bind(wx.EVT_BUTTON,self.Back4)
        print self.grid.GetCellValue(evt.GetRow(), evt.GetCol())
        for key in OnSearchWindows.ResultDict:
            if (OnSearchWindows.ResultDict[key].split("###",2)[0]==self.grid.GetCellValue(evt.GetRow(), evt.GetCol())):
                OnSearchWindows.key3=key
                print OnSearchWindows.key3
        self.grid.Show(False)
        self.papertitle=wx.StaticText(MyFrame.searchpage,-1,OnSearchWindows.ResultDict[OnSearchWindows.key3].split("###",2)[0],(250,60),(450,40))
        self.paperabstract=wx.TextCtrl(MyFrame.searchpage,-1,OnSearchWindows.ResultDict[OnSearchWindows.key3].split("###",2)[1],(250,100),(650,200),style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_LEFT)
        self.paperUrl=wx.TextCtrl(MyFrame.searchpage,-1,"http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber="+OnSearchWindows.key3,(250,320),(500,25))
        self.downloadbt=wx.Button(MyFrame.searchpage,-1,"download",(800,70))
        self.downloadbt.Bind(wx.EVT_BUTTON,self.Download)
        self.movetobt=wx.Button(MyFrame.searchpage,-1,"copy url",(800,320))
        self.button7.Bind(wx.EVT_BUTTON,self.OnHide1)
        self.movetobt.Bind(wx.EVT_BUTTON,self.MoveTo)
        
    def OnHide1(self,evt):
        self.papertitle.Show(False)
        self.paperabstract.Show(False)
        self.paperUrl.Show(False)
        self.downloadbt.Show(False)
        self.movetobt.Show(False)
        font=wx.Font(12,wx.DEFAULT,wx.NORMAL,wx.NORMAL,True)
        font2=wx.Font(16,wx.DEFAULT,wx.NORMAL,wx.NORMAL,False)
        self.searchflag=wx.StaticText(MyFrame.searchpage,-1,"searching...",(550,170),(630,25))
        self.searchflag.SetForegroundColour((255,145,0))
        self.searchflag.SetFont(font2)
        self.Namelist=confs.getConfName(self.inputText1.GetValue())
        self.searchflag.Show(False)
        MyFrame.searchpage.Show(False)
        self.List={}
        self.bt={}
        for i in range(len(self.Namelist)):
            self.List[i]=wx.TextCtrl(MyFrame.searchpage,-1,self.Namelist[i][0],(250,70+i*30),(630,25))
            self.List[i].SetForegroundColour((30,130,230))
            self.List[i].SetFont(font)
        for j in range(len(self.Namelist)):
            self.bt[j]=wx.Button(MyFrame.searchpage,-1,"ENTER",(900,70+j*30),(80,25),name=self.Namelist[j][1])
            self.bt[j].Bind(wx.EVT_BUTTON,self.OnEnter)
        MyFrame.searchpage.Show(True)
    def Back3(self,evt):
        self.grid.Show(False)
        self.inputkey.Show(True)
        self.inputText2.Show(True)
        self.bt2.Show(True)
        self.text.Show(True)
        OnSearchWindows.button9.Bind(wx.EVT_BUTTON,self.Back2)
    def OnSearchPaper(self,evt):             #####    显示符合关键字的论文名称，供用户点击进入    第三步
        OnSearchWindows.button9.Bind(wx.EVT_BUTTON,self.Back3)
        font=wx.Font(10,wx.DEFAULT,wx.NORMAL,wx.NORMAL,False)
        self.inputkey.Show(False)
        self.inputText2.Show(False)
        self.bt2.Show(False)
        self.text.Show(False)
        resultDict=confs.searchPaper(self.Namelist[0][1],self.inputkey.GetValue().split())        
        OnSearchWindows.ResultDict=resultDict
        self.paperlist={}
        self.detailbt={}
        lens=len(resultDict)
        print lens
        self.grid=wx.grid.Grid(frame,-1,pos=(300,100),size=(700,300))
        self.grid.CreateGrid(lens, 1)
        self.grid.SetColLabelValue(0,"Name")
        self.grid.SetRowLabelSize(50)
        self.grid.SetColSize(0,650)
       
        row=0
        for i in resultDict:
            self.grid.SetCellValue(row,0,resultDict[i].split("###",2)[0])
            row+=1
           # 当单击鼠标左键时触发
        self.grid.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, self.detail)
    def OnCellLeftClick(self, evt):
        print "(%d, %d)"%(evt.GetRow(), evt.GetCol())
        print self.grid.GetCellValue(evt.GetRow(), evt.GetCol())

    def Back2(self,evt):
        self.inputkey.Show(False)
        self.inputText2.Show(False)
        self.bt2.Show(False)
        self.text.Show(False)
        for i in range(len(self.Namelist)):
            self.List[i].Show(True)
        for j in range(len(self.Namelist)):
            self.bt[j].Show(True)
        OnSearchWindows.button9.Bind(wx.EVT_BUTTON,self.Back1)
    def OnEnter(self,evt):                   #####  等待用户输入关键字来查找论文        第二步
        MyFrame.temp=evt.GetEventObject().GetName()
        MyFrame.mythread3=MyThread3(MyFrame.temp)
        MyFrame.mythread3.start()
        for j in range(len(self.Namelist)):
            print self.Namelist[j][1]
        OnSearchWindows.button9.Bind(wx.EVT_BUTTON,self.Back2)
        #判断是否已经存在
        MyFrame.mythread4=MyThread4(self)
        MyFrame.mythread4.start()
    def dlg(self):
        print "showdlg"
        #dlg=MyCreateDBDlg(frame,-1,"Create DB")
        threading.Event().set()
        dlg=wx.MessageDialog(None,"database not exist,create it?","create database",wx.YES_NO|wx.ICON_QUESTION)
        if(dlg.ShowModal()==wx.ID_YES):
                dlg.Destroy()
                print "creating database"
                if(confs.buildNewDb(MyFrame.temp)):
                    print "build DB successfully!"
                else:
                    print "error" 
                    
    def ShowOnSearch1(self):
        for i in range(len(self.Namelist)):
            self.List[i].Show(False)
        for j in range(len(self.Namelist)):
            self.bt[j].Show(False)
        font=wx.Font(12,wx.DEFAULT,wx.NORMAL,wx.NORMAL,False)
        if(MyFrame.mythread3.result==True):
        #if(confs.checkUpdate(temp)==True):
            print "Database OK!"                    
        if(MyFrame.mythread3.result==False):
            print "NO DATABASE YET"
            threading.Event().clear()
            OnSearchWindows.button9.Show(False)
            #self.dlg()
            MyFrame.mythread5=MyThread5(MyFrame.temp)
            MyFrame.mythread5.start()
            MyFrame.mythread6=MyThread6(self)
            MyFrame.mythread6.start()
            '''dlg=wx.MessageDialog(None,"database not exist,create it?","create database",wx.YES_NO|wx.ICON_QUESTION)
            if(dlg.ShowModal()==wx.ID_YES):
                dlg.Destroy()
                print "creating database"
                if(confs.buildNewDb(MyFrame.temp)):
                    print "build DB successfully!"
                else:
                    print "error"                 
                    '''   
        else:
            self.text={}
            self.inputText2=wx.StaticText(MyFrame.searchpage,-1,"please input keyword",(250,180),(300,25))
            self.inputkey=wx.TextCtrl(MyFrame.searchpage,-1,"",(480,180),(100,25))
            self.bt2=wx.Button(MyFrame.searchpage,-1,"search paper",(650,180),(100,25))
            for j in range(len(self.Namelist)):
                if MyFrame.temp==self.Namelist[j][1]:
                    print "show"
                    self.text=wx.StaticText(MyFrame.searchpage,-1,self.Namelist[j][0],(250,100),(700,50),style=wx.TE_CENTER)
                    #self.text.SetForegroundColour((30,130,230))
                    #self.text.SetFont(font)
                    
            #self.inputText2=wx.StaticText(MyFrame.searchpage,-1,"please input keyword",(250,180),(100,25))
            self.inputText2.Bind(wx.EVT_TEXT_ENTER,self.OnSearchPaper)
            #self.inputText2.SetFont(font)
            #self.inputkey=wx.TextCtrl(MyFrame.searchpage,-1,"",(420,180),(100,25))
            self.inputkey.Bind(wx.EVT_TEXT_ENTER,self.OnSearchPaper)
            #self.bt2=wx.Button(MyFrame.searchpage,-1,"search paper",(550,180),(100,25))
            self.button7.Bind(wx.EVT_BUTTON,self.OnHide)
            self.bt2.Bind(wx.EVT_BUTTON,self.OnSearchPaper)
            
    def OnHide(self,evt):
        self.text.Show(False)
        self.inputText2.Show(False)
        self.inputkey.Show(False)
        self.bt2.Show(False)
        font=wx.Font(12,wx.DEFAULT,wx.NORMAL,wx.NORMAL,True)
        font2=wx.Font(16,wx.DEFAULT,wx.NORMAL,wx.NORMAL,False)
        self.searchflag=wx.StaticText(MyFrame.searchpage,-1,"searching...",(550,170),(630,25))
        self.searchflag.SetForegroundColour((255,145,0))
        self.searchflag.SetFont(font2)
        self.Namelist=confs.getConfName(self.inputText1.GetValue())
        self.searchflag.Show(False)
        MyFrame.searchpage.Show(False)
        self.List={}
        self.bt={}
        for i in range(len(self.Namelist)):
            self.List[i]=wx.TextCtrl(MyFrame.searchpage,-1,self.Namelist[i][0],(250,70+i*30),(630,25))
            self.List[i].SetForegroundColour((30,130,230))
            self.List[i].SetFont(font)
        for j in range(len(self.Namelist)):
            self.bt[j]=wx.Button(MyFrame.searchpage,-1,"ENTER",(900,70+j*30),(80,25),name=self.Namelist[j][1])
            self.bt[j].Bind(wx.EVT_BUTTON,self.OnEnter)
        MyFrame.searchpage.Show(True)
    def Back1(self,evt):
        for i in range(len(self.Namelist)):
            self.List[i].Show(False)
        for j in range(len(confs.NAMELIST)):
            self.bt[j].Show(False)
        OnSearchWindows.button9.Show(False)
    def ShowOnSearch(self):
        threading.Event().clear()
        self.Namelist=confs.NAMELIST
        self.List={}
        self.bt={}
        for i in range(len(confs.NAMELIST)):
            self.List[i]=wx.TextCtrl(MyFrame.searchpage,-1,self.Namelist[i][0],(250,70+i*30),(630,25))
            self.List[i].SetForegroundColour((30,130,230))
        for j in range(len(confs.NAMELIST)):
            self.bt[j]=wx.Button(MyFrame.searchpage,-1,"ENTER",(900,70+j*30),(80,25),name=self.Namelist[j][1])
            self.bt[j].Bind(wx.EVT_BUTTON,self.OnEnter)
        OnSearchWindows.button9.Show(True)
        OnSearchWindows.button9.Bind(wx.EVT_BUTTON,self.Back1)
    def LogMessage(self,msg):
        frame.SetStatusText(msg)
        #OnSearchWindows.myshowlabel.SetLabel(msg) 
    def OnSearch(self,evt):                 #####   显示获取的会议的全称　　　　　　 第一步
        font=wx.Font(12,wx.DEFAULT,wx.NORMAL,wx.NORMAL,True)
        font2=wx.Font(16,wx.DEFAULT,wx.NORMAL,wx.NORMAL,False)
        MyFrame.mythread1=MyThread1(self.inputText1.GetValue())
        MyFrame.mythread1.start()
        self.Namelist=confs.NAMELIST
        MyFrame.mythread2=MyThread2(self)
        MyFrame.mythread2.start()
'''class MyCreateDBDlg(wx.Dialog):
    def __init__(self,parent,id,title):
        wx.Dialog.__init__(self,parent,id,title,size=(120,100))
        self.panel=wx.Panel(self)
        self.dlg=wx.MessageDialog(None,"database not exist,create it?","create database",wx.YES_NO|wx.ICON_QUESTION)
        if(self.dlg.ShowModal()==wx.ID_YES):
                self.dlg.Destroy()
                print "creating database"
                if(confs.buildNewDb(MyFrame.temp)):
                    print "build DB successfully!"
                else:
                    print "error"
        self.Show()
    def CreateDB(self,evt):
        print "createDB"
    def CloseDlg(self,evt):
        self.Close()
        '''
class MyThread6(threading.Thread):
    def __init__(self,window):
        threading.Thread.__init__(self)
        self.window=window
    def run(self):
        msg = "creating database ...  "
        i=0
        while (MyFrame.mythread5.isAlive()):
            threading.Event().wait(1)
            wx.CallAfter(self.window.LogMessage, msg+str(i))
            i+=1
        MyFrame.mythread5.join()
        MyFrame.myonsearchwindow.dlg()
class MyThread5(threading.Thread):
    def __init__(self,temp):
        threading.Thread.__init__(self)
        self.temp=temp
    def run(self):
        print "Confs.buildNewDb"
        confs.buildNewDb(MyFrame.temp)
        #MyThread3.result=confs.checkUpdate(self.temp)
class MyThread4(threading.Thread):
    def __init__(self,window):
        threading.Thread.__init__(self)
        self.window=window
    def run(self):
        msg = "Checking database existed or not...  "
        i=0
        while (MyFrame.mythread3.isAlive()):
            threading.Event().wait(1)
            wx.CallAfter(self.window.LogMessage, msg+str(i))
            i+=1
        MyFrame.mythread3.join()
        MyFrame.myonsearchwindow.ShowOnSearch1()
class MyThread3(threading.Thread):
    def __init__(self,temp):
        threading.Thread.__init__(self)
        self.temp=temp
    def run(self):
        MyThread3.result=confs.checkUpdate(self.temp)
class MyThread2(threading.Thread):
    def __init__(self,window):
        self.window=window
        threading.Thread.__init__(self)
    def run(self):
        msg = "Searching...  "
        i=0
        while (MyFrame.mythread1.isAlive()):
            threading.Event().wait(1)
            wx.CallAfter(self.window.LogMessage, msg+str(i))
            i+=1
        MyFrame.mythread1.join()
        MyFrame.myonsearchwindow.ShowOnSearch()
        
class MyThread1(threading.Thread):
    def __init__(self,shortname):
        threading.Thread.__init__(self)
        self.shortname=shortname
    def run(self):
        confs.getConfName(self.shortname)

if __name__=='__main__':
    app=wx.App()
    frame=MyFrame()
    frame.Show()
    app.MainLoop()

