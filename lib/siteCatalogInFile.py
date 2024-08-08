from .xmlFile import xmlFile
from .catalogFile import catalogFile
#  catalog file, in or out either. 
class siteCatalogInFile(catalogFile):
    
    header = []
    categoryTags = []
    categoryAssignmentTags = []
    targetOutfileHandler = None
    
    def __init__(self, fname,path): 
        #super(configFile,self).__init__(self._name,self._path)
        isOutFileBool = False
        super().__init__(fname, path, isOutFileBool)
        self.iterationTag = 'category' #is this even used? 
        if (self._isOutFileBool == True):
            pass
        else:
            pass # self.readInitialTxt()
    
    def setTargetOutfileHandler(self, targetOutfileHandler):
        self.targetOutfileHandler = targetOutfileHandler
  
    def getTargetOutfileHandler(self):
        return self.targetOutfileHandler
 
      