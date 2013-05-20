'''
Created on May 20, 2013

@author: EliteCrew
'''
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

class ComponentThree:
    
    def __init__(self, extractionObject):
        self.extraction = extractionObject
        self.restaurantAttributes = dict()
        
    def processReview(self, reviewText):
        '''
        do a lot of stuff to process a review
        return Attribute object
        '''
        reviewWords = word_tokenize(reviewText)
        taggedWords = pos_tag(reviewWords)
        
        # do a lot more stuff
        
    def processReviews(self):
        while True:
            review = self.extraction.nextReview()
            if len(review) == 0:
                return
            newAttributes = self.processReview(review['text'])
            
            #check if existing attributes exist for restaurant. if exists, grab it
            #append new attributes to existing attributes if exists
            #else set attributes for restaurant