'''
Created on May 24, 2013

@author: Kathy
'''
class RestaurantSet:
    '''
    Class that contains a specific set of restaurants
    '''
    def __init__(self, setFilename):
        '''
        Constructor
        '''
        self.restaurants = dict()  #stores the set of restaurants
        self.filename = setFilename
        
    def debug(self):
        print "debugging restaurant set: " + self.filename
        print "restaurant IDs: "
        for restaurantID in self.restaurants:
            print restaurantID 
        print
    
    def appendRestaurant(self, restaurantObj, restID):
        '''
        Add the restaurant to the set
        '''
        self.restaurants.update({restID : restaurantObj})
        
    def obtainFilename(self):
        '''
        Return the name of the file used to store this object
        '''
        return self.filename
    
    def returnRestaurants(self):
        '''
        Return the dictionary of all the restaurants within this set
        '''
        return self.restaurants
    
    def returnRestaurantObj(self, restID):
        '''
        Return the Restaurant object for the specified restaurant
        '''
        if restID not in self.restaurants:
            return None
        return self.restaurants[restID]
        
    