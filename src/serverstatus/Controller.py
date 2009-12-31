import Backend
import Gui
import socket
import struct
import sys
import threading
import time


class Controller(object):
    
    def __init__(self): 
        self.__backend = Backend.Backend()
        self.__gui = Gui.Gui(self)
        self.__gui.setStatus(Controller.ping(self.__getAddressTuple()))
        self.__gui.start()
            
    def toggleServerState(self, widget, data=None):
        if Controller.ping(self.__getAddressTuple()) == True:
            self.__shutdownServer()
            self.exitProgam()
        else:
            thread = self.WakeupWaitingThread(self.__gui, int(self.__backend.getRetries()), self.__getAddressTuple(), self.__backend.getMac())
            thread.start()
            #thread.join()
    
    def exitProgam(self):
        sys.exit(0)
        
    @staticmethod    
    def ping(addressTuple):   
        try:
            s = socket.create_connection(addressTuple, 1)
            s.close()
            available = True
        except socket.error:
            available = False
        return available      
    
    def getFreeSpace(self):
        space = None
        try:
            s = self.__getConnection()
            s.send(str(2) + "\n")
            space = s.recv(128)
            s.close()
        except socket.error: 
            space = None
        return space
    
    def __shutdownServer(self):
        try:
            s = self.__getConnection()
            s.send(str(1)+ "\n")
            s.close()
        except socket.error: 
            pass
        
    def __getConnection(self): 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.__getAddressTuple())
        return s
          
    def __getAddressTuple(self):
        return self.__backend.getAddress(), int(self.__backend.getPort())
    
    class WakeupWaitingThread(threading.Thread):
        
        def __init__(self, gui, retries, addressTuple, mac):
            threading.Thread.__init__(self)       
            self.__gui = gui
            self.__retries = retries
            self.__addressTuple = addressTuple
            self.__mac = mac
        
        def run(self):
            self.__wakeup()
            
        def __wakeup(self):
            available = False
            self.__gui.enableButton(False)
            self.__wakeOnLan()
            while (self.__retries > 0) and (available == False):
                available = Controller.ping(self.__addressTuple)
                self.__retries = self.__retries - 1
                self.__gui.setStatusWhileWakingUp(self.__retries)
                time.sleep(1)
            if available == False:
                self.__gui.setStatusWakeupFailed()
            else:
                self.__gui.setStatus(True)
            self.__gui.enableButton(True)
        
        # Wake-On-LAN
        #
        # Copyright (C) 2002 by Micro Systems Marc Balmer
        # Written by Marc Balmer, marc@msys.ch, http://www.msys.ch/
        # This code is free software under the GPL   
        def __wakeOnLan(self):
        
            # Construct a six-byte hardware address
        
            addr_byte = self.__mac.split(':')
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
    
if __name__ == "__main__":
    Controller()
