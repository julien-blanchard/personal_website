import pandas as pd
import matplotlib.style as style, matplotlib.pyplot as plt 
from statsmodels.tsa.seasonal import seasonal_decompose
import jinja2
from markupsafe import escape
from markupsafe import Markup
from markupsafe import soft_unicode
from pycaret.regression import *
from sklearn.model_selection import train_test_split

# **********************************************************************

def getDataframe(url_address):
    df = pd.read_csv(url_address)
    return df 

def getCleanedData(data):
    dframe = (
        data
        .set_index(pd.DatetimeIndex(pd.to_datetime(df["Date"]).dt.date.values))
        .filter(["Adj Close"])
        .rename(columns={"Adj Close": "Close"})
        .pipe(lambda x: x.assign(
            Variation = x["Close"].shift(1) - x["Close"],
            Rolling_mean = x["Close"].rolling(window=30).mean(),
            Rolling_std = x["Close"].rolling(window=30).std()
            )
        )
        .dropna()
        ) 
    return dframe

df = getDataframe("META.csv")
df = getCleanedData(df)
df.tail()

# **********************************************************************

style.use("ggplot")

def getLinePlot(data,title):
    data.plot(
        figsize=(13,9),
        title=title
        );

getLinePlot(df,"META stocks")

# **********************************************************************

getLinePlot(df.resample("M").mean(),"META stocks (monthly)")

# **********************************************************************

def getInterval(data):
    dframe = (
        data
        .filter(["Close"])
        .pipe(lambda x: x.assign(
            Rolling_mean = x["Close"].rolling(window=30).mean(),
            Upper = x["Close"] + x["Close"].rolling(window=30).std(),
            Lower = x["Close"] - x["Close"].rolling(window=30).std()
        ))
    )
    return dframe

def getIntervalPlot(data):
    fig = plt.figure(figsize=(15, 9))
    ax = fig.add_subplot(1,1,1)
    x_axis = data.index
    ax.fill_between(x_axis, data["Upper"], data["Lower"], color="grey")
    ax.plot(x_axis, data["Close"], color="red", lw=3, label="Close")
    ax.plot(x_axis, data["Rolling_mean"], color="blue", lw=3, label="Rolling mean")
    ax.set_title('Confidence interval for META stocks')
    plt.legend(loc="upper right")
    plt.xticks(rotation=45)
    plt.show()

df2 = getInterval(df)
getIntervalPlot(df2)

# **********************************************************************

def getDecompositionPlot(data,freq,title):
    results = seasonal_decompose(
        x=data, 
        freq=freq,
        model="additive"
        )

    plt.rc("figure", figsize=(15,11))
    decomposition_results.plot().suptitle(title, fontsize = 18)
    plt.show()

getDecompositionPlot(df["Close"],12,"Mutliplicative decomposition for META stocks")

# **********************************************************************

train_data = df.head(int(len(df)*(90/100)))
test_data = df.tail(int(len(df)*(10/100)))

s = setup(
    data=train_data,
    test_data =test_data,
    target="Close",
    fold_strategy="timeseries",
    fold = 3,
    session_id = 123
    )

# **********************************************************************

best = compare_models(sort="MAE")

# **********************************************************************

best_model = predict_model(best)