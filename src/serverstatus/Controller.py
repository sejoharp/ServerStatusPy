import Backend
import Gui
import socket
import struct
import threading
import time


class Controller(object):
    
    def __init__(self): 
        self.__backend = Backend.Backend()
        self.__gui = Gui.Gui(self)
        self.__setGuiState(self.ping())
        self.__gui.start()
            
    def toggleServerState(self, widget, data=None):
        if self.ping() == True:
            self.__shutdownServer()
        else:
            thread = self.WakeupWaitingThread(self.__gui, self, int(self.__backend.getRetries()))
            thread.start()
            thread.join()
    
    def __setGuiState(self, available):
        if available == True:
            self.__gui.setStatus(True, self.__getFreeSpace() / (1024 * 1024 * 1024) + " GB")
        else:
            self.__gui.setStatus(False)
            
    def ping(self):   
        try:
            s = socket.create_connection(self.__getAddressTuple(), 5)
            s.close()
            available = True
        except socket.error:
            available = False
        return available      
    
    def __getFreeSpace(self):
        space = None
        try:
            s = self.__getConnection()
            s.send(2)
            space = s.recv(4096)
            s.close()
        except socket.error: 
            space = None
        return space
    
    def __shutdownServer(self):
        try:
            s = self.__getConnection()
            s.send(1)
            s.close()
        except socket.error: 
            pass
        
    def __getConnection(self): 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.__getAddressTuple())
        return s
          
    def __getAddressTuple(self):
        return self.__backend.getAddress(), self.__backend.getPort()
    
    # Wake-On-LAN
    #
    # Copyright (C) 2002 by Micro Systems Marc Balmer
    # Written by Marc Balmer, marc@msys.ch, http://www.msys.ch/
    # This code is free software under the GPL   
    def __wakeOnLan(self):
    
        # Construct a six-byte hardware address
    
        addr_byte = self.__backend.getMac().split(':')
        hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
        int(addr_byte[1], 16),
        int(addr_byte[2], 16),
        int(addr_byte[3], 16),
        int(addr_byte[4], 16),
        int(addr_byte[5], 16))
    
        # Build the Wake-On-LAN "Magic Packet"...
    
        msg = '\xff' * 6 + hw_addr * 16
    
        # ...and send it to the broadcast address using UDP
    
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(msg, ('<broadcast>', 9))
        s.close()
    
    class WakeupWaitingThread(threading.Thread):
        
        def __init__(self, gui, controller, retries):
            threading.Thread.__init__(self)       
            self.__gui = gui
            self.__retries = retries  
            self.__controller = controller
        
        def run(self):
            self.__wakeup()
            
        def __wakeup(self):
            available = False
            #self.__wakeOnLan()
            while (self.__retries > 0) and (available == False):
                available = self.__controller.ping()
                self.__retries = self.__retries - 1
                self.__gui.setServerStatus("waking up (" + str(self.__retries) + ")")
                time.sleep(2)
                print(self.__retries)
            #if available == False:
            #    self.__gui.setServerStatus("wakeup failed")
            #else:
            #    self.__setGuiState(True)
    
if __name__ == "__main__":
    Controller()