def getDataframe(csv_file):
    df = pd.read_csv(csv_file)
    return df 

df = getDataframe("videogamessales.csv")
df.sample(5)

# **********************************************************************

from collections import Counter

def getCount(serie,howmany):
    counted = Counter(serie)
    labels = [l for l,v in counted.most_common(howmany)]
    values = [v for l,v in counted.most_common(howmany)]
    result = pd.DataFrame({"Labels":labels,"Values":values})
    return result

getCount(df["Publisher"],6)

# **********************************************************************

def getDoubleCount(data,serie1,serie2):
    count = data.groupby([serie1,serie2])[[serie2]].count()
    count.rename(columns={serie2:"volume"}, inplace=True)
    count.reset_index(drop=False, inplace=True)
    return count 

getDoubleCount(df,"Publisher","Platform")

# **********************************************************************

def getGroupBy(data,serie,aggr):
    grouped = data.groupby(serie, as_index=False).agg(aggr)
    return grouped.round(2)

getGroupBy(df,"Platform", {"NA_Sales":"mean","EU_Sales":"max","JP_Sales":"min"})

# **********************************************************************

def getDummies(dataframe,filtered,pivoted,howmany,ind):
    # dummies
    data = dataframe.filter(filtered)
    dummies = pd.get_dummies(data, prefix="count", columns=pivoted)
    for c in dummies.columns.to_list()[1:]:
        dummies.rename(columns={c: c.replace("count_","")}, inplace=True)
    # limiting the number of columns
    top = {}
    for c in dummies.columns.to_list()[1:]:
        top[c] = dummies[f"{c}"].sum()
    top = sorted(top, key=top.get, reverse=True)[:howmany]
    top.insert(0, ind)
    dummies = dummies.filter(top)
    # reducing the number of cols
    agg = {}
    for c in dummies.columns.to_list()[1:]:
        agg[c] = "sum"
    dummies = dummies.groupby(ind, as_index=False).agg(agg)
    return dummies

# dummies table for the top 6 elements
dummies = getDummies(df,["Publisher","Platform"],["Platform"],6,"Publisher")
dummies

# **********************************************************************

rc = {
    "figure.figsize": (18,5),
    "axes.edgecolor": "white",
    "font.family": "monospace",
    "font.size": 13
     }
plt.rcParams.update(rc)

# **********************************************************************

def getBarCharts(x1,y1,x2,y2,my_title1,my_title2):
    fig = plt.figure()
    plt.subplot(121)
    left = sns.barplot(x=x1, y=y1, orient="h", palette="Blues_r")
    sns.despine(left=True, right=True, top=True, bottom=True)
    plt.xlabel("")
    plt.ylabel("")
    left.set_title(my_title1)
    plt.subplot(122)
    right = sns.barplot(x=x2, y=y2, orient="h", palette="Blues_r")
    sns.despine(left=True, right=True, top=True, bottom=True)
    plt.xlabel("")
    plt.ylabel("")
    right.set_title(my_title2)
    plt.subplots_adjust(wspace = 0.2, hspace = 0.4, top = 0.9)
    plt.show()

left = getCount(df["Publisher"], 7)
right = getCount(df["Platform"], 7)

getBarCharts(left["Values"], left["Labels"],
             right["Values"], right["Labels"],
             "Top publishers", "Top platforms"
             )

# **********************************************************************

def getStackedBars(data,x,title):
    data.plot(
        kind="barh",
        x=x,
        stacked=True, 
        legend="upper right",
        title=title,
        cmap="Blues_r"
        );

d = dummies.query("Publisher in ('Electronic Arts','Namco Bandai Games','Activision','THQ','Ubisoft')")
getStackedBars(d,"Publisher","test")

# **********************************************************************

from wordcloud import WordCloud, STOPWORDS

