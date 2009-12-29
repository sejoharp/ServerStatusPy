'''
Created on Dec 25, 2009

@author: joscha
'''
import gtk
import pygtk
pygtk.require('2.0')

class Gui(object):
    '''
    classdocs
    '''

    def setStatus(self, status, space = None):
        if status == True:
            self.__textStatus.set_text("online")
            self.__buttonToggle.set_label("shutdown")
            self.__textSpace.set_label(space)
        else:
            self.__textStatus.set_text("offline")
            self.__buttonToggle.set_label("wake up")
            self.__textSpace.set_label("unkown")
            
    def setServerStatus(self, msg):
        self.__textStatus.set_text(msg)
        
    def setSpace(self, space):
        self.__textSpace.set_text(space)
    
    def __destroy(self, widget, data=None):
        gtk.main_quit()
  
    def __init__(self, controller): 
        self.__controller = controller 
        self.__win = gtk.Window()
        grid = gtk.Table(3,2,True)
        self.__buttonToggle = gtk.Button()
        labelStatus = gtk.Label("server status: ")
        labelSpace = gtk.Label("available space: ")
        self.__textSpace = gtk.Label()
        self.__textStatus = gtk.Label()
        self.__buttonToggle.connect("clicked", self.__controller.toggleServerState, None)
        self.__win.connect("destroy", self.__destroy)
        
        ###
        ##  This grid:
        ##  0        1        2
        ##  ------------------- 0
        ##  |    b1  |        |
        ##  ------------------- 1
        ##  |        |   b2   |
        ##  ------------------- 2
        ##  |       b3        |1,2
        ##  ------------------- 3
        ###
        
        #put buttons into the table
        grid.attach(self.__textStatus,1,2,0,1)
        grid.attach(self.__textSpace,1,2,1,2)
        grid.attach(self.__buttonToggle,0,2,2,3)
        grid.attach(labelStatus,0,1,0,1)
        grid.attach(labelSpace,0,1,1,2)
        
        self.__win.add(grid)
        
        self.__win.show_all()

    def start(self):
        gtk.main()

        