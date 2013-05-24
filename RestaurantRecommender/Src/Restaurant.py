'''
Created on May 24, 2013

@author: Kathy and Richard
'''

from math import sqrt

class Restaurant:
    '''
    Stores information on the restaurant
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.restDict = dict()  #stores the basic info about the restaurant
        self.attributes = dict()  #stores the attributes for the restaurant
        self.reasons = []  #list of reasons for visiting the restaurant
    
    def returnAttributes(self):
        '''
        Returns the attributes for the restaurant
        '''
        return self.attributes
    
    def returnCategories(self):
        '''
        Returns the categories for the restaurant
        '''
        return self.restDict['categories']
    
    def returnReasons(self):
        '''
        Returns the list of reasons for visiting the restaurant
        '''
        return self.reasons   
    
    def appendReason(self, reason):
        '''
        Adds a user's reason for visiting the restaurant to the list of reasons
        '''
        self.reasons.append(reason)
        
    def attributeAdditionFormula(self, base, additive):
        '''
        return the computed addition of the two given attributes
        '''
        return base + additive/(sqrt(abs(base)))
    
    def printAttributes(self):
        '''
        prints the associative array of attributes
        '''
        for attribute in self.attributes.iterkeys:
            print attribute + " => " + self.attributes[attribute]
            
        
    def appendAttributes(self, newAttributes):
        '''
        appends the new attribute list to the existing one and returns a new one
        if no existing value for that attribute, set it
        '''
        for newAttribute in newAttributes.iterkeys:
            if newAttribute in self.attributes:
                self.attributes[newAttribute] = self.attributeAdditionFormula(self.attributes[newAttribute], newAttributes[newAttribute])
            else:
                self.attributes[newAttribute] = newAttributes[newAttribute]
    
