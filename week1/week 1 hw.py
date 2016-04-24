# -*- coding: utf-8 -*-
import numpy as np
import codecs
import nltk
import re
from nltk.tokenize import wordpunct_tokenize
from nltk import PorterStemmer


class Corpus():
    
    """ 
    The Corpus class represents a document collection
     
    """
    def __init__(self, doc_data, stopword_file, clean_length):
        """
        Notice that the __init__ method is invoked everytime an object of the class
        is instantiated
        """
        

        #Initialise documents by invoking the appropriate class
        self.docs = [Document(doc[0], doc[1], doc[2]) for doc in doc_data] 
        
        self.N = len(self.docs)
        self.clean_length = clean_length
        
        #get a list of stopwords
        self.create_stopwords(stopword_file, clean_length)
        
        #stopword removal, token cleaning and stemming to docs
        self.clean_docs(2)
        
        #create vocabulary
        self.corpus_tokens()
        
    def clean_docs(self, length):
        """ 
        Applies stopword removal, token cleaning and stemming to docs
        """
        for doc in self.docs:
            doc.token_clean(length)
            doc.stopword_remove(self.stopwords)
            doc.stem()        
    
    def create_stopwords(self, stopword_file, length):
        """
        description: parses a file of stowords, removes words of length 'length' and 
        stems it
        input: length: cutoff length for words
               stopword_file: stopwords file to parse
        """
        
        with codecs.open(stopword_file,'r','utf-8') as f: raw = f.read()
        
        self.stopwords = (np.array([PorterStemmer().stem(word) 
                                    for word in list(raw.splitlines()) if len(word) > length]))
        
     
    def corpus_tokens(self):
        """
        description: create a set of all all tokens or in other words a vocabulary
        """
        
        #initialise an empty set
        self.token_set = set()
        for doc in self.docs:
            self.token_set = self.token_set.union(doc.tokens)

    def document_term_matrix(self):
        """
        description:  returns a D by V array of frequency counts
        """
        # subroutine: computes the counts of each vocabulary in the document
        def counts(doc):
            # initialize a matrix
            term_mat = [0]*len(self.token_set)
            for token in doc.tokens:
                term_mat[list(self.token_set).index(token)] = term_mat[list(self.token_set).index(token)] + 1
            return term_mat;
        
        self.doc_term_matrix = [[counts(doc)] for doc in self.docs]



class Document():
    
    """ The Doc class rpresents a class of individul documents
    
    """
    
    def __init__(self, speech_year, speech_pres, speech_text):
        self.year = speech_year
        self.pres = speech_pres
        self.text = speech_text.lower()
        self.tokens = np.array(wordpunct_tokenize(self.text))
        
        
        
    def token_clean(self,length):

        """ 
        description: strip out non-alpha tokens and tokens of length > 'length'
        input: length: cut off length 
        """

        self.tokens = np.array([t for t in self.tokens if (t.isalpha() and len(t) > length)])


    def stopword_remove(self, stopwords):

        """
        description: Remove stopwords from tokens.
        input: stopwords: a suitable list of stopwords
        """

        
        self.tokens = np.array([t for t in self.tokens if t not in stopwords])


    def stem(self):

        """
        description: Stem tokens with Porter Stemmer.
        """
        
        self.tokens = np.array([PorterStemmer().stem(t) for t in self.tokens])


#1
#Extend the classes to include the following methods:
#document_term_matrix - which returns a D by V array of frequency counts.
#tf_idf - returns a D by V array of tf-idf scores
#dict_rank - returns the top n documents based on a given dictionary and represenation of tokens (eg. doc-term matrix or tf-idf matrix)
#Include subroutines as and when necessary



#2
#Pick a dictionary (or dictionaries) of your choice from the Harvard IV set,
#the Loughran-McDonald set, or some other of your choosing that you think may be
#relevant for the data you collected. Then conduct the following exercise:
#Use the two methods above to score each document in your data.
#Explore whether the scores diﬀer according to the meta data ﬁelds you gathered:
#for example, do diﬀerent speakers/sources/etc tend to receive a higher score
#than others?
#Do the answers to the previous question depend on whether tf-idf weighting is
#applied or not? Why do you think there is (or is not) a diﬀerence in your
#answers?

#3
#We will now do a sentiment analysis using the AFINN list of words.
#AFINN is a list of English words rated for valence with an integer between
#minus five (negative) and plus five (positive). The words have been manually
#labeled by Finn Årup Nielsen in 2009-2011. A positive valence score can be
#interpreted as the word conveying a postive emotion and vice versa.
#Load AFINN-111.txt from ./data/AFINN. Inspect the contents of the file and
#write a function that converts it into a dictionary where the keys are words
#and values are the valence scores attributed to them. You may use the readme
#file for hints.

def get_valence(string):
    '''This function opens the AFINN-111 file and converts it
    into a dictionary with words as keys and valence score as values
    Input: String, a word in the dictionary
    Output: Int, the valence of input word'''

    #open AFINN-111 file as a list
    with open("AFINN-111.txt", "r") as f:
        lines = f.readlines()

    #split by tab
    content = [line.split("\t") for line in lines]

    #create dictionary 
    dictionary = dict((word, int(valence)) for (word,valence) in content)

    return dictionary[string]

#4
#Now, use the presedential speeches from last week's HW to calculate its
#sentiment score. Match every word against the dictionary and come up with a
#metric that captures the sentiment value. If a word is not present mark its
#score as 0. Write a function that takes in a list of word and returns their
#sentiment score. What is the score of the speech you have been assigned?
#Which year, president gave the least and most positive speech?


