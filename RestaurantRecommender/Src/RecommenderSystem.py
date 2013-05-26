'''
Created on May 26, 2013

@author: Kathy
'''
import traceback, sys, Recommendation, RestaurantManager, Extraction, ComponentThree, Vocabulary, time

def main():
    #request for the user to input a userID
    userid = raw_input("Enter the userID of the user to be recommended: ")
    
    userid = "JkeCKyEaQlbLd9uZYl4DjA"  #used for testing
    overallstart = time.clock()
    
    #Component #1: retrieve the necessary words used to analyze the reviews
    print 'Performing Component #1'
    start = time.clock()
    vocab = Vocabulary.Vocabulary('../config/synonyms.csv', '../config/antonyms.csv', '../config/visit_wordlist.txt', '../config/possible_adjectives.txt')
    vocab.saveSynonymAntonymLists()
    end = time.clock()
    print 'Component #1 took: ' + str(end-start) + 'seconds'
    
    #Component #2: extract the information from the dataset
    print 'Performing Component #2'
    start = time.clock()
    ext = Extraction.Extraction('tmpNFvucr', 'userinfo.json', 'busInfo.json')
    #ext.extractInfo()
    end = time.clock()
    print 'Component #2 took: ' + str(end-start) + 'seconds'
    
    #Component #3: analyze the reviews
    print 'Performing Component #3'
    start = time.clock()
    restManager = RestaurantManager.RestaurantManager(ext)
    restManager.createSets()  #create the needed RestaurantSet and Restaurant objects
    compThree = ComponentThree.ComponentThree(ext, vocab, restManager)
    compThree.processReviews()  #fill in the objects with information
    restManager.storeSet()  #store the objects
    end = time.clock()
    print 'Component #3 took: ' + str(end-start) + 'seconds'
    
    #Component #4: use the previous results to determine the top-N results to recommend to the user
    print 'Performing Component #4'
    start = time.clock()
    rec = Recommendation.Recommendation(userid, ext, restManager, 10)
    topResults = rec.recommendRestaurants()
    end = time.clock()
    print 'Component #4 took: ' + str(end-start) + 'seconds'

    #display the top-N results
    print 'Recommending to: ' + userid
    for result in topResults:
        print 'Name: ' + result[0] + '  Ranking Value: ' + str(result[1])
    
    
    overallend = time.clock()
    print 'The overall recommendation time took: ' + str(overallend - overallstart) + 'seconds'
    
if __name__ == '__main__':
    try:
        main()
    except:
        print 'Error: ', str(sys.exc_info()[0])
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print 'Description: ', str(exc_value)
        traceback.print_tb(exc_traceback, limit=10, file=sys.stdout)