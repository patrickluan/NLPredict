from numpy import array
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from nltk.corpus import words
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import matplotlib.pyplot as plt

import utility

def process_file(file_name):
    filtered =[]
    stop_words=set(stopwords.words("english"))
    stemmed =[] 
    with open(file_name, encoding='utf-8', errors='surrogateescape') as f:
        text = f.read()
    tokenized_word=word_tokenize(text)
    #filter the stop words 
    for word in tokenized_word:
        if(word not in stop_words):
            filtered.append(word) 
    #convert to stemmed word
    ps = PorterStemmer()
    for word in filtered:
        stemmed.append(ps.stem(word))
    result_str= ' '
    # a long string with stemmed words
    return result_str.join(stemmed) 

def convert_file_to_array(tf, file_names, training):
    x =[]
    for file_name in file_names:
        bag_of_word = process_file(file_name)
        x.append (bag_of_word)
    if training:
        text_counts= tf.fit_transform(x)
    else:
        text_counts= tf.transform(x)
    return text_counts

    
if __name__ == "__main__":
    #trying to use the same cv to preserve the dictionary
    cv = CountVectorizer( analyzer = 'word', lowercase=True, ngram_range = (1,1))
    tf =  TfidfVectorizer(input = 'content')
    #tf: 55% cv:44% @3/29/2020
    vectorizer = cv
    file_names = utility.get_file_list()
    # using different way to vectorize
    x = convert_file_to_array(vectorizer,file_names, True)
    # x = convert_file_to_array(tf,file_names, True)
    y = utility.get_target_values(file_names)

    #use the build-in split function to validate the prediction:
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
    clf = MultinomialNB(alpha =1.0).fit(X_train, y_train)
    predicted= clf.predict(X_test)


    #pick 3 data point and predict:
    '''
    clf = MultinomialNB(alpha=1.0 ).fit(x,y)
    test_file_names  = ['datafeeder\\data\\2020_03_05\\feed.txt',
        'datafeeder\\data\\2020_03_27\\feed.txt',
        'datafeeder\\data\\2020_03_28\\feed.txt',
        ]
    #predict tomorrow will increase
    y_test = array([0, -1, -1]) 
    x_test = convert_file_to_array(vectorizer, test_file_names, False)
    predicted= clf.predict(x_test)
    '''

    
    print("MultinomialNB Accuracy: {:2.2f}%".format( metrics.accuracy_score(y_test, predicted)*100.0))
    print(y_test)
    print('predicted: ')
    print(predicted)
    