pip install palmettopy

# **********************************************************************

from palmettopy.palmetto import Palmetto

# **********************************************************************

def getPalmettoScore(tokens):
    palmetto = Palmetto("http://palmetto.cs.upb.de:8080/service/")
    coherences = ["ca", "cp", "cv", "npmi", "uci", "umass"]
    for c in coherences:
        print(f"Coherence score for {c.upper():<7}->\t", palmetto.get_coherence(tokens, coherence_type=c))

words = ["mango", "apple", "banana", "cherry", "peach"]
getPalmettoScore(words)

# **********************************************************************

sample_topics = {
    "Topic_one": ["mango", "apple", "banana", "cherry"],
    "Topic_two": ["football","bird","nose","sweater"],
    "Topic_three": ["cat","lion","feline","panther"] 
}

def getCoherenceScores(topics):
    palmetto = Palmetto("http://palmetto.cs.upb.de:8080/service/")
    for k,v in topics.items():
        print(f"Coherence score for {k:<13} ->\t{palmetto.get_coherence(v, coherence_type='ca')}")

getCoherenceScores(sample_topics)

# **********************************************************************

from gensim.test.utils import common_corpus, common_dictionary
from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel

sample = [
    ["cat","tiger","lion"],
    ["apple","banana","strawberry"]
]

def getPalmettoScore(topics):
    # dictionary = Dictionary(topics)
    # corpus = [dictionary.doc2bow(t) for t in topics]
    cm = CoherenceModel(
        topics=topics,
        corpus=common_corpus,
        dictionary=common_dictionary,
        coherence="u_mass")
    score = cm.get_coherence()
    print(score)

getPalmettoScore(sample)

# **********************************************************************

dictionary = Dictionary(topics)
corpus = [dictionary.doc2bow(t) for t in topics]