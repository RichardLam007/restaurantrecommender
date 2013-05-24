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
        self.restaurants = []  #stores the set of restaurants
        self.filename = setFilename
    
    def appendRestaurant(self, restaurantObj):
        '''
        Add a restaurant to the set
        '''
        self.restaurants.append(restaurantObj)
        
    def obtainFilename(self):
        '''
        Return the name of the file used to store this object
        '''
        return self.filename
        
    