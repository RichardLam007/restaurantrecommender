'''
Created on Apr 25, 2013

@author: EliteCrew
'''
    
import csv
import urllib2
import json

class Vocabulary(object):

    def __init__(self, synonymFileName, antonymFileName, visitTypesFileName, possibleAdjectivesToAddFile):  
        
        '''
        Constructor
        '''
        self.synonymList = [] #attribute list + synonyms
        self.antonymList = []
        self.visitTypesList = []
        
        self.synonymDict = dict()
        self.antonymDict = dict()
                
        self.synonymFileName = synonymFileName
        self.antonymFileName = antonymFileName
        self.visitTypesFileName = visitTypesFileName
        
        self.possibleAdjectivesToAddFile = possibleAdjectivesToAddFile
        
        self.apiRequest = "http://words.bighugelabs.com/api/2/3a44e9c4e799329f75b03083cf41a457/$/json"
        self.__loadFromFiles__()
        self.synonymDict = self.createLookupDictionary(self.synonymList)
        self.antonymDict = self.createLookupDictionary(self.antonymList, True)
            
    def createLookupDictionary(self, TwoDWordList, excludeFirst = False):
        '''
        Generates and returns a dictionary object to do a reverse lookup from a 2 dimensional list
        For example:
        Input: [{'a', 'a1', 'a2'} {'b', 'b1', 'b2'}]
        Return: ['a' => 'a', 'a1' => 'a', 'a2' => 'a', 'b' => 'b', 'b1' => 'b', 'b2' => 'b']
        
        If excludeFirst is True, then dictionary will not have the first word in each row point to itself
        '''
        lookUpDict = dict()
        
        for row in TwoDWordList:
            for word in row:
                if not excludeFirst or not word == row[0]:
                    lookUpDict[word] = row[0] #add an entry in the dict in which the synonym maps to the adjective attribute (first word in each row)
        return lookUpDict
        
    def __loadFromFiles__(self):
        '''
        Loads words from csv and txt files
        '''
        f = open(self.synonymFileName, "rb")
        reader = csv.reader(f)
        for row in reader:
            self.synonymList.append(row)
        f.close()
        
        f = open(self.antonymFileName, "rb")
        reader = csv.reader(f)
        for row in reader:
            self.antonymList.append(row)
        f.close()

        f = open(self.visitTypesFileName, "r")
        for line in f:
            self.visitTypesList.append(line.rstrip('\n')) 
        f.close()
            
    def isReasonForVisit(self, word):
        '''
        Returns true if the specified word is a reason for visiting
        '''
        if word in self.visitTypesList:
            return True
        else:
            return False
    
    def getMatchingAdjective(self, word):
        '''
        Returns attribute if the specified word is an adjective found in the attribute list or a synonym of the attribute list
        '''  
        if word in self.synonymDict:
            return self.synonymDict[word]
        else:
            self.dumpPossibleNewAdjective(word)
            return None

       
    def getMatchingAntonymAdjective(self, word):
        '''
        Returns original (positive) attribute if the specified word is an adjective found in the antonym list 
        '''
        if word in self.antonymDict:
            return self.antonymDict[word]
        else:
            self.dumpPossibleNewAdjective(word)
            return None
    
    def saveSynonymAntonymLists(self):
        '''
        Saves lists to file for future use
        '''
        f = open(self.synonymFileName, "wb")
        for synonymRow in self.synonymList:
            f.write(",".join(synonymRow) + "\n")
        f.close()
        
        f = open(self.antonymFileName, "wb")
        for antonymRow in self.antonymList:
            f.write(",".join(antonymRow) + "\n")
        f.close()


    def getSynonymsAndAntonymsNewWords(self):
        '''
        Fills the synonyms and antonyms list for adjectives without synonyms only
        '''
        i = 0
        for synonyms in self.synonymList:
            if synonyms.__len__() == 1:
                retrieved = urllib2.urlopen(self.apiRequest.replace("$", synonyms[0]))
                results = json.loads(retrieved.read())
                if "adjective" in results:
                    if "syn" in results['adjective']:
                        self.synonymList[i] = self.synonymList[i] + results['adjective']['syn']
                        if "ant" in results['adjective']:
                            self.antonymList.append([synonyms[0]] + results['adjective']['ant'])
            i+=1

    def getAllNewSynonymsAndAntonyms(self):
        '''
        Fills the synonyms and antonyms list. Will overwrite all synonyms
        '''
        i = 0
        for synonyms in self.synonymList:
            retrieved = urllib2.urlopen(self.apiRequest.replace("$", synonyms[0]))
            results = json.loads(retrieved.read())
            self.synonymList[i] = [self.synonymList[i][0]]
            if "adjective" in results:
                if "syn" in results['adjective']:
                    self.synonymList[i] = self.synonymList[i] + results['adjective']['syn']
                if "ant" in results['adjective']:
                    self.antonymList.append([synonyms[0]] + results['adjective']['ant'])
            i+=1
                    
    def debugLists(self):
        print "Synonyms list:"
        for synonymsRow in self.synonymList:
            print synonymsRow
        print
        print "Antonyms List:"
        for antonymsRow in self.antonymList:
            print antonymsRow
        print
        print "Visit type List:"
        for visitType in self.visitTypesList:
            print visitType
        print 
        
    def debugDicts(self):  
        print "Synonyms dict:"
        for synonymKey in self.synonymDict.iterkeys():
            print synonymKey + " => " + self.synonymDict[synonymKey]
        print 
        print "Antonyms dict:"
        for antonymKey in self.antonymDict.iterkeys():
            print antonymKey + " => " + self.antonymDict[antonymKey]
        
    def dumpPossibleNewAdjective(self, word):
        f = open(self.possibleAdjectivesToAddFile, "r")
        if not word in f.read():
            f.close()
            f = open(self.possibleAdjectivesToAddFile, "a")
            f.write(word + "\n")
        f.close()