import snscrape.modules.twitter as sntwitter
import pandas as pd

def getTweets(handle,howmany):
    struct = {
        "Posted": [],
        "From": [],
        "Tweet": []
    }
    tweets = sntwitter.TwitterSearchScraper(f"{handle} lang:en").get_items()
    for i,t in enumerate(tweets):
        if i > howmany:
            break
        else:
            struct["posted"].append(t.date)
            struct["from"].append(t.user.username)
            struct["tweet"].append(t.rawContent)
    dframe = pd.DataFrame(struct)
    return dframe

getTweets("to:@AppleSupport",500)

# **********************************************************************

df = df.filter(["Tweet"])

import preprocessor as p

df["cleaned"] = df["tweet"].apply(lambda x: p.clean(x))
df.filter(["cleaned"]).sample(10)

# **********************************************************************

def getSentiment(corpus):
    struct = {}

    with open("AFINN-en-165.txt", "r") as file:
        for f in file.readlines():
            struct[f.split("\t")[0]] = f.split("\t")[1].strip("\n")

    for t in corpus.split(" "):
        if t.lower() in struct:
            print(f"{t:<15} =>\t{struct[t]}")
        else:
            print(f"{t:<15} =>\t0")

text = "Hi, my name is Julien I love pizzas but I absolutely hate cauliflower"
getSentiment(text)

# **********************************************************************

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

text = "I also hate artichokes"

sia = SentimentIntensityAnalyzer()
result = sia.polarity_scores(text)

for k,v in result.items():
    print(f"{k:<10} =>\t{v}")

# **********************************************************************

def getSentiment(data,serie):
    sia = SentimentIntensityAnalyzer()
    sentiment_cols = {}
    for i,col in enumerate(data[serie]):
        sentiment_cols[i] = sia.polarity_scores(col)
    sentiment_df = pd.DataFrame(sentiment_cols)
    return sentiment_df.T

def getSentimentTag(data):
    result = []
    for i,v in data.iterrows():
        scores = [v[1],v[2],v[3]]
        m = max(scores)
        ind = scores.index(m)
        if ind == 0:
            result.append("Negative")
        elif ind == 1:
            result.append("Neutral")
        else:
            result.append("Positive")
    return result

sent_valence = getSentiment(df,"cleaned")
valence = pd.merge(df["cleaned"], sent_valence, left_index=True, right_index=True)
valence["valence_tag"] = getSentimentTag(valence)
valence.sample(10)

# **********************************************************************

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

# **********************************************************************

text = "Actually, I hate vegetables in general."

encoded_text = tokenizer(text, return_tensors="pt")
output = model(**encoded_text)
scores = output[0][0].detach().numpy()
scores = softmax(scores)

for s in scores:
    print(s)

# **********************************************************************

def getSentimentRoberta(data,serie):
    sentiment_cols = {
        "neg" : [],
        "neu" : [],
        "pos" : []
    }
    for i,col in enumerate(data[serie]):
        encoded_text = tokenizer(col, return_tensors="pt")
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        sentiment_cols["neg"].append(scores[0])
        sentiment_cols["neu"].append(scores[1])
        sentiment_cols["pos"].append(scores[2])
    sentiment_df = pd.DataFrame(sentiment_cols)
    return sentiment_df

sent_roberta = getSentimentRoberta(df,"cleaned")
roberta = pd.merge(df["cleaned"], sent_roberta, left_index=True, right_index=True)
roberta["roberta_tag"] = getSentimentTag(roberta)
roberta.sample(10)

# **********************************************************************

def getMismatch(data):
    result = []
    for k,v in data.iterrows():
        if v[1] == v[2]:
            result.append(False)
        else:
            result.append(True)
    return result

def combineSentiment(left,right):
    l = left.filter(
        ["cleaned","valence_tag"]
        )
    r = right.filter(
        ["cleaned","roberta_tag"]
        )
    combined = l.merge(
        r,
        how="left",
        left_on="cleaned",
        right_on="cleaned"
        )
    return combined

mismatch = combineSentiment(valence,roberta)
mismatch["mismatch"] = getMismatch(mismatch)
mismatch.query('mismatch == True')

# **********************************************************************

from collections import Counter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly

def getCount(serie):
    result = {
        "tag": [],
        "volume": []
    }
    c = Counter(serie)
    for k,v in c.most_common():
        result["tag"].append(k)
        result["volume"].append(v)
    return result   

def getDoubleBarPlots(x1, y1, x2, y2, title, subtitle1, subtitle2):
    cols = ["#003f5c","#bc5090","#ffa600"]
    fig = make_subplots(rows=1, cols=2, subplot_titles=(subtitle1, subtitle2))
    fig.layout.template = "plotly_white"
    fig.add_trace(
        go.Bar(
            x=x1,
            y=y1,
            orientation="h",
            marker_color=cols,
            width=0.8,
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=x2,
            y=y2,
            orientation="h",
            marker_color=cols,
            width=0.8,
        ),
        row=1,
        col=2,
    )
    fig.update_layout(
        title=title,
        bargap=0.01,
        showlegend=False,
        template="plotly_white",
        plot_bgcolor="#E9E8E8",
        paper_bgcolor="#E9E8E8",
        width=900,
        height=450,
        font=dict(
            family="Arial",
            size=18
        )
    )
    fig.update_yaxes(
        type="category",
        categoryorder="total ascending"
        )
    fig.show()

valence_tags = getCount(mismatch["valence_tag"])
roberta_tags = getCount(mismatch["roberta_tag"])
getDoubleBarPlots(
    valence_tags["volume"],
    valence_tags["tag"],
    roberta_tags["volume"],
    roberta_tags["tag"],
    "Sentiment tags distribution","Valence","roBERTa"
    ) 

# **********************************************************************

import transformers
import shap
import numpy as np

classifier = transformers.pipeline("sentiment-analysis", top_k=None)

# **********************************************************************

test_df = df["cleaned"][:3].to_list()

for cl in classifier(test_df):
    for c in cl:
        print(c)

# **********************************************************************

explainer = shap.Explainer(classifier)
shap_values = explainer(test_df)
print(shap_values)

# **********************************************************************

def getTextPlot(data):
    shap.plots.text(
        data,
        xmin=-0.1
        )

getTextPlot(shap_values)

# **********************************************************************

def getBarPlot(data):
    shap.plots.bar(
        data,
        order=shap.Explanation.argsort,
        clustering_cutoff=1
        )

getBarPlot(shap_values[0,:,"POSITIVE"])

# **********************************************************************

def getBarPlot(data):
    shap.plots.bar(
        data,
        order=shap.Explanation.argsort
        )

getBarPlot(shap_values[:, :, "POSITIVE"].mean(0))

# **********************************************************************

def getForcePlot(data):
    shap.plots.force(
        data,
        matplotlib=True,
        figsize=(20,6),
        plot_cmap=["#77dd77", "#f99191"],
        text_rotation=1
    )

getForcePlot(shap_values[0,:,"NEGATIVE"])