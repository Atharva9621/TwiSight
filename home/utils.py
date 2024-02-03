from ntscraper import Nitter
from langid import classify
from transformers import pipeline

scrapper = Nitter()

scrap_params = {
    "terms": ["TrumpIndictment"],
    "mode": "hashtag", # default : term, allowed :  hashtag,user,term
    "number": 4, # default -1
    "since": None , # default None , format : YYYY-MM-DD
    "until": None, # default : None , format : YYYY-MM-DD
    "near": None,  # default : None
    "language": "en", # default : None
    "to": None, # default : None,
    "filters": None, # allowed : 'nativeretweets', 'media', 'videos', 'news', 'verified', 'native_video', 'replies', 'links', 'images', 'safe', 'quote', 'pro_video'
    "exclude": None, # default : None, allowed : same as above
    "max_retries": 5, # default : 5
    "instance": None # default : None
}

def get_pipelines():
  pipelines = {}
  pipelines["sentiment_analysis"] = pipeline(task = "sentiment-analysis",model = "cardiffnlp/twitter-roberta-base-sentiment-latest")
  return pipelines

pipelines = get_pipelines()

def get_detailed_tweets_of_topic(scrap_params,scrapper):
  try:
    tweets = scrapper.get_tweets(**scrap_params)['tweets']
  except :
    print("Failed to Fetch")
    return []
  return tweets

def extract_tweet_text(tweets):
  tweet_text = [tweet['text'] for tweet in tweets]
  return tweet_text

def get_tweet_texts(scrap_params,scrapper):
  tweet_texts = extract_tweet_text(get_detailed_tweets_of_topic(scrap_params,scrapper))
  return tweet_texts

def filter_texts(texts):
  filtered_texts = [text for text in texts if classify(text)[0] == 'en']
  return filtered_texts

def get_sentiments(texts,pipe):
  sentiments = pipe(texts)
  return sentiments

def get_tweet_texts_and_model_labels(scrap_params,scrapper,pipe):
  tweet_texts = get_tweet_texts(scrap_params,scrapper)
  filtered_texts = filter_texts(tweet_texts)
  sentiments = get_sentiments(filtered_texts,pipe)
  text_sentiments = list(zip(filtered_texts,sentiments))
  return text_sentiments

def customize_filter_params(params):
  filter_params = scrap_params.copy()
  filter_keys = list(params.keys())
  for key in filter_keys:
    if (key == "terms"):
      filter_params[key] = params[key]
    else : 
      filter_params[key] = params[key][0]
  return filter_params

def fetch_tweets_and_check_sentiments(params):
  filter_params = customize_filter_params(params)
  tweets_sentiments = get_tweet_texts_and_model_labels(filter_params,scrapper,pipelines["sentiment_analysis"])
  return tweets_sentiments

def display_list(lst):
  for elm in lst :
    print(elm)
    print("-"*20)
