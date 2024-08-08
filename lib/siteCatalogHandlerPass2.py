from lib.catalogOutFile import catalogOutFile
from lib.catalogInFile import catalogInFile
from pathlib import Path

class siteCatalogHandlerPass2( ):
     
    reg = None        #class var, not instance
    siteCalogOutFile = None
    siteCatalogInFile = None
    
    def __init__(self, reg):
        self.reg = reg
        cifilename  = reg.configJson.data['sitecatalog']   #reg.configJson.data['catalog']
        cifilepath  = reg.configJson.data['infilesDir']
        self.siteCalogOutFile = catalogOutFile( reg.configJson.data['siteCatalogOutfile'] , 'outfiles')
        self.siteCatalogInFile = catalogInFile(cifilename,cifilepath)
    #read entire sitecatalog, parsing raw line by line
    def parse(self): 
        fh = self.siteCatalogInFile.getFileHandler()
        inCategory=0
        targetCurrentCategory = 0
        inCategoryAssignment = 0
        inRecommendation = 0 
        currCategoryAssignmentPID = None
        for line in fh:
            if  '<online-flag>f' in line: 
                line = line.replace('false','true')
            if '<category category-id=' in line:
                inCategory = 1
                currCid = line.split('"')[1]
                if currCid in self.reg.dataHolder.chosenCategories:
                    targetCurrentCategory=1
            elif '<category-assignment category-id=' in line:  #is start 
                inCategoryAssignment = 1
                currCategoryAssignmentPID = line.split('"')[3]
                if currCategoryAssignmentPID == '410923':
                    v=1
            elif '<recommendation source-id=' in line and 'target-id=' in line:
                inRecommendation = 1
                recommendationSrcPID = line.split('"')[1]
                recommendationTargetPID = line.split('"')[5]
            
            if inCategory == 1:
                if targetCurrentCategory == 1:
                    self.writeData(line)
                else:
                    v=1
                    pass
                if '</category' in line:
                    inCategory=0
                    targetCurrentCategory=0
            elif inCategoryAssignment == 1:
                if currCategoryAssignmentPID in self.reg.dataHolder.masterCatProducts:
                    self.writeData(line)
                else:
                    v=1
                    pass
            elif inRecommendation == 1:
                if ( recommendationSrcPID in self.reg.dataHolder.masterCatProducts  or recommendationSrcPID in self.reg.dataHolder.variantProducts) and (recommendationTargetPID in self.reg.dataHolder.masterCatProducts   or recommendationTargetPID in self.reg.dataHolder.variantProducts):
                    self.writeData(line)

            else:  #not in cat or in catassignment, so just print. 
                self.writeData(line)
            
            
            if '</category-assignment' in line or ( '<category-assignment category-id' in line    and    '"/>' in line):
                inCategoryAssignment = 0
                currCategoryAssignmentPID = None
            elif '</recommendation>' in line or (  '<recommendation source-id=' in line and '"/>' in line):
                inRecommendation = 0
                
                       
                
        self.siteCalogOutFile.close()

    def writeData(self, line):
        stripped = line.strip()
        if stripped != '':
            self.siteCalogOutFile.writeString(line)