names = ["Ana","John","Ana","Ana","Mary","John"]

def countNames(data):
    result = {}
    for name in names:
        if name in result:
            result[name] += 1
        else:
            result[name] = 1
    print(result)

countNames(names)

# **********************************************************************

result = sorted(result.items(), key=lambda x: x[1], reverse=True)

# **********************************************************************

from collections import Counter

names = ["Ana","John","Ana","Ana","Mary","John"]

def countNames(data):
    result = Counter(data)
    print(result)

countNames(names)

# **********************************************************************

from collections import Counter

names = ["Ana","John","Ana","Ana","Mary","John"]

def countNames(data,howmany):
    counted = Counter(data)
    for k,v in counted.most_common(howmany):
        print(f"{k:<5} | {v:>3}")

countNames(names,2)

# **********************************************************************

from collections import Counter
import pandas as pd

names = ["Ana","John","Ana","Ana","Mary","John"]

def countNames(data,howmany):
    counted = Counter(data)
    keys = [k for k,v in counted.most_common(howmany)]
    values = [v for k,v in counted.most_common(howmany)]
    dataframe = pd.DataFrame(
        {"Keys":keys,
         "Values":values
         }
        )
    return dataframe

countNames(names,3)

# **********************************************************************

def getDataFrame(url_address,ind):
    df = pd.read_csv(url_address)
    return df

df = getDataFrame("https://raw.githubusercontent.com/julien-blanchard/dbs/main/pokemon_go.csv")
df.sample(5)

# **********************************************************************

df["Primary"].value_counts(
    normalize=True,
    ascending=False,
    dropna=False
    ) 

# **********************************************************************

def getMultiCount(data,serie1,serie2):
    d = data.groupby([serie1,serie2])[[serie2]].count()
    d.rename(columns={serie2:"volume"}, inplace=True)
    d.reset_index(drop=False, inplace=True)
    return d 

getMultiCount(df,"Primary","Secondary")

# **********************************************************************

df["Primary_count"] = df["Primary"].groupby(df["Primary"]).transform("count")
