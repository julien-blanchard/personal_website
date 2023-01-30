import pandas as pd
import yfinance as yf

# =============================================

def getDataframe(company,start_day,end_day):
    dataframe = yf.download(
        company,
        start=start_day,
        end=end_day,
        progress=False,
        auto_adjust=True
        ).reset_index()
    dataframe = (
        dataframe
        .set_index(pd.DatetimeIndex(dataframe["Date"].values))
        .drop(columns=["Volume"])
        )
    return dataframe  

df = getDataframe("TWTR","2021-12-31","2022-12-31")
df.tail(8)

# =============================================

import mplfinance as mpf

mpf.plot(df)

# =============================================

def getMAVPlot(serie,frequency,title):
    mpf.plot(
        df.drop(columns=[serie]).resample(frequency).mean(),
        title=title,
        figsize=(15,9),
        type="candle",
        mav=(3,6,9)
        )
    
getMAVPlot("Date","W","Smoothed out Monthly Moving Average for Twitter's stock prices")

# =============================================

def getCandlePlot(serie,frequency,title):
    mpf.plot(
        df.drop(columns=[serie]).resample(frequency).mean(),
        title=title,
        figsize=(15,9),
        fill_between=dict(
            y1=df["Low"].resample(frequency).mean().values,
            y2=df["High"].resample(frequency).mean().values,
            alpha=0.2,
            panel=0,
            color="blue"
            )
        )

getCandlePlot("Date","W","Smoothed out daily variation for Twitter's stock prices")

# =============================================

upper = df["Close"].mean() + df["Close"].std()
lower = df["Close"].mean() - df["Close"].std()

def getCandlePlotSTD(serie,frequency,title):
    mpf.plot(
        df.drop(columns=[serie]).resample(frequency).mean(),
        title=title,
        figsize=(15,9),
        type="candle",
        hlines=dict(
            hlines=[upper,lower],
            colors=["blue","blue"],
            linestyle="-.",
            alpha=0.3
            )
        )

getCandlePlotSTD("Date","W","Smoothed out lower and upper standard deviation for Twitter's stock prices")

# =============================================

def getEventsPlot(serie,frequency,events,title):
    mpf.plot(
        df.drop(columns=[serie]).resample(frequency).mean(),
        title=title,
        figsize=(15,9),
        type="line",
        vlines=dict(
            vlines=events,
            linewidths=(1,1,1),
            colors=["red","red","red"],
            alpha=0.5
            )
        )

getEventsPlot("Date","W",["2022-04-25","2022-07-08","2022-10-27"],"Impact of Elon Musk's announcements over Twitter's stock prices")

# =============================================

from statsmodels.tsa.seasonal import seasonal_decompose

def getDecompositionPlot(data,freq,title):
    results = seasonal_decompose(
        x=data, 
        period=freq,
        model="additive"
        )

    plt.rc("figure", figsize=(15,13))
    results.plot().suptitle(title, y=1.05, fontsize = 18)
    plt.show()

getDecompositionPlot(df["Close"],12,"Mutliplicative decomposition for Twitter stocks")

# =============================================

from prophet import Prophet
from prophet.plot import add_changepoints_to_plot, plot_plotly, plot_components_plotly, plot_cross_validation_metric
from prophet.diagnostics import cross_validation, performance_metrics

def getProphetDF(data,serie1,serie2):
    result = (
        data
        .filter([serie1,serie2)
        .rename(columns={"Date":"ds","Close":"y"})
    )
    return result

df_prophet = getProphetDF(df,"Date","Close")

# =============================================

eighty = round((len(df_prophet) / 100) * 80)
train = df_prophet[:eighty]
test = df_prophet[eighty:]

m = Prophet(
    weekly_seasonality=True,
    interval_width=0.95,
    #n_changepoints=5
)
m.add_country_holidays(country_name="US")
m.fit(train)

future = m.make_future_dataframe(periods=180, freq="D")
forecast = m.predict(future)
forecast.tail(10)

# =============================================

from matplotlib import pyplot as plt

def getPredictionPlot(title):
    fig = m.plot(forecast, uncertainty=True)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price in $")
    plt.legend(loc="upper left")

getPredictionPlot("Predictions for Twitter's stock values")

# =============================================

def getChangePlot(title):
    fig = m.plot(forecast)
    a = add_changepoints_to_plot(fig.gca(), m, forecast)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price in $")
    plt.legend(loc="upper left")

getChangePlot("Predictions and change points")

# =============================================

def viewChangePoints():
    x = 1
    for cp in m.changepoints:
        print(f"Date for change point n.{x}:\n\n\t{str(cp).split(' ')[0]}\n")
        x+=1

viewChangePoints()

# =============================================

def getComponentsPlot():
    fig = m.plot_components(forecast)

getComponentsPlot()

# =============================================

from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric

df_cv = cross_validation(
    m,
    initial="120 days",
    period="60 days",
    horizon = "90 days"
    )

# =============================================

(
df_cv
.tail()
.style
.background_gradient(cmap="Blues_r")
)

# =============================================

def getPerformanceMetrics(howmany):
    result = (
        performance_metrics(df_cv)
        .tail(howmany)
        .style
        .background_gradient(cmap="Blues_r")
    )
    return result

df_p = getPerformanceMetrics(10)
df_p

# =============================================

def getPerformancePlot(metric):
    fig = plot_cross_validation_metric(df_cv, metric=metric)
    plt.title("RMSE score over time")

getPerformancePlot("rmse")

# =============================================

def getPerformanceComparison():
    f = forecast[["ds","yhat"]]
    (
        test
        .merge(
            right=f,
            how="left",
            left_on="ds",
            right_on="ds"
            )
        .plot(
            figsize=(15,7),
            kind="line",
            x="ds",
            title="Test values VS forecast values"
            )
    );

getPerformanceComparison()

# =============================================

from markupsafe import escape
from markupsafe import Markup
import numpy as np
from markupsafe import soft_unicode
from pycaret.regression import *

df_pycaret = (
    df
    .set_index(pd.DatetimeIndex(df["Date"].values))
    .filter(["Date","Close"])
    .rename(columns={"Date":"ds","Close":"y"})
)

# =============================================

eighty = round((len(df_pycaret) / 100) * 80)
train = df_pycaret[:eighty]
test = df_pycaret[eighty:]

s = setup(
    data=train,
    test_data=test,
    target="y",
    fold_strategy="timeseries",
    fold = 3,
    session_id = 123
    )

# =============================================

best = compare_models(sort="RMSE")
best