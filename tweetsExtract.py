
import tweepy as tw
import pandas as pd

def tweet_extractor(keywords, start_date, n_tweets):
    consumer_key="ArvY8sU6HDZSuGk9nMADCd1Za"
    consumer_secret="WhhxixavlxGgAsr6nHwwjmsEDdNCBGCC2LxHJWLl0Tho5OcTKe"
    access_token="2415738176-GCKuN5W25sftYfjOMXMgA1UXaS6kHkl8gYnMWGm"
    access_token_secret="GBzgC4NrDA4XhCf7CS6md1zQuNmm0o458rhJSqfz3PFki"

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    
    n_tweets = int(n_tweets)
    count_each_keyword = n_tweets/len(keywords)
    
    user_names = []
    location = []
    text = []
    keyword=[]
    for word in keywords:
        search_words = word+" -filter:retweets" 
        #"wildfires+climate -filter:retweets"  #-filter:retweets :this is removing the retweets
        # if we pass word(game+ps5) then it will look for the sentences where both are present in a sentence.
        date_since = start_date
        # Collect tweets
        
        tweets = tw.Cursor(api.search,
                    q=search_words,
                    lang="en",
                    since=date_since).items(count_each_keyword)

        # Iterate and print tweets
        # acess location- tweet.user.location
        # acess name- tweet.user.screen_name
        # acess text- tweet.text
        for tweet in tweets:
            user_names.append(tweet.user.screen_name)
            location.append(tweet.user.location)
            text.append(tweet.text)
            keyword.append(word)
    
    dataset = pd.DataFrame(columns = ['UserName', 'Location', 'Text', 'Keyword'])
    dataset["UserName"] = user_names
    dataset["Location"] = location
    dataset["Text"] = text
    dataset["Keyword"] = keyword
    dataset = dataset.sample(frac=1)
    dataset.reset_index(drop=True, inplace=True) 
    return dataset


def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')