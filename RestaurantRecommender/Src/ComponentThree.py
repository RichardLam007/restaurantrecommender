'''
Created on May 20, 2013

@author: EliteCrew
'''
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

class ComponentThree:
    
    def __init__(self, extractionObject, vocabularyObject, restaurantManagerObject):
        self.extraction = extractionObject
        self.vocabularyObject = vocabularyObject
        self.restaurantAttributes = dict()
        self.restaurantManager = restaurantManagerObject
        
    def processReview(self, reviewText):
        '''
        Given the text of a review, returns a dictionary of adjectives and list of reasons for visiting
        return Attribute object
        '''
        reviewWords = word_tokenize(reviewText)
        taggedWords = pos_tag(reviewWords)
        # do a lot more stuff
        adjectives = dict()
        reasons = list()
        
        for row in taggedWords:
            word = row[0]
            POS = row[1]
            if POS in ["JJ", "JJR"]:
                adjective = self.vocabularyObject.getMatchingAdjective(word)
                if not adjective == None:
                    adjectives[word] = 1
                else:
                    adjective = self.vocabularyObject.getMatchingAntonymAdjective(word)
                    if not adjective == None:
                        adjectives[word] = -1
            if POS in ["NN", "NNS", "FW"]
                if self.vocabularyObject.isReasonForVisit(word):
                    reasons.append(word)
        ################
        # NOT DONE YET
        ################
        return adjectives, reasons
        
    def processReviews(self):
        '''
        Loops through all available reviews from extraction object, processes them, and pushes results into the appropriate restaurant objects
        '''
        while True:
            review = self.extraction.nextReview()
            if len(review) == 0:
                return # no more
            newAttributes, newReasons = self.processReview(review['text'])
            
            restaurantObj = self.restaurantManager.returnRestaurant(review['business_id'])
            restaurantObj.appendReasons(newReasons)
            restaurantObj.appendAttributes(newAttributes)