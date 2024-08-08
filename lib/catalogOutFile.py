from .xmlFile import xmlFile
from .catalogFile import catalogFile
#  catalog file, in or out either. 
class catalogOutFile(catalogFile):
    
    def __init__(self, fname,path): 
        isOutFileBool = True
        super().__init__(fname, path, isOutFileBool)
         
       