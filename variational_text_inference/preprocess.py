import os 
import pprint
import re
import string
import sys
import numpy as np
import spacy 
from spacy.lang.en.stop_words import STOP_WORDS

import importlib
importlib.reload(sys)

from gensim.parsing.preprocessing import STOPWORDS
STOPWORDS = list(set(STOPWORDS))

nlp = spacy.load('en_core_web_sm') # no need for large model

hand_picked_stop_words = ['rt' , "it's" , 'says' , "doesn't" , "shes" ,"hes" , "she's" ,"he's", u"don't" , "thanks" , "thank's", "like" ,
                         "today" , "time", "know" , "knows" , "help" , "check" , "good", 'must', 'back', 'service' ,
                         'trust', 'yesterday' , 'before' , 'away', 'products', "we're", "bad", "its" ,"it's" , "like" ,
                         'tell', 'talk' , 'wait', 'think','thinks','00pm',"jr's", 'truth','want','wants', 'give','gave',
                         'sure', 'edit', 'may', 'maybe', 'may not', 'might','might not', "we've", 'able', 'go', 'goes',
                         'went', "what's", 'list', 'lists', "can't", 'forever', 'ever', 'says', 'item', "we'd", '#deporthillary',
                         'woud', 'will', 'would', 'mmmmk', "t'was", "ira's", 'sehe', 'haaa', "l'art", 'spss', "bryan's"]



def length_check(  word):
        if '_' in word:
            return word
        else:
            if len(word) >= 17:
                return None
            else:
                return word 

def pre_process_sentence (  sentence ):
    
    text = []
    punct = list(string.punctuation)
    
    #remove punctuation
    for punctuation in punct:
        sentence = sentence.replace(punctuation, '')

    #convert to lowercase and tokenize 
    sentence = nlp.make_doc(str(sentence.lower()))

    #lemmatize
    for token in sentence:
        #remove stop words
        if token.is_stop == False:
            text.append(token.lemma_)
            
    return text



if __name__ == "__main__":
	
	print("Start")
	print(pre_process_sentence('Machine learning testong jsswasxa'))