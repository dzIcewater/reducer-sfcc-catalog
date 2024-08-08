from .xmlFile import xmlFile
from .catalogFile import catalogFile
#  catalog file, in or out either. 
class catalogInFile(catalogFile):
    
    def __init__(self, fname,path): 
        isOutFileBool = False
        super().__init__(fname, path, isOutFileBool)