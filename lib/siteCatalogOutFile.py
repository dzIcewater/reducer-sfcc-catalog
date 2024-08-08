from .xmlFile import xmlFile
from .catalogFile import catalogFile
#  catalog file, in or out either. 
class siteCatalogOutFile(catalogFile):
    
    
    def __init__(self, fname,path): 
        #super(configFile,self).__init__(self._name,self._path)
        isOutFileBool = True
        super().__init__(fname, path, isOutFileBool)
         
        if (self._isOutFileBool == True):
            pass
        else:
            pass # self.readInitialTxt()
    