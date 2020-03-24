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
    return result_str.join(stemmed) 

def convert_file_to_array(file_names):
    x =[]
    template = 'datafeeder\\data\\{}\\feed.txt'
    for file_name in file_names:
        full_name = str.format(template, file_name)
        x.append (process_file(full_name))
    print(len(array(x)))
    return array(x)

if __name__ == "__main__":
    y = [1, -9.6, -1.3, -0.6, 0.7]
    file_names = ['2020_3_5', '2020_3_7', '2020_3_8', '2020_3_9', '2020_3_10']
    
    clf = MultinomialNB().fit(convert_file_to_array(file_names),array(y))
    test_file_names  = ['2020_3_19', '2020_3_20', '2020_3_21']
    y_test = [0.4, -0.1, -6.4]
    predicted= clf.predict(convert_file_to_array(test_file_names))
    print("MultinomialNB Accuracy:",metrics.accuracy_score(array(y_test), predicted))

'''
print( nltk.pos_tag(stemmed))

fdist = FreqDist(stemmed)
fdist.plot(30,cumulative=False)
plt.show()


cv = CountVectorizer(lowercase=True, ngram_range = (1,1))
text_counts= cv.fit_transform(stemmed)
print(text_counts)
'''