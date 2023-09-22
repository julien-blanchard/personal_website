# **********************************************************************

gem install polars-df

# **********************************************************************

require "polars-df"

food = {
    Food: ["pizza","burger"],
    Price: [5,6]
}

def getDataFrame(data)
    dframe = Polars::DataFrame.new(data)
    return dframe
end

df = getDataFrame(food)
puts df.head(10)

# **********************************************************************

def getDataFrame(csv_file)
    dframe = Polars.read_csv(csv_file)
    return dframe
end

df = getDataFrame("fake_csv.csv")
puts df.head

# **********************************************************************

cols = df[ ["Last_name","Country"] ]
puts cols.head

# **********************************************************************

filtered = df[(Polars.col("Age") > 43) & (Polars.col("Country") == "Croatia")]
puts filtered.head

# **********************************************************************

def getGroupBy(data,serie)
    grouped = data
        .groupby(serie)
        .count
    return grouped
end

df = getDataFrame("fake_csv.csv")
group = getGroupBy(df,"Country")
puts group.head

# **********************************************************************

def getGroupBy(data,serie)
    grouped = data
        .groupby(serie)
        .count
        .sort(["count"])
    return grouped
end

df = getDataFrame("fake_csv.csv")
group = getGroupBy(df,"Country")
puts group

# **********************************************************************

left = df[ ["Last_name","Country"] ]
right = df[ ["Last_name","Age"] ]
combined = left.join(right, on: "Last_name", how: "left")
puts combined.head

# **********************************************************************

top = df.head(2)
bottom = df.tail(2)
combined = top.vstack(bottom)
puts combined