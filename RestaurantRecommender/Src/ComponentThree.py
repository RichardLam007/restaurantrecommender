'''
Created on May 20, 2013

@author: EliteCrew
'''
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

class ComponentThree:
    
    def __init__(self, extractionObject, restaurantManager):
        self.extraction = extractionObject
        self.restaurantAttributes = dict()
        self.restaurantManager = restaurantManager
        
    def processReview(self, reviewText):
        '''
        do a lot of stuff to process a review
        return Attribute object
        '''
        reviewWords = word_tokenize(reviewText)
        taggedWords = pos_tag(reviewWords)
        
        # do a lot more stuff
        adjectives = list()
        reasons = list()
        
        ################
        #NOT WORKING YET
        ################

        
        return adjectives, reasons
        
        
        
    def processReviews(self):
        while True:
            review = self.extraction.nextReview()
            if len(review) == 0:
                return
            newAttributes, newReasons = self.processReview(review['text'])
            
            restaurantObj = self.restaurantManager.returnRestaurant(review['business_id'])
            restaurantObj.appendReasons(newReasons)
            restaurantObj.appendAttributes(newAttributes)