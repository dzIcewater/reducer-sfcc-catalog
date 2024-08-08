
from lib.registry import registry
 
from lib.xmlFile import xmlFile

from lib.siteCatalogInFile import siteCatalogInFile
from lib.siteCatalogOutFile import siteCatalogOutFile

from lib.siteCatalogOperations import siteCatalogOperations
from lib.masterCatalogReducer import masterCatalogReducer
from lib.productListFile import productListFile

from lib.inventoryOperations import inventoryOperations

from pathlib import Path
import xml.sax
import sys, traceback
 

    
class Main( ):
    
    reg = None  
    
    def __init__(self):
        self.reg = registry()
        reg = self.reg
        reg.masterCatalogReducerObj = masterCatalogReducer(reg) #init the objs. 
        reg.siteCatalogOperationsObj = siteCatalogOperations(reg)
        reg.inventoryOperationsObj   = inventoryOperations(reg)
        pass
    
    
    #this is the standard set of actions . 
    def doPrimary(self):
        print('start main')
        reg = self.reg
        #make reduced sitecat file
        self.siteCatalogPass1() #
        print('makereduced cat start')
        #  TODO:  do chmod or path obj call to chmod to force or ensure (throw exception? ) correct permissions.
        #mcr.writeDataIntermediateFiles()     #not needed -just a debug to make sure the files exist. 
        try:
            reg.masterCatalogReducerObj.makeReducedMasterCatStage1()
            pass
        except Exception as e:
            print(e)
            #exc_type, exc_value, exc_traceback = sys.exc_info()
            #print("*** print_tb:")
            #traceback.print_tb(exc_traceback, limit=5, file=sys.stdout)
            
        print('start writeAllInventoryFilesForSkus')
        reg.inventoryOperationsObj.writeAllInventoryFilesForSkus()
        print('end writeAllInventoryFilesForSkus')
        
        reg.masterCatalogReducerObj.writeDataIntermediateFiles() #write the intermediate files 
        
        reg.masterCatalogReducerObj.readDataIntermediateFiles() #read these in case we want to start from here (and thus not doing makeReducedSitecatMap()
        
        reg.siteCatalogOperationsObj.makeReducedSiteCatalog()
        #filter masters/variants based on site catalog reasonable structure.
        #does raw text parsing as this is the final step.
        reg.masterCatalogReducerObj.makeReducedMasterCatStage2()  #raw parse + write final mastercatalog xml.  
        print ('master products after being filtered, count: ' + str (  len ( reg.dataHolder.masterCatProducts.keys() )   ))
        print('makereducedcat end')
        
        #make reduced inventory file
        #makeReducedInv()
        #make reduced pb file
        #make reduced promotions file
        #upload them and import with ocapi calls
        print('done')

    #make a list of the categories  that are online.  and list of all of them just for comparison. 
    def siteCatalogPass1(self):
        #input is the site catalog file (or a test one);  /infiles/devsitecat.xml   full file
        #out : map of categories online in a map, and a map of pid->category mappings.
        reg = self.reg 
        print('makeReducedSitecatalog start')
        reg.siteCatalogOperationsObj.analyzeSiteCatalog1()
        print('online categories count: ' + str( len(reg.dataHolder.onlineCategories) ) )
        print('all categories count: ' + str(len(reg.dataHolder.allCategories) ) )
        print('category assignments count: ' + str ( len(reg.dataHolder.categoryAssignments) ))

        
        pass

    def makeReducedInv(self):
        pass

 
 
 
    #given we already have a mastercat file in infiles, make the full inventory lists for all those variants. 
    def doMakeInventoryOnlyGivenMasterCat(self):
        reg = self.reg
        print('start doMakeInventoryOnlyGivenMasterCat')
        
        #make unfiltered data lists from master cat. 
        FILTERDISABLEDBOOL=True
        reg.masterCatalogReducerObj.makeReducedMasterCatStage1(FILTERDISABLEDBOOL)

        #load sku lists in mem from existing master cat file,not the temp files we made. 
        
        
        #make the inv lists xml. 
        reg.inventoryOperationsObj.writeAllInventoryFilesForSkus()
        
        
        
        
        
        print('end doMakeInventoryOnlyGivenMasterCat')
  
  
  
  
  
  
  
  
  


# Design:
 
    #reduce catalog size, filter the products, based on : 
    # 1. master product is online
    # 2. master product is searchable 
    # 2. master product is in an online catalog already (sitecatalog)
    # 3. variants of those are included - need final loop for this part too.  put this in the raw loop. 
    
    # steps needed:
    # 1.  grab all masters that are online. and searchable.
    # 2.  grab all the variants that belong to those masters.
    # 3.  inventory > 0 ? not a big problem. do later. 
    # 4.  raw parse grabbing all the product identified.  
    