def getWordCloud(text_left,text_right,title):
    text_left = " ".join(text_left)
    text_right = " ".join(text_right)
    wc_left = WordCloud(max_words=200, width=600, height=400, background_color="white", margin=0, max_font_size=80, min_font_size=10, colormap="Blues_r").generate(text_left)
    wc_right = WordCloud(max_words=200, width=600, height=400, background_color="white", margin=0, max_font_size=80, min_font_size=10, colormap="Blues_r").generate(text_left) 
    plt.figure()
    plt.suptitle(title, size=20, y=1)
    plt.subplot(1,2,1)
    plt.imshow(wc_left)
    plt.axis("off")
    plt.subplot(1,2,2)
    plt.imshow(wc_right)
    plt.axis("off")
    plt.show()

getWordCloud(df["Publisher"].dropna(),df["Name"],"Top keywords")

# **********************************************************************

def getHistPlots(x1,x2,title1,title2):
    fig = plt.figure()
    plt.subplot(121)
    left = sns.histplot(x1, kde=True, bins=10, palette="Blues_r")
    sns.despine(left=True, right=True, top=True, bottom=True)
    plt.xlabel("")
    plt.ylabel('')
    left.set_title(title1)
    plt.subplot(122)
    right = sns.histplot(x2, kde=True, bins=10, palette="Blues_r")
    sns.despine(left=True, right=True, top=True, bottom=True)
    plt.xlabel("")
    plt.ylabel("")
    right.set_title(title2)
    plt.subplots_adjust(wspace = 0.2, hspace = 0.4, top = 0.9)
    plt.show()

left = df.query("Publisher == 'Ubisoft'")
right = df.query("Publisher == 'Electronic Arts'")

getHistPlots(left["Year"],right["Year"],"Years (Ubisoft)","Years (EA)")

# **********************************************************************

def getViolinPlots(data,x,y,title):
    plt.figure()
    sns.boxplot(data=data, x=x, y=y, orient="v", palette="Blues_r")
    plt.title(title)
    sns.despine(left=True, right=True, top=True, bottom=True)
    plt.show()

violin = df.query("Publisher in ('Ubisoft','Electronic Arts')")
getViolinPlots(violin,"Publisher","Year","Release years for Ubisoft and EA")

# **********************************************************************

def getCorrPlot(data,x,y,howmany,title):
    # aggregation
    corr = data.filter([x,y])
    dataframe = getCount(data[y],howmany)
    dataframe = dataframe["Labels"].to_list()
    corr = corr.loc[corr[y].isin(dataframe)]

    # dummies and re aggregation

    corr = pd.get_dummies(corr,prefix="",prefix_sep="",columns=[y])
    aggregate = {}
    for col in corr.columns[1:]:
        aggregate[col] = "sum"
    corr = corr.groupby(x, as_index=False).agg(aggregate)

    # normalising
    for col in corr.columns[1:]:
        corr[col] = np.log(corr[col] + 1)
    
    # correlation matrix
    corr.drop(columns=[x],inplace=True)
    corr = corr.corr()
    sns.clustermap(corr, figsize=(10,10), cmap="Blues")
    sns.despine(left=True, right=True, top=True, bottom=True)
    plt.title(title) 
    plt.show()

getCorrPlot(df,"Publisher","Platform",10,"Correlation plot")

# **********************************************************************

import networkx as nx 
n = df.filter(["Publisher", "Platform", "Year"])

def getNetwPlot(data, serie1, serie2, serie3):
    G = nx.from_pandas_edgelist(data, serie1, serie2, edge_attr=True)
    edgelist = nx.to_edgelist(G)

    colors = [i/len(G.nodes) for i in range(len(G.nodes))]

    plt.figure(figsize=(12,8))
    nx.draw(
        G,
        with_labels=True,
        node_size=[v * 200 for v in dict(G.degree()).values()],
        width=[v[2][serie3] / 500 for v in edgelist],
        font_size=10,
        node_color=colors,
        cmap="BuPu"
    )
    plt.title("NetworkX")
    plt.show()

getNetwPlot(n, "Publisher", "Platform", "Year")
