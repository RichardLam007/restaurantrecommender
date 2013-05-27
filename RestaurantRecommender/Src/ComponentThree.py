'''
Created on May 20, 2013

@author: EliteCrew
'''
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from math import sqrt

class ComponentThree:
    
    def __init__(self, extractionObject, vocabularyObject, restaurantManagerObject, debug = False):
        self.debug = debug
        self.extraction = extractionObject
        self.vocabularyObject = vocabularyObject
        self.restaurantAttributes = dict()
        self.restaurantManager = restaurantManagerObject
        
        
    def additionFormula(self, base, additive):
        '''
        return the computed addition of the two given attributes/reasons
        '''
        if base < 1:
            return additive
        return base + additive/(sqrt(abs(base)))
        
    def processReview(self, reviewText):
        '''
        Given the text of a review, returns a dictionary of adjectives and list of reasons for visiting
        return Attribute object
        '''
        reviewWords = word_tokenize(reviewText)
        taggedWords = pos_tag(reviewWords)
        adjectives = dict()
        reasons = dict()
        
        previousPreviousWord = None
        previousWord = None
        
        for row in taggedWords:
            if self.debug == True:
                print row
            word = row[0].lower()
            POS = row[1]
            negator = 1
            
            if previousPreviousWord in ['no', 'not', 'bad', 'terrible', 'horrible', 'worst']:
                negator = -1
            
            if POS in ["JJ", "JJR"]: #if verbs
                adjective = self.vocabularyObject.getMatchingAdjective(word) #check for adjective via synonym
                if not adjective == None:
                    if word in adjectives:
                        adjectives[word] = self.additionFormula(adjectives[word], 1*negator)
                    else:
                        adjectives[word] = 1*negator
                else:
                    adjective = self.vocabularyObject.getMatchingAntonymAdjective(word) #check for adjective via antonym
                    if not adjective == None:
                        if word in adjectives:
                            adjectives[word] = self.additionFormula(adjectives[word], -1*negator)
                        else:
                            adjectives[word] = -1*negator
            if POS in ["NN", "NNS", "FW"]: #if noun, foreign word
                if self.vocabularyObject.isReasonForVisit(word):
                    if word in reasons:
                        reasons[word] = self.additionFormula(reasons[word], 1*negator)
                    else:
                        reasons[word] = 1*negator
                        
            previousWord = word
            previousPreviousWord = previousWord
        ################
        # NOT DONE YET
        ################
        return adjectives, reasons
        
    def processReviews(self, maxNumber):
        '''
        Loops through all available reviews from extraction object, processes them, and pushes results into the appropriate restaurant objects
        '''
        reviewCount = 0
        while reviewCount < maxNumber:
            reviewCount += 1
            print "processing review count: " + str(reviewCount)
            review = self.extraction.nextReview()
            if len(review) == 0:
                return # no more
            newAttributes, newReasons = self.processReview(review['text'])
            
            restaurantObj = self.restaurantManager.returnRestaurant(review['business_id'])
            if not restaurantObj == None:
                restaurantObj.appendReasons(newReasons)
                restaurantObj.appendAttributes(newAttributes)
            
            