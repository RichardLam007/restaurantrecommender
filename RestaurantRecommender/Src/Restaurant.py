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
        self.reasons = dict()  #stores the reasons for visiting the restaurant
        self.rank = 0  #store the overall rank of the restaurant
    
    def returnAttributes(self):
        '''
        Returns the attributes for the restaurant
        '''
        return self.attributes
    
    def returnRestaurantData(self, dataCategory):
        '''
        Returns the requested data for the restaurant
        '''
        return self.restDict[dataCategory]
    
    def returnReasons(self):
        '''
        Returns the list of reasons for visiting the restaurant
        '''
        return self.reasons   
    
    def appendReasons(self, visitReasons):
        '''
        Adds the reasons users visit the restaurant
        '''
        for vReason in visitReasons:
            if vReason in self.reasons:
                self.reasons[vReason] = self.additionFormula(self.reasons[vReason], visitReasons[vReason])  
            else:
                self.reasons[vReason] = visitReasons[vReason]              
        
    def additionFormula(self, base, additive):
        '''
        return the computed addition of the two given attributes/reasons
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
                self.attributes[newAttribute] = self.additionFormula(self.attributes[newAttribute], newAttributes[newAttribute])
                self.rank = self.attributes[newAttribute]
            else:
                self.attributes[newAttribute] = newAttributes[newAttribute]
    
    def returnRank(self):
        '''
        Return the overall rank for the restaurant based on the attributes for it
        '''
        return self.rank
        