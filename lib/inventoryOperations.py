from .file import File
from .inventoryHandlerPass1 import inventoryHandlerPass1
class inventoryOperations():
    reg = None
    def __init__(self, reg): 
        self.reg = reg 

    def writeAllInventoryFilesForSkus(self):
        inventoryHandlerPass1Obj = inventoryHandlerPass1(self.reg)
        inventoryHandlerPass1Obj.writeAllForAllInventoryLists()
        