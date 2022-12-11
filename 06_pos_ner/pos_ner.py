import pandas as pd

def getDataframe(data):
    df = pd.read_csv(data)
    return df

df = getDataframe("https://raw.githubusercontent.com/julien-blanchard/dbs/main/df_journal.csv")
df.sample(5)

# **********************************************************************

df = df.filter(["article"])

# **********************************************************************

import spacy

nlp = spacy.load("en_core_web_sm")

# **********************************************************************

text = "hey I'm Julien and you're reading an article on how to use some of the basic features or spaCy"

doc = nlp(text)

for token in doc:
    print(f"{token.text:<10} | {token.pos_:<10} | {token.dep_:<10} | {token.head.text:<10} | {spacy.explain(token.pos_):<10}")

# **********************************************************************

for token in doc:
    if token.pos_ == "VERB":
        print(f"{token.text:<10} | {token.pos_:<10}")

# **********************************************************************

def getTags(serie):
    tokens = nlp(serie)
    lex = [t.pos_ for t in tokens]
    lex = " ".join(lex)
    lex = lex.replace(" ", " / ")
    return lex

df["tags"] = df["article"].apply(getTags)
df.head(10)

# **********************************************************************

def getVerbs(serie,tag):
    result = []
    doc = nlp(" ".join(serie))
    for token in doc:
        if token.pos_ == tag:
            result.append(token.text.lower())
    return result  

verbs = getVerbs(df["article"],"VERB")

from collections import Counter

def getCount(data,howmany):
    counted = Counter(data)
    for k,v in counted.most_common(howmany):
        print(f"{k:<15} | {v:>6}")

getCount(verbs,10)

# **********************************************************************

import spacy

nlp = spacy.load("en_core_web_sm")

text = "hey I'm Julien and you're reading an article on how to use some of the basic features or spaCy"

doc = nlp(text)

for entity in doc.ents:
    print(f"{entity.text:<10} | {entity.label_:<10} | {spacy.explain(entity.label_):<10}")

# **********************************************************************

def getEnts(serie,tag):
    result = []
    doc = nlp(" ".join(serie))
    for entity in doc.ents:
        if entity.label_ == tag:
            result.append(entity.text.lower())
    return result  

orgs = getEnts(df["article"],"ORG")