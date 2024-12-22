import yfinance as yf
import pandas as pd

companies = ["AMZN","GOOG","TSLA","META"]
tickers = yf.Tickers(companies)

def getDataFrame(start_date,end_date):
    dataframe = (
        tickers
        .history(
            start=start_date,
            end=end_date,
            interval="1d"
        )
        .stack(level=1)
        .rename_axis(["Date", "Ticker"])
        .reset_index()
        .iloc[:,:3]
    )
    return dataframe

df = getDataFrame("2023-06-30","2023-08-01")

#############################

import pandas as pd
from faker import Faker
import random
from datetime import date, timedelta
from pprint import pprint

fake = Faker()
companies = [fake.company() for _ in range(4)]
today = date.today()

def getFakeData(howmany):
    struct = {
        "Date": [],
        "Company": [],
        "Open Price": [],
        "Close Price": []
    }
    for i in range(howmany):
        for c in companies:
            price = random.randint(100,150)
            struct["Date"].append(str(today - timedelta(i)))
            struct["Company"].append(c)
            struct["Open Price"].append(price)
            struct["Close Price"].append(price + random.randint(1,10))
    return struct

data = getFakeData(200)
df = pd.DataFrame(data)
df.head(20)

#############################

import pygwalker as pyg
import warnings

warnings.filterwarnings("ignore")

walker = pyg.walk(df)

#############################

import pygwalker as pyg

walker = pyg.walk(
    df,
    use_kernel_calc=True,
    dark="dark"
    )