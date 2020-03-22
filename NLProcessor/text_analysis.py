import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt


#hard coded file name for now
file_name = 'datafeeder\\data\\2020_3_20\\feed.txt'
with open(file_name) as f:
    text = f.read()

tokenized_word=word_tokenize(text)
fdist = FreqDist(tokenized_word)
fdist.plot(30,cumulative=False)
plt.show()
