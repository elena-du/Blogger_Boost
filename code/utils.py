

import pickle
import spacy
import scattertext as st
import re

import matplotlib.pyplot as plt

import spacy
#from spacy import displacy
#from spacy.symbols import amod
from spacy.lang.en.stop_words import STOP_WORDS

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.stem import WordNetLemmatizer

from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

import pyLDAvis
import pyLDAvis.sklearn

import pandas as pd
import numpy as np

import swat
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt
import seaborn as sns

import nltk
#nltk.download()
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string



# Function 1:

def display_topics(model, feature_names, no_top_words, model_type = 'lsa_nmf_lda', topic_names=None):
    '''
    Function automates displaying top words per topic. Function works for LSA, NMF, LDA and Corex models.

    '''
    if model_type == 'lsa_nmf_lda':
        for ix, topic in enumerate(model.components_):
            if not topic_names or not topic_names[ix]:
                print("\nTopic ", ix)
            else:
                print("\nTopic: '",topic_names[ix],"'")
            print(", ".join([feature_names[i]
                            for i in topic.argsort()[:-no_top_words - 1:-1]]))
    elif model_type == 'corex':
        for ix, topic in enumerate(model.alpha):
            if not topic_names or not topic_names[ix]:
                print("\nTopic ", ix)
            else:
                print("\nTopic: '",topic_names[ix],"'")
            print(", ".join([feature_names[i]
                            for i in topic.argsort()[:-no_top_words - 1:-1]]))
    else:
        raise ValueError('Unknown model type')

# Function 2


def remove_stop_words(comment_line):
    '''
    Preprocessing step: removing stop words.

    '''
    stop_words = set(stopwords.words('english'))
    token_words=word_tokenize(str(comment_line))
    filtered_comment_line = [w for w in token_words if not w in stop_words]

    return " ".join(filtered_comment_line)


#Function 3

# inspired by https://blog.cambridgespark.com/tutorial-build-your-own-embedding-and-use-it-in-a-neural-network-e9cde4a81296

def word_splt(lst):
    return list(map(lambda word:[word], lst))

def lemmatize_sent(sent):
    lemmatizer=WordNetLemmatizer()
    return [lemmatizer.lemmatize(word.lower()) for word in sent]

def embedd_by_topic(ind):
    text = new_df_g['post'][ind]

    text_l = text.split('.')
    text_l=word_splt(text_l)
    tokens = [sub.split() for subl in  text_l for sub in subl]

    lemmatized = []
    for i in tokens:
        lemmatized.append(lemmatize_sent(i))


    embedding_dim=300

    w_v = Word2Vec(lemmatized, size=embedding_dim, window=5,
                   min_count=5, negative=15, iter=10, workers=multiprocessing.cpu_count())

    word_vectors = w_v.wv

    return word_vectors
