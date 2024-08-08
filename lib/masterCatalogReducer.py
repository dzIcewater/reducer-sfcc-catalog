from .file import File
from .catalogFile import catalogFile
from pathlib import Path
import xml.sax

from lib.catalogInFile import catalogInFile
from lib.catalogOutFile import catalogOutFile
from lib.catalogHandlerPass1 import catalogHandlerPass1
from lib.catalogHandlerPass2 import catalogHandlerPass2
from lib.catalogRawHandlerFinalPass import catalogRawHandlerFinalPass 

from lib.productListFile import productListFile


#  catalog file, in or out either.
class masterCatalogReducer( ):
    reg = None
    def __init__(self, reg): 
        self.reg = reg 

    #step 1 : use SAX, loop through the master cat file, making lists for masters, variants, assignments,   etc 
    def makeReducedMasterCatStage1(self,  FILTERDISABLEDBOOL=False):
        reg = self.reg
        if reg.DEBUG==1:
            cifilename  = reg.configJson.data['testCatalog']   #reg.configJson.data['catalog']
        else:
            
            cifilename  = reg.configJson.data['catalog']   #reg.configJson.data['catalog']
        cifilepath  = reg.configJson.data['infilesDir']
        cifilepathPath = Path(cifilepath)
        filetoopenPath = cifilepathPath / cifilename
        
        #ci = catalogInFile(cifilename,cifilepath)
        #co = catalogOutFile('outfiletest.xml'Screenshot from 2021-03-20 22-44-15ndler
        #ci.setTargetOutfileHandler(ofh)
        ch = catalogHandlerPass1(reg, filetoopenPath, FILTERDISABLEDBOOL) #contenthandler
        fh = ch.getFileHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(ch)
        try:
            parser.parse(fh) #  <-note this comes from cifilepath originally.   probably some cleanup of some of those lines needs todo. 
        except Exception as err:
            pass
        print('master cat products filtered, count: ' +  str( len ( reg.dataHolder.masterCatProducts.keys() ) ) )
        print('master cat products:')
        for key1,value1 in   reg.dataHolder.masterCatProducts.items():
            print(key1)
        
    #write masters and variants txt files in output.     
    def writeDataIntermediateFiles(self):
        reg = self.reg
        isWritableBool=True
        mastersProductListFileObj = productListFile(reg, reg.configJson.data['masterListFileName'])
        mastersProductListFileObj.initToWrite()
        mastersProductListFileObj.writeDictKeys(reg.dataHolder.masterCatProducts)  #print the whole list of filtered masters to a file.
        mastersProductListFileObj.close()
        
        variantsProductListFileObj = productListFile(reg, reg.configJson.data['variantListFileName'])
        variantsProductListFileObj.initToWrite()
        variantsProductListFileObj.writeDictKeys(reg.dataHolder.variantProducts)  #print the whole list of filtered masters to a file.
        variantsProductListFileObj.close()
        
        chosenCategoriesListFileObj = productListFile(reg, reg.configJson.data['chosenCategoriesListFilename'])
        chosenCategoriesListFileObj.initToWrite()
        chosenCategoriesListFileObj.writeDictKeys(reg.dataHolder.chosenCategories)  #print the whole list of filtered masters to a file.
        chosenCategoriesListFileObj.close()
 
        allCategoriesListFileObj = productListFile(reg, reg.configJson.data['allCategoriesListFilename'])
        allCategoriesListFileObj.initToWrite()
        allCategoriesListFileObj.writeDictKeys(reg.dataHolder.allCategories)  #print the whole list of filtered masters to a file.
        allCategoriesListFileObj.close()
        
        onlineCategoriesListFileObj = productListFile(reg, reg.configJson.data['onlineCategoriesListFilename'])
        onlineCategoriesListFileObj.initToWrite()
        onlineCategoriesListFileObj.writeDictKeys(reg.dataHolder.onlineCategories)  #print the whole list of filtered masters to a file.
        onlineCategoriesListFileObj.close()
        
        
        
        
        
    #todo: Finish this
    def readDataIntermediateFiles(self):
        reg = self.reg
        mastersProductListFileObj = productListFile(reg, reg.configJson.data['masterListFileName'])
        mastersProductListFileObj.initToRead()
        mastersProductListFileObj.readDictKeys(reg.dataHolder.masterCatProducts)  #print the whole list of filtered masters to a file.
        mastersProductListFileObj.close()
        
        variantsProductListFileObj = productListFile(reg, reg.configJson.data['variantListFileName'])
        variantsProductListFileObj.initToRead()
        variantsProductListFileObj.readDictKeys(reg.dataHolder.variantProducts)  #print the whole list of filtered masters to a file.
        variantsProductListFileObj.close()
        
        chosenCategoriesListFileObj = productListFile(reg, reg.configJson.data['chosenCategoriesListFilename'])
        chosenCategoriesListFileObj.initToRead()
        chosenCategoriesListFileObj.readDictKeys(reg.dataHolder.chosenCategories)  #print the whole list of filtered masters to a file.
        chosenCategoriesListFileObj.close()

        allCategoriesListFileObj = productListFile(reg, reg.configJson.data['allCategoriesListFilename'])
        allCategoriesListFileObj.initToRead()
        allCategoriesListFileObj.readDictKeys(reg.dataHolder.allCategories)  #print the whole list of filtered masters to a file.
        allCategoriesListFileObj.close()

        onlineCategoriesListFileObj = productListFile(reg, reg.configJson.data['onlineCategoriesListFilename'])
        onlineCategoriesListFileObj.initToRead()
        onlineCategoriesListFileObj.readDictKeys(reg.dataHolder.onlineCategories)  #print the whole list of filtered masters to a file.
        onlineCategoriesListFileObj.close()
        
    #use list of masters and variants, and the the raw catalog infile master, and put together output xml file of new reduced master catalog. 
    def makeReducedMasterCatStage2(self):
        reg = self.reg
        #if reg.DEBUG==1:
            #masterCatInfilename  = reg.configJson.data['testCatalog']   #reg.configJson.data['catalog']
        #else:
            #masterCatInfilename  = reg.configJson.data['catalog']   #reg.configJson.data['catalog']
        #masterCatInfilepath  = reg.configJson.data['infilesDir']
        #cifilepathPath = Path(masterCatInfilepath)
        #masterCatalogInfilePathObj = cifilepathPath / masterCatInfilename
        #infileHandler = masterCatalogInfilePathObj.open()
        co = catalogOutFile( reg.configJson.data['masterCatalogOutfile'] , 'outfiles')
        if reg.DEBUG==1:
            cifilename  = reg.configJson.data['testCatalog']   #reg.configJson.data['catalog']
        else:
            cifilename  = reg.configJson.data['catalog']   #reg.configJson.data['catalog']
        cifilepath  = reg.configJson.data['infilesDir']
        cifilepathPath = Path(cifilepath)
        filetoopenPath = cifilepathPath / cifilename #not using !
        fh = filetoopenPath.open() #not using!
        ci = catalogInFile(cifilename,cifilepath)
        # ch2 = catalogHandlerPass2(reg, co) #set up the output    #this doenst work, xmllint shows errors in the output catalog final file. 
        crh = catalogRawHandlerFinalPass(reg, ci, co)
        crh.parse()
        
    