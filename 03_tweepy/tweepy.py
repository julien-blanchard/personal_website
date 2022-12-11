import pandas as pd 
import tweepy

def getKeys(file_name):
    with open(file_name, "r") as keys_csv:
        for key in keys_csv.readlines():
            keys = [k.replace('"',"") for k in key.split(",")]
            twitter_keys = {
                "consumer_key":        keys[0],
                "consumer_secret":     keys[1],
                "access_token_key":    keys[2],
                "access_token_secret": keys[3]
                }
    return twitter_keys

# **********************************************************************

def getAccess(twitter_keys):
    auth = tweepy.OAuthHandler(
        twitter_keys["consumer_key"],
        twitter_keys["consumer_secret"]
        )
    auth.set_access_token(
        twitter_keys["access_token_key"],
        twitter_keys["access_token_secret"]
                        )
    api = tweepy.API(
        auth,
        wait_on_rate_limit=True
                   )
    return api

# **********************************************************************

def getStruct():
  data = {
      "created": [],
      "author": [],
      "favorites": [],
      "retweets": [],
      "tweet": [],
      "replying_to": [],
      "quoted": [],
      "place": [],
      "favorited": [],
      "retweeted": [],
      "geo": []
      }
  return data

# **********************************************************************

def getTweets(choice,user=None,query=None,volume):

    def getUser(id_user):
      try:
        api.get_user(id = c.id_user).user_name
      except:
        return "Unknown"

    keys = getKeys("tweepy.csv")
    api = getAccess(keys)
    data = getStruct()
    if choice == "u":
      cursor = tweepy.Cursor(
          api.user_timeline,
          id=user,
          tweet_mode="extended"
          ).items(volume)
      for c in cursor:
        data["created"].append(c.created_at),
        data["author"].append(getUser(c.id)),
        data["favorites"].append(c.favorite_count),
        data["retweets"].append(c.retweet_count),
        data["tweet"].append(c.full_text),
        data["replying_to"].append(c.in_reply_to_screen_name),
        data["quoted"].append(c.is_quote_status),
        data["place"].append(c.place),
        data["favorited"].append(c.favorited),
        data["retweeted"].append(c.retweeted),
        data["geo"].append(c.geo)
      df = pd.DataFrame(data)
    elif choice == "q":
      cursor = tweepy.Cursor(
          api.search,
          q=query,
          tweet_mode="extended"
          ).items(volume)
      for c in cursor:
          data["created"].append(c.created_at),
          data["author"].append(getUser(c.id)),
          data["favorites"].append(c.favorite_count),
          data["retweets"].append(c.retweet_count),
          data["tweet"].append(c.full_text),
          data["replying_to"].append(c.in_reply_to_screen_name),
          data["quoted"].append(c.is_quote_status),
          data["place"].append(c.place),
          data["favorited"].append(c.favorited),
          data["retweeted"].append(c.retweeted),
          data["geo"].append(c.geo)
      df = pd.DataFrame(data)
    else:
      print("Wrong input")
    df["time"] = pd.to_datetime(df["created"]).dt.time
    df["created"] = pd.to_datetime(df["created"]).dt.to_period("D")
    return df

# **********************************************************************

def getUserInfo(twitter_handle,volume):
    keys = getKeys("tweepy.csv")
    api = getAccess(keys)
    followers = [f.screen_name for f in tweepy.Cursor(api.followers, twitter_handle).items(volume)]
    following = [f.screen_name for f in tweepy.Cursor(api.friends, twitter_handle).items(volume)]
    df = pd.DataFrame({"following": pd.Series(following), "followers": pd.Series(followers)})
    return df