import pandas as pd

def getDataframe(url_table,ind):
    df = pd.read_html(url_table)[ind]
    return df

df = getDataframe("https://en.wikipedia.org/wiki/Historical_population_of_Ireland",1)
df.sample(5)

# **********************************************************************

df = df.drop(columns=["Rank"])
df = df.query("Province == 'Leinster'")
df.sort_values("Density (/ km²)", ascending=False)

# **********************************************************************

(
df
.drop(columns=["Rank"])
.query("Province == 'Leinster'")
.sort_values("Density (/ km²)", ascending=False)
)

# **********************************************************************

(
             df
.drop(columns=["Rank"])                              .query("Province == 'Leinster'")
          .sort_values("Density (/ km²)", ascending =
False)
)

# **********************************************************************

def getPlot(x,y,title):
    result = (
        df
        .drop(columns=["Rank"])
        .rename(columns=lambda x:x.lower())
        .query("province == 'Leinster'")
        .sort_values("density (/ km²)", ascending=True)
        .plot(
            figsize=(12,5)
            , kind="barh"
            , x=x
            , y=y 
            , cmap="Blues_r"
            , grid=True
            , title=title
        )
    )
    return result

getPlot("county","density (/ km²)","2016 Census overview for Leinster")