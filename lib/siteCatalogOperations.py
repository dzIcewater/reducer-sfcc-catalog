from .file import File
from pathlib import Path
from collections import deque
import xml.sax
import sys
from lib.catalogInFile import catalogInFile
from lib.catalogOutFile import catalogOutFile
from lib.catalogHandlerPass1 import catalogHandlerPass1
from lib.siteCatalogHandlerPass1 import siteCatalogHandlerPass1
from lib.siteCatalogHandlerPass2 import siteCatalogHandlerPass2
from lib.testDataHolder import testDataHolder
from anytree import Node, RenderTree
 

class siteCatalogOperations():
    reg = None
    def __init__(self, reg): 
        self.reg = reg 

    def analyzeSiteCatalog1(self):
        reg = self.reg 
        if reg.DEBUG==1:
            cifilename  = reg.configJson.data['testSitecatalog']
        else:
            cifilename  = reg.configJson.data['testSitecatalog']
        cifilepath  = reg.configJson.data['infilesDir']
        cifilepathPath = Path(cifilepath);
        cifullpath  = cifilepath + '/' + cifilename
        filetoopenPath = cifilepathPath / cifilename
        fh = filetoopenPath.open()
        ch = siteCatalogHandlerPass1(reg) #  get all categories that are 1.   online ,  2. fit our requirements 
        parser = xml.sax.make_parser()
        parser.setContentHandler(ch)
        parser.parse(fh)

        self.buildNodeTree()
 
  
        nodesstr = RenderTree( reg.dataHolder.allCategoriesNodes['root'] )
        onlinecatsDict = reg.dataHolder.onlineCategories
        catassn = reg.dataHolder.categoryAssignments
        acl = len(reg.dataHolder.allCategories.keys())
        cl = len(catassn)
        ocl = len( onlinecatsDict.keys() )
    
    #TODO:   this makes the actual reduced site cat, final step for sitecat. 
    def makeReducedSiteCatalog(self):
        reg = self.reg
        ########  
        print ('makeReducedSiteCatalog  :site cat handler pass 2 - start' )
        sitecathandler = siteCatalogHandlerPass2(reg) #setContentHandler
        sitecathandler.parse()
        print ('makeReducedSiteCatalog  :site cat handler pass 2 - end' )
     
    
    #building entire node tree of site categories. 
    def buildNodeTree(self):
        self.buildNodeTreeHelper(self.reg.dataHolder)
    
    def buildNodeTreeTest(self):
        self.buildNodeTreeHelper(testDataHolder())

    def buildNodeTreeHelper(self, dataHolder):
        
        categories = dataHolder.allCategories
        toProcessCategories = deque() #this is the stack  https://dbader.org/blog/stacks-in-python
        Done = False
        categorieslist =  list(categories)
        index=0
        rootnode = None
        print (sys.version)
        maxindex = len(categorieslist) - 1
        loopcount=0
        while Done == False:
            loopcount+=1
            if loopcount == 1199:
                z=5
            categorySrc = None
            if toProcessCategories:  # means 'if not empty'
                if toProcessCategories[0] == 'shop':
                    z4=1
                category = toProcessCategories.pop()
                if category == 'shop':
                    z3=1
                categorySrc = 'stack'
            else:
                category = categorieslist[index]
                categorySrc = 'list'
                if index < maxindex:
                    index += 1
                else:
                    Done = True
            if Done == False:
                categoryParent = categories[category]
                if categoryParent == None:
                    rootnode = dataHolder.allCategoriesNodesAppend(category,categoryParent)
                else:
                    if dataHolder.canAppendToAllCategories(category,categoryParent):
                        node = dataHolder.allCategoriesNodesAppend(category, categoryParent)
                    else:
                        if category == 'shop':
                            z2=1
                        if categoryParent == 'shop':
                            z3=1
                        toProcessCategories.append(category)
                        toProcessCategories.append(categoryParent)
            