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

#hard coded file name for now



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
    template = 'datafeeder\\data\\{}\\feed.txt'
    for file_name in file_names:
        full_name = str.format(template, file_name)
        x.append (process_file(full_name))
    
    if training:
        text_counts= cv.fit_transform(x)
    else:
        text_counts= cv.transform(x)
    return text_counts

if __name__ == "__main__":
    #trying to use the same cv to preserve the dictionary
    cv = CountVectorizer( analyzer = 'word', lowercase=True, ngram_range = (1,1))
    #y = array([10, -96, -13, -6, 7, 4, -1])
    # increase = 1, decrease = 0
    y = array([1, 0, 0, 0, 1, 1, 0]) 
    file_names = ['2020_3_5', '2020_3_7', '2020_3_8', '2020_3_9', '2020_3_10','2020_3_19', '2020_3_20']
    x = convert_file_to_array(cv,file_names, True)
    clf = MultinomialNB(alpha=0.5 ).fit(x,y)
    test_file_names  = ['2020_3_21']
    #y_test = array([-6])
    y_test = array([0])
    x_test = convert_file_to_array(cv, test_file_names, False)
    predicted= clf.predict(x_test)
    print("MultinomialNB Accuracy:{} predict: ", metrics.accuracy_score(y_test, predicted), predicted)

'''
print( nltk.pos_tag(stemmed))

fdist = FreqDist(stemmed)
fdist.plot(30,cumulative=False)
plt.show()


cv = CountVectorizer(lowercase=True, ngram_range = (1,1))
text_counts= cv.fit_transform(stemmed)
print(text_counts)
'''