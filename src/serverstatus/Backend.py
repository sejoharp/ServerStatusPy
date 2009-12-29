from xml.dom.minidom import parse

class Backend(object):

    def __init__(self):
        self.__address = None
        self.__port = None
        self.__mac = None
        self.__retries = None
    
    def getAddress(self):
        ret = None
        if self.__address == None:
            ret = self.__getAttributeFromDB("address")
        else:
            ret = self.__address
        return ret
    
    def getPort(self):
        ret = None
        if self.__port == None:
            ret = self.__getAttributeFromDB("port")
        else:
            ret = self.__port
        return ret
    
    def getMac(self):
        ret = None
        if self.__mac == None:
            ret = self.__getAttributeFromDB("mac")
        else:
            ret = self.__mac
        return ret

    def getRetries(self):
        ret = None
        if self.__retries == None:
            ret = self.__getAttributeFromDB("retries")
        else:
            ret = self.__retries
        return ret
    
    def __getAttributeFromDB(self, attribute):
        return self.__getTree().getElementsByTagName(attribute).item(0).firstChild.nodeValue
    
    def __getTree(self):
        tree = parse("/home/joscha/workspace/ServerStatusPy/config.xml")
        return tree
        
        
if __name__ == "__main__":
    backend = Backend()
    print(backend.getAddress())
    print(backend.getPort())
    print(backend.getmac())
    print(backend.getRetries())
