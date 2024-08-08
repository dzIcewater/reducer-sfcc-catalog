from .file import File
from .catalogFile import catalogFile
from pathlib import Path

#  catalog file, in or out either.
class productListFile(File):      #holds masters or variants. 
    reg = None
    
    def __init__(self, reg, productListFileName): 
        self.reg = reg
        fname = productListFileName
        path = reg.configJson.data['outfilesDir']
        super().__init__(fname, path, None)
                  
    def writeDictKeys(self, inDict):
        #write this dict to the file.   keys only
        for key1,value1 in    inDict.items():
            self.writeString(key1 + '\n')
        self.close()

    def readDictKeys(self, targetObj):
        for line in self._fh:
            targetObj[line.strip()] = None
        
        
    def getDict(self):
        outDict = {}
        for line in self._fh:
            outDict[line.strip()] = None
        return outDict