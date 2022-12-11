import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# **********************************************************************

def getDataFrame(url_address,ind):
    df = pd.read_html(url_address, index_col=None)[ind]
    return df

df = getDataFrame("https://www.tiobe.com/tiobe-index/",0)

# **********************************************************************

def quickClean(data):
    cols = [col for col in data.columns]
    data.rename(columns={f"{cols[4]}" : "Language"}, inplace=True)
    data.drop(columns=[cols[2],cols[3]], inplace=True)
    return data

df = quickClean(df)
df.head()

# **********************************************************************

def getDataBase(db_name_in,db_name_out,dataframe):
    engine = create_engine(f"sqlite:///{db_name_in}.db")
    dataframe.to_sql(db_name_out, engine, index=False, if_exists="replace")
    return engine

engine = getDataBase("languages","tiobe",df)

# **********************************************************************

df2 = getDataFrame("https://en.wikipedia.org/wiki/Comparison_of_programming_languages",1)
df2.head()

# **********************************************************************

engine = getDataBase("languages","wiki",df2)

# **********************************************************************

pd.read_sql(
    """
    SELECT
      t.Language,
      w.Imperative
    FROM 
      tiobe AS t
      LEFT JOIN wiki AS w ON t.Language = w.Language
    LIMIT 5
    """,
    engine
)
