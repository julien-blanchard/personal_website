import pandas as pd
import random
from faker import Faker

def getFakeData(howmany):
    fake = Faker()
    group = [i for i in range(1,5)]
    names = [fake.unique.first_name() for i in range(60)]
    data_dict = {
        "Names1": [random.choice(names) for i in range(howmany)],
        "Names2": [random.choice(names) for i in range(howmany)],
        "Group": [random.choice(group) for i in range(howmany)]
     }
    result = pd.DataFrame(data_dict)
    return result

df = getFakeData(600)
df.to_csv("fake_names.csv")

# **********************************************************************

import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt

# **********************************************************************

df_pk_go = "https://raw.githubusercontent.com/julien-blanchard/dbs/main/pokemon_go.csv"
df_fake_n = "https://raw.githubusercontent.com/julien-blanchard/dbs/main/fake_names.csv"

# **********************************************************************

G = nx.from_pandas_edgelist(df_pk_go, "Primary", "Secondary")
edgelist = nx.to_edgelist(G)
print(edgelist)

# **********************************************************************

G = nx.from_pandas_edgelist(df_pk_go, "Primary", "Secondary", edge_attr=True)
edgelist = nx.to_edgelist(G)
for edge in edgelist:   
    print(f"{edge[0]},{edge[1]}\n\t{edge[2]}")

# **********************************************************************

n = df_pk_go.filter(["Primary", "Secondary"])
n = n[n["Secondary"] != "None"]

def getNetwPlot(data,serie1,serie2,title):
  G = nx.from_pandas_edgelist(data, serie1, serie2)
  edgelist = nx.to_edgelist(G)

  plt.figure(figsize=(12,8))
  nx.draw(
      G,
      with_labels = True,
      font_size = 15,
  )
  plt.title(title)
  plt.show()

getNetwPlot(n,"Primary","Secondary","Types relationship in the Pokemon GO dataset")

# **********************************************************************

n = df_pk_go.filter(["Primary", "Secondary", "Attack", "Defense", "Capture_rate"])
n = n[n["Secondary"] != "None"]

colors = [i/len(G.nodes) for i in range(len(G.nodes))]
node_color=colors,
cmap="BuPu"

G = nx.from_pandas_edgelist(df_pk_go, "Primary", "Secondary", edge_attr=True)
for i in G.degree():
    print(i)

# **********************************************************************

node_size = [v * 200 for v in dict(G.degree()).values()]
edge_size = [e[2]["serie_name"] / 500 for e in edgelist]

# **********************************************************************

def getNetwPlot(data,serie1,serie2,serie3,title):
  G = nx.from_pandas_edgelist(data, serie1, serie2, edge_attr=True)
  edgelist = nx.to_edgelist(G)

  colors = [i/len(G.nodes) for i in range(len(G.nodes))]

  plt.figure(figsize=(12,8))
  nx.draw(
      G,
      with_labels = True,
      node_size = [v * 200 for v in dict(G.degree()).values()]
      width_size = [e[2][serie3] / 500 for e in edgelist],
      font_size = 15,
      node_color = colors,
      cmap = "BuPu"
  )
  plt.title(title)
  plt.show()

getNetwPlot(n, "Primary", "Secondary", "Attack","Types relationship in the Pokemon GO dataset")

# **********************************************************************

def getNetwPlot(data,serie1,serie2,serie3,title):
  G = nx.from_pandas_edgelist(data, serie1, serie2, edge_attr=True)
  edgelist = nx.to_edgelist(G)

  colors = [i/len(G.nodes) for i in range(len(G.nodes))]

  plt.figure(figsize=(12,8))
  nx.draw(
      G,
      with_labels = True,
      node_size = [v * 200 for v in dict(G.degree()).values()]
      width_size = [e[2][serie3] / 500 for e in edgelist],
      font_size = 12,
      node_color = colors,
      cmap = "Pastel1"
  )
  plt.title(title)
  plt.show()

getNetwPlot(n, "Names1", "Names2", "Group","Names relationship for the fake names dataset")