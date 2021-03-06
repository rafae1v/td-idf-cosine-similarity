#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 08:17:26 2018

@author: Rafael
"""

import re

from unidecode import unidecode
from nltk.corpus import stopwords
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time

#start run time
start = time.time()


stopWords = stopwords.words('english')

def stem_tokens(tokens, ps):
    stemmed = []
    for item in tokens:
        stemmed.append(ps.stem(item))
    return stemmed
ps = PorterStemmer()

def lemmatize_tokens(tokens, wnl):
    lemmatized = []
    for item in tokens:
        lemmatized.append(wnl.lemmatize(item))
    return lemmatized
wnl = WordNetLemmatizer()


query = input('Enter a query: ')

#seperate large text file into documents with an article each
def split_corpus(articleList):
    for article in articleList:                
        seqInfoFile = open( '../%s.txt' % re.sub(r'\W+', '',article[0:19]), 'w')
        seqInfoFile.write(str(article))


#go back to articles and clean it
tokensList = []
def process_articles(articleList):
    for index, articleList in enumerate(articleList):
        tokens = word_tokenize(articleList)
        tokens = stem_tokens(tokens, ps)
        tokens = lemmatize_tokens(tokens, wnl)
        tokensList.append(tokens)
        tokensList[index] = [w for w in tokens if not w in stopWords]
        tokensList[index] = [c for c in tokens if c not in punctuation]

    
def main():
    inputText = open("../train-v2.0.txt")
    inputContent = unidecode(inputText.read())
    inputContent += '\n'+ query
    articleList = inputContent.split("\n\n")
    #split_corpus(articleList)
    process_articles(articleList)

    #make list of counts
    count_vectorizer = CountVectorizer(stop_words=stopWords)
    cv_matrix_train = count_vectorizer.fit_transform(articleList)
    
    #make cosine similarity matrix
    cs_matrix = cosine_similarity(cv_matrix_train, cv_matrix_train)
    cs_matrix[cs_matrix >= 1] = 0
    searchindex = np.where(cs_matrix==np.max(cs_matrix[-1]))
    articleindex = searchindex[-1][1]
    
    #get most similar article
    cs_matrix[cs_matrix ==1] = 0
    print(str(cs_matrix))
    print(np.max(cs_matrix))
    print(articleList[articleindex])
main()
end = time.time()
print(end - start)