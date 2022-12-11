import numpy as np
import pandas as pd

def getDataFrame():
    df = pd.DataFrame(
        np.random.randint(0,100,size=(100, 12)),
        columns=list("ABCDEFGHIJKL")
        )
    return df 

df = getDataFrame() 
df

# **********************************************************************

pip install joypy

# **********************************************************************

import joypy
import pandas as pd
from matplotlib import cm
from matplotlib import style

# **********************************************************************

fig, axes = joyplot(df)

# **********************************************************************

def getJoyPlot(data,title):
    fig, ax = joyplot(
              data=data, 
              figsize=(15,10),
              colormap=cm.magma,
              tails=0.2,
              overlap=0.3,
	      linewidth=3,
              fade=True,
              bins=30,
              title=title
                );

getJoyPlot(df,"Distribution comparison")