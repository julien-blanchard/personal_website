import Levenshtein as lev
import pandas as pd

corpus = [
    "Julien is a big fan of pizzas and salted caramel",
    "Julien loves pizzas and salted caramel",
    "Julien is a big fan of food in general",
    "Julien loves pizzas but he hates onions",
    "Julien is a big fan of pizzas but he hates onions",
    "Julien is a big fan of pizzas but he absolutely hates onions",
    "Julien is a big fan of pizzas",
    "Julien loves pizzas",
]

def getMatrix(data):
    m = {}
    ind = 1
    for d in data:
        m[f"Sentence {ind}"] = [lev.ratio(d,sent) for sent in data]
        ind+=1
    return m

def getDataFrame(data):
    distances = getMatrix(data)
    sentences = {"Sentences": [f"Sentence {i+1}" for i in range(len(data))]}
    datafr = pd.concat([pd.DataFrame(sentences),pd.DataFrame(distances)], axis=1)
    return datafr.style.background_gradient(cmap="Blues")

df = getDataFrame(corpus)
df