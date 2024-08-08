from .file import File
from lib.configFile import configFile
from lib.catalogOutFile import catalogOutFile
from lib.filters import filters
from anytree import Node, RenderTree


class dataHolder(object):
    reg = None    
    allCategories       = {}
    onlineCategories    = {}
    categoryAssignments = {}
    masterCatProducts   = {}   #this is after filtering
    variantProducts     = {}
    chosenCategories    = {}
    
    def __init__(self, reg):
        self.reg = reg
        self.initOnlineCategories()
        pass
    
    def initOnlineCategories(self):
        self.allCategories          = {}
        self.onlineCategories       = {}
        self.allCategoriesRootNode  = {}
        self.allCategoriesNodes     = {}
        self.onlineCategoriesNodes  = {}
        self.categoryAssignments    = {}
        self.masterCatProducts      = {}
        self.variantProducts        = {}
        self.chosenCategories       = {}
        self.chosenCategoriesTree   = {}

    #add a category
    def allCategoryAppend(self, catStr, categoryParentStr):
        if catStr == 'shop':
            z=1
        self.allCategories[catStr] = categoryParentStr  #append as a key.
        
    #add an online category
    def onlineCategoryAppend(self, categoryStr, categoryParentStr):
        self.onlineCategories[categoryStr] = categoryParentStr  #append as a key.
    
    def onlineCategoriesNodesAppend(self, categoryStr, categoryParentStr):
        if categoryParentStr == None:
            node = Node(categoryStr)  #root
            self.onlineCategoriesNodes[categoryStr] = node
        else:
            categoryParentStrNode = self.onlineCategoriesNodes[categoryParentStr]
            node = Node(categoryStr, categoryParentStrNode)
            self.onlineCategoriesNodes[categoryStr] = node

    def allCategoriesNodesAppend(self, categoryStr, categoryParentStr):
        node = None
        if categoryParentStr == None:
            node = Node(categoryStr)  #root
            self.allCategoriesRootNode  = node
            self.allCategoriesNodes[categoryStr] = node
        else:
            categoryParentNode = self.allCategoriesNodes[categoryParentStr]
            node = Node(categoryStr, categoryParentNode)
            self.allCategoriesNodes[categoryStr] = node
        return node
    
    def canAppendToAllCategories(self, categoryStr, categoryParentStr):
        if categoryParentStr in self.allCategoriesNodes:
            return True
        return False
        
    #add one cat assignment.
    def categoryAssignmentAppend(self, assignment):
        self.categoryAssignments[assignment['pid']] = assignment['catid']
    
    
    #these are categoryIDs that match actual master products chosen .
    def chosenCategoryAppend(self, chosenCategoryID):
        if chosenCategoryID not in self.chosenCategories:
            self.chosenCategories[chosenCategoryID] =  {} #init 
        self.chosenCategoryAppendLoopUntilRoot(chosenCategoryID)
        #self.chosenCategories[chosenCategoryID][pid] = None
    
    def chosenCategoryAppendLoopUntilRoot(self, chosenCategoryID):
        #go from this cat id, until root, up the chain, appending to the dict. 
        currentCatID = chosenCategoryID
        while currentCatID != 'root':
            self.chosenCategories[currentCatID] = None
            parentCatID = self.allCategories[currentCatID]
            currentCatID = parentCatID
    
        
    def masterCatProductAppend(self, pid):
        self.masterCatProducts[pid.strip()] = None    
        
    def variantProductAppend(self, skuStr):
        self.variantProducts[skuStr.strip()] = None
    
    def allVariantProductsAppendGroup(self, skuStrArr):
        count=0 
        
        for sku in skuStrArr:
            count +=1 
            if self.reg.variantCountWithinMaxVariantCountPerMaster(count):
                self.variantProductAppend(sku)
            else:
                return
    
    
    #returns: t or f
    def productSkuInOnlineCategory(self, pid):
        if pid in self.categoryAssignments:
            assignedCatID = self.categoryAssignments[pid]
            if assignedCatID in self.onlineCategories:
                return True
        return False
    
    def getProductSkuOnlineCategoryAssignmentID(self, pid):
        if pid in self.categoryAssignments:
            assignedCatID = self.categoryAssignments[pid]
            if assignedCatID in self.onlineCategories:
                return assignedCatID
        return False