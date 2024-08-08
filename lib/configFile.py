from .file import File
import json
# the json config file.  
class configFile(File):
    _name='config.json'
    _path='.'
    data = 'uninit'
    
    def __init__(self):
        isOutFileBool = False
        super().__init__(self._name,self._path , isOutFileBool)
        self.loadJson()
    def loadJson(self):
        self.data = json.load( self._fh )
    def printConfig(self):
        print(self.data['catalog'])