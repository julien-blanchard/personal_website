from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from pprint import pprint

# **********************************************************************

def getCorpus(data):
    corpus = data.replace("\n"," ")
    corpus = corpus.replace("  ", " ")
    corpus = sent_tokenize(corpus)
    corpus = [c.lower() for c in corpus]
    # corpus = [c for c in corpus if corpus not in stopwords]
    corpus = [re.sub(r"[^\w\s]", "", c) for c in corpus]
    return corpus

# **********************************************************************

def getVects(data):
    vectorizer = TfidfVectorizer()
    vectorizer.fit(data)
    vects = vectorizer.transform(data)
    return vects

corp = getCorpus(holmes)
vectors = getVects(corp)

# **********************************************************************

vectorizer = TfidfVectorizer(
    max_df=0.9,
    min_df=0.1,
    max_features=200000,
    #stop_words=stopwords,
    decode_error="ignore"
)
