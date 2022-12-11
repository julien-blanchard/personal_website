pip install pandas-bokeh

# **********************************************************************

import pandas as pd
import pandas_bokeh
pandas_bokeh.output_notebook()

# **********************************************************************

def getTables() -> pd.DataFrame:
    df_left = pd.read_html("https://en.wikipedia.org/wiki/List_of_Irish_counties_by_area")[0]
    df_right = pd.read_html("https://en.wikipedia.org/wiki/List_of_Irish_counties_by_population")[0]
    df_left.columns = [x.split(" (")[0].title() for x in df_left.columns]
    df_right.columns = [x.split(" (")[0].title() for x in df_right.columns]
    df_joined = pd.merge(
        left = df_left
        , right = df_right
        , how = "left"
        , left_on = "County"
        , right_on = "County"
        , suffixes = ("", "_y")
    )
    return df_joined

df = getTables()
df.head()

# **********************************************************************

def getCleanedDataframe(data: pd.DataFrame) -> pd.DataFrame:
    result = (
    data
    .drop(df.tail(2).index)
    .drop(data.filter(regex="_y$").columns,axis=1)
    .rename(columns = {"Traditional Province": "Province"})
    .assign(Area = lambda x:x["Area"].str.split(pat=" ", expand=True)[0])
    .assign(Area = lambda x:x["Area"].str.replace(",","").astype(float))
    .apply(lambda x: (x-x.min()) / (x.max() - x.min()) if x.dtype == "float" else x, axis=0)
    .sort_values("Density", ascending=True)
    )
    return result

plot = getCleanedDataframe(df)
plot.head()

# **********************************************************************

def getBarPlot(data: pd.DataFrame,title: str):
    data.plot_bokeh(
        kind="barh"
        , figsize=(800,500)
        , x="County"
        , y=["Density","Population","Area"]
        , stacked=True
        , colormap=["#30a2da","#fc4f30","#e5ae38"]
        , alpha=0.6
        , title=title
    )

getBarPlot(plot,"Area and density distribution by county")

# **********************************************************************

def getPopulation(table_url: str) -> pd.DataFrame:
    population = pd.read_html(table_url)[8]
    return population 

pop = getPopulation("https://en.wikipedia.org/wiki/Demographics_of_the_Republic_of_Ireland")
pop.head()

# **********************************************************************

def getCleanedPop(data: pd.DataFrame) -> pd.DataFrame:
    result = (
        data
        .drop(df.tail(1).index)
        .set_index(pd.DatetimeIndex(data["Unnamed: 0"].values[:-1]))
        .drop(columns="Unnamed: 0")
        .assign(
            Upper_thshld = lambda x: (x["Population on 1 April"].mean() + x["Population on 1 April"].std().round(0)),
            Lower_thshld = lambda x: (x["Population on 1 April"].mean() - x["Population on 1 April"].std().round(0))
            )
        .dropna()
        .resample("10y").mean()
    )
    return result

population = getCleanedPop(pop)
population.head()

# **********************************************************************

def getLinePlot(data: pd.DataFrame,title: str):
    data.plot_bokeh(
        kind="step"
        , figsize=(1100,500)
        , x=data.index
        , y=["Population on 1 April","Upper_thshld","Lower_thshld"]
        , colormap=["#30a2da","#fc4f30","#e5ae38"]
        , alpha=0.6
        , legend="bottom_right"
        , rangetool=True
        , title=title
    )

getLinePlot(population,"Population over time")

# **********************************************************************

def getStackedLinePlot(data: pd.DataFrame,title: str):
    data.plot_bokeh(
        kind="area"
        , figsize=(1100,500)
        , x=data.index
        , y=["Crude birth rate (per 1000)","Crude death rate (per 1000)","Total fertility rate[fn 1][11]"]
        , stacked=True
        , colormap=["#30a2da","#fc4f30","#e5ae38"]
        , alpha=0.6
        , legend="top_right"
        #, rangetool=True
        , title=title
    )

getStackedLinePlot(population,"Crude death and birth rates over time")

# **********************************************************************

from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource

def getSideTable(data: pd.DataFrame):
    table_data = (
        data
        .filter(["city","capital","population"])
    )
    left = DataTable(
        columns=[TableColumn(field=c, title=c) for c in table_data.columns],
        source=ColumnDataSource(table_data),
        height=350,
    )
    right = (
        data
        .head()
        .sort_values("population", ascending=True)
        .plot_bokeh(
            kind="barh"
            , x="city"
            , y="population"
            , color="#30a2da"
            , legend="bottom_right"
            , alpha=0.4
            , show_figure=False
                )
    )
    result = pandas_bokeh.plot_grid(
        [[left, right]]
        , plot_width=550
        , plot_height=400
        );

getSideTable(df)

# **********************************************************************

def getGeoPlot(data: pd.DataFrame, title: str):
    data["pop_size"] = data["population"] / 4000
    data.plot_bokeh.map(
        x="lng"
        , y="lat"
        , hovertool_string="""
            <h3> @{city} </h3> 
            <h3> Population: @{population} </h3>
            """
        , tile_provider="OSM"
        , size="pop_size"
        , category="population"
        , colormap="Bokeh"
        , alpha=0.5
        , line_color="black"
        , line_width=3
        , legend="City names"
        , figsize=(900, 600)
        , title=title
        )

getGeoPlot(df[1:], "Most populated cities in Ireland, after Dublin")