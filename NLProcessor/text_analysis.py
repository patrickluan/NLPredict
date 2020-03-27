from numpy import array
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from sklearn.naive_bayes import MultinomialNB
from nltk.stem import PorterStemmer
from nltk.corpus import words
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics

import utility
prediction =['Decrease', 'Increase']
def process_file(file_name):
    filtered =[]
    stop_words=set(stopwords.words("english"))
    stemmed =[] 
    with open(file_name) as f:
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

def convert_file_to_array(cv, file_names, training):
    x =[]
    for file_name in file_names:
        x.append (process_file(file_name))
    
    if training:
        text_counts= cv.fit_transform(x)
    else:
        text_counts= cv.transform(x)
    return text_counts


if __name__ == "__main__":
    
    #trying to use the same cv to preserve the dictionary
    cv = CountVectorizer( analyzer = 'word', lowercase=True, ngram_range = (1,1))
    file_names = utility.get_file_list()
    x = convert_file_to_array(cv,file_names, True)
    y = utility.get_target_values(file_names)
    clf = MultinomialNB(alpha=1.0 ).fit(x,y)
    test_file_names  = ['datafeeder\\data\\2020_03_26\\feed.txt',
        'datafeeder\\data\\2020_03_27\\feed.txt']
    #predict tomorrow will increase
    y_test = array([utility.DECREASE,utility.DECREASE]) 
    x_test = convert_file_to_array(cv, test_file_names, False)
    predicted= clf.predict(x_test)
    print("MultinomialNB Accuracy: ", metrics.accuracy_score(y_test, predicted))
    print("Predictions: ", predicted )
