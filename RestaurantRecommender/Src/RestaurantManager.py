'''
Created on May 24, 2013

@author: Kathy
'''
import pickle, RestaurantSet, Restaurant

class RestaurantManager:
    '''
    Class that handles the different sets of restaurants
    '''
    def __init__(self, extObj):
        '''
        Constructor
        '''
        self.restaurantSets = dict()  #stores the restaurant sets
        self.extractor = extObj #the Extraction object to retrieve the restaurant info
    
    def storeSet(self):
        '''
        Store the sets of restaurants into a file
        '''
        for restSet in self.restaurantSets:
            setFilename = self.restaurantSets[restSet].obtainFilename()
            pickle.dump(restSet, open(setFilename, 'w'))
    
    def createSets(self):
        '''
        Divides up the restaurants into multiple sets
        '''
        restDict = self.extractor.obtainBussInfo()
        for rest in restDict:
            filename = ord(rest[-1])
            if filename not in self.restaurantSets:
                self.restaurantSets.update({filename : RestaurantSet(filename)})
            self.restaurantSets[filename].appendRestaurant(Restaurant(rest))
            
    def obtainSet(self, setIndex):
        '''
        Return the set of restaurants
        '''
        setFilename = self.restaurantSets[setIndex].obtainFilename()
        fileset = pickle.load(open(setFilename,'r'))
        return fileset
    
    def obtainAllSets(self):
        '''
        Return all sets of restaurants
        '''
        allSets = dict()
        
        for restSet in self.restaurantSets:
            setFilename = self.restaurantSets[restSet].obtainFilename()
            restSetObj = pickle.load(open(setFilename, 'r'))
            allSets.update({setFilename.split(".")[0] : restSetObj})
        
        return allSets
        