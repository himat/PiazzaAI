import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Reads in the multiple bag of words vectorized data files and returns as a single dictionary
def read_vectorized_data(input_csv, vectorizer_name, limit=None):
    if vectorizer_name == "bag":
        VectorizerEngine = CountVectorizer
    elif vectorizer_name == "tfidf":
        VectorizerEngine = TfidfVectorizer

    print "Reading data with ", vectorizer_name, " format"
    
    if limit == None:
        data = pd.read_csv(input_csv, header=0)
    else:
        data = pd.read_csv(input_csv, header=0, nrows=limit)


    # Shuffle data
    data = data.sample(frac=1).reset_index(drop=True)

    vectorizer = VectorizerEngine(analyzer = 'word', stop_words = 'english')
    
    title_vector = (vectorizer.fit_transform(data['title'])).toarray()
    title_vocab = vectorizer.vocabulary_
    title_dict = vectorizer.get_feature_names()

    body_vector = (vectorizer.fit_transform(data['body'])).toarray()
    body_vocab = vectorizer.vocabulary_
    body_dict = vectorizer.get_feature_names()

    class_vectorizer = VectorizerEngine(analyzer = 'word')
    
    tags_vector = (class_vectorizer.fit_transform(data['tags'])).toarray()
    tags_vocab = class_vectorizer.vocabulary_
    tags_dict = class_vectorizer.get_feature_names()

    vis_vector = (class_vectorizer.fit_transform(data['visibility'])).toarray()
    vis_vocab = class_vectorizer.vocabulary_
    vis_dict = class_vectorizer.get_feature_names()

    # Matches names to feature indices
    vocabs = {'title' : title_vocab,
              'body' : body_vocab,
              'tags' : tags_vocab,
              'visibility' : vis_vocab}
                  
    # Matches indices to feature names
    dicts = {'title' : title_dict,
             'body' : body_dict,
             'tags' : tags_dict,
             'visibility' : vis_dict}

    vectors = {'title' : title_vector,
               'body' : body_vector,
               'tags' : tags_vector,
               'visibility' : vis_vector}

    originals = {'title' : data['title'],
                 'body' : data['body'],
                 'tags' : data['tags'],
                 'visibility' : data['visibility']}

    return (vocabs, dicts, vectors, originals)


