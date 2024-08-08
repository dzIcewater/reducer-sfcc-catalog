from main import Main


class m():
 
    def __init__(self):
        pass
         
    def do(self):
        print('bla')
        
    def doPrimary(self): #makes reduced mastercatalog, sitecat, 
        mymain = Main()
        mymain.doPrimary()
        
    def doMakeInventoryOnlyGivenMasterCat(self):
        mymain = Main()
        mymain.doMakeInventoryOnlyGivenMasterCat()
        
        
        
print('begin run')     
main = m() #instatiate my configurable class here. 
main.doMakeInventoryOnlyGivenMasterCat()   #do the specific task i want from the m() class.
print('finished')