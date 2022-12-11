import pandas as pd

def getDataFrame() -> pd.DataFrame:
    data = pd.read_csv("journal.csv")
    return data

df = getDataFrame()
df.head()

# **********************************************************************

import re
import nltk
import nltk.corpus
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords

def getCleanText(serie: str) -> str:
  stop_words=set(nltk.corpus.stopwords.words("english"))
  lem = WordNetLemmatizer()
  tokens = word_tokenize(str(serie))
  tokens = [lem.lemmatize(t.lower()) for t in tokens if t not in stop_words and len(t) > 4]
  cleaned = " ".join(tokens)
  return cleaned

df["cleaned"] = df["article"].apply(getCleanText)
df.head()

# **********************************************************************

corpus = df["cleaned"].to_list()

try:
  topic_model = BERTopic()
  topics, probs = topic_model.fit_transform(corpus)
except Exception as e:
  print(e)

# **********************************************************************

topic_model.get_topic_info()

# **********************************************************************

def showTopics():
  for topics in range(0, (len(topic_model.get_topic_info()))):
    print(f"\nTopic: {topics + 1}\n")
    for t in topic_model.get_topic(topics):
      print("\t", t[0])

showTopics()

# **********************************************************************

def getTopTopics(min_score):
  for topics in range(0, (len(topic_model.get_topic_info()))):
    print(f"\nTopic: {topics + 1}\n")
    for t in topic_model.get_topic(topics):
      if t[1] >= min_score:
        print(f"\t{t[0]:<12} | \t{t[1]}")

getTopTopics(0.03)

# **********************************************************************

topic_model.visualize_barchart()

# **********************************************************************

import pandas as pd
from bs4 import BeautifulSoup
import urllib
import requests
from datetime import date, datetime, timedelta
import random
import re
import time
import numpy as np

class Journal:

  # the url embedded within an F-string statement, the number of pages we'll iterate through, and our lists
    def __init__(self):
        self.Urls = [f"https://www.thejournal.ie/irish/page/{i}/" for i in range(1,20)]
        self.Articles = []
        self.Published = []
        self.Views = []
        self.Comments = []

  # here we're simply calling the url, and parsing the HTML tags
    def getRequest(self,url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup
  
  # that took me an hour, as my initial script was missing the likes and views, but capturing unrelated articles
    def getContent(self,url):
        soup = self.getRequest(url)
        for s in soup.find_all("span", class_="published-at"):
            s = s.text.replace("Updated", "")
            s = s.replace("Live", "")
            self.Published.append(s.strip())
        for s in soup.find_all("h4", class_="title"):
            self.Articles.append(s.text.strip())
        for s in soup.find_all("span", class_="interactions"):
            try:
                if s.text.strip().split("\n")[2]:
                    self.Comments.append(s.text.strip().split("\n")[2])
            except:
                continue
        for s in soup.find_all("span", class_="interactions"):
            try:
                if s.text.strip().split("\n")[0]:
                    self.Views.append(s.text.strip().split("\n")[0])
            except:
                continue

  # creating dictionaries, where the key is the name of our columns, and the values are our lists
    def getDataframe(self):
        urls = self.Urls
        for u in urls:
            self.getContent(u)
        limit = len(self.Comments)
        df = {"date": self.Published,
            "article": self.Articles,
            "views": self.Views,
            "comments": self.Comments
            }
        df = pd.DataFrame.from_dict(df, orient="index")
        df = df.transpose().dropna()
        return df

    def getCleanDates(self,serie):
        if "update" in serie.lower():
            if not re.search("Mon|Tue|Wed|Thu|Fri|Sat|Sun",serie):
                return serie.replace("Updated","").strip().split(",")[0]
        elif re.search("Mon|Tue|Wed|Thu|Fri|Sat|Sun",serie):
            cleanedText = serie.replace("Updated\n","").strip().split(" ")[0]
            today = date.today()
            for i in range(7):
                day = today - timedelta(days=i)
            if day.strftime("%A")[:3] == cleanedText:
                return day
        elif "ago" in serie.lower():
            return date.today()
        else:
            return serie.split(",")[0]

    # cleaned dataframe
    def getCleanedDF(self):
        df = self.getDataframe()
        df["date"] = df["date"].apply(self.getCleanDates)
        df["date"] = pd.to_datetime(df["date"])
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df["views"] = df["views"].apply(lambda x: str(x).split(" ")[0].replace(",","")).astype(int)
        df["comments"] = df["comments"].apply(lambda x: str(x).strip())
        df["comments"] = df["comments"].apply(lambda x: str(x).split(" ")[0] if "Comments" in x else "0").astype(int)
        return df

# work your magic, Journal class!
journal = Journal()
df = journal.getCleanedDF()