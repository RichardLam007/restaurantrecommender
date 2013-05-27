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
        
        self.createSets()  #create the different restaurant sets
        self.restaurantSets = self.obtainAllSets()  #fill in the sets with data
    
    def storeSet(self):
        '''
        Store the sets of restaurants into a file
        '''
        for restSet in self.restaurantSets:
            setFilename = self.restaurantSets[restSet].obtainFilename()
            pickle.dump(restSet, open(str(setFilename), 'w'))
    
    def createSets(self):
        '''
        Divides up the restaurants into multiple sets
        '''
        restDict = self.extractor.obtainBussInfo()  #get the dictionary of businesses
        for rest in restDict:
            filename = ord(rest[-1]) #use the ascii value of the last character in the businessID for the filename
            #map each possible filename to a restaurant set
            if filename not in self.restaurantSets:
                self.restaurantSets.update({filename : RestaurantSet.RestaurantSet(filename)})
            self.restaurantSets[filename].appendRestaurant(Restaurant.Restaurant(restDict[rest]), rest)  #add the restaurant to the appropriate set
            
    def obtainSet(self, setIndex):
        '''
        Return the set of restaurants
        '''
        setFilename = self.restaurantSets[setIndex].obtainFilename()
        fileset = pickle.load(open(str(setFilename),'r'))
        return fileset
    
    def obtainAllSets(self):
        '''
        Return all sets of restaurants
        '''
        allSets = dict()
        
        #Generate the dictionary containing all the restaurant sets
        for restSet in self.restaurantSets:
            setFilename = self.restaurantSets[restSet].obtainFilename()
            restSetObj = pickle.load(open(str(setFilename), 'r'))  #Obtain the set from the file
            allSets.update({setFilename : restSetObj})  #Insert this set into a temporary dictionary
        
        return allSets
    
    def returnRestaurant(self, restID):
        '''
        return the Restaurant object for the specified restaurant
        '''
        filename = ord(restID[-1]) #use the ascii value of the last character in the businessID for the filename
        restSet = self.restaurantSets[filename]  #obtain the restaurant set containing this restaurant
        restObj = restSet.returnRestaurantObj(restID)  #obtain the restaurant object
        
        return restObj
        