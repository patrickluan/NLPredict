import urllib.request
import pickle
import  db_operations
import ssl
from ssl import Purpose
from bs4 import BeautifulSoup
from nltk.corpus import words
from nltk.corpus import stopwords

#link = 'https://www.newsbtc.com/feed/'
frequent_words = set()
FREQUENT_WORDS_FILE = 'c:\\python\\NLPredict\\datafeeder\\data\\frequent_words.txt'
def is_english_word(word):
    lower_case_word = word.lower()
    if lower_case_word in frequent_words:
        return True
    if lower_case_word in words.words():
        frequent_words.add(lower_case_word)
        return  True
    return False

def find_all_urls():
    db = db_operations.db_operations()
    if not db.connect():
        return {}
    links = db.get_content_urls()
    return links
def dump_contents(log_id, content):
    db = db_operations.db_operations()
    if not db.connect():
        return 
    db.insert_content(log_id, content)
    return

# start of the operation
def read_content():
    stop_words=set(stopwords.words("english"))
    with open(FREQUENT_WORDS_FILE, 'rb') as word_file:
        frequent_words = pickle.load(word_file)
        
    for link in find_all_urls():
        result = ''
        #link is a (id, url) tuple
        req = urllib.request.Request(link[1], headers={'User-Agent': 'Mozilla/5.0'})
        site = urllib.request.urlopen(req)
        soup = BeautifulSoup(site.read(),'html.parser' )
        for script in soup(["script", "style", "a", "link"]):
            script.decompose()    # rip it out
        stripped_text = soup.get_text(strip = True)
        
        for seg in stripped_text.split():
            if len(seg)>2 and is_english_word(seg) and (seg not in stop_words):
                result = result + ' ' + seg
        index = link[0]
        dump_contents(index, result)
    with open(FREQUENT_WORDS_FILE, 'wb') as word_file:
        pickle.dump(frequent_words, word_file)

