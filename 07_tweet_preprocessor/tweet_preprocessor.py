pip install tweet-preprocessor

# **********************************************************************

import pandas as pd
import preprocessor as tp

tweets = {
    "text": [
          "#regularexpressions suck but #perl is awesome",
          "Hey @elonmusk what's up?",
          "This is awesome https://pypi.org/project/tweet-preprocessor/"
          ]
}

df = pd.DataFrame(tweets)
df

# **********************************************************************

df["cleaned"] = df["text"].apply(lambda x: tp.clean(x))
df

# **********************************************************************

df["url"] = df["text"].apply(lambda x: tp.parse(x).urls)
df

# **********************************************************************

text = "@RT if you like that content, and use a #hashtag so that 99999999 people on https://twitter.com can find you!"

tp.set_options(tp.OPT.URL, tp.OPT.MENTION, tp.OPT.NUMBER)
tp.clean(text)