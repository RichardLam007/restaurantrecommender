'''
Created on May 20, 2013

@author: EliteCrew
'''
from math import sqrt

class Attributes:
    '''
    Class that contains the adjective attributes for a restaurant
    '''
    
    def __init__(self):
        self.attributes = dict()
        
    def attributeAdditionFormula(self, base, additive):
        '''
        return the computed addition of the two given attributes
        '''
        return base + additive/(sqrt(base))
    
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
        