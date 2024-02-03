from ntscraper import Nitter
from langid import classify
from transformers import pipeline
import os
import json

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
  pipelines["sentiment"] = pipeline(task = "sentiment-analysis",model = "cardiffnlp/twitter-roberta-base-sentiment-latest")
  pipelines["toxicity"] = pipeline(task = "text-classification",model = "facebook/roberta-hate-speech-dynabench-r4-target")
  pipelines["depression"] = pipeline(task = "text-classification", model = "paulagarciaserrano/roberta-depression-detection")
  pipelines["spam"] = pipeline(task= "text-classification",model = "mariagrandury/roberta-base-finetuned-sms-spam-detection")
  # pipelines["nsfw"] = pipeline(task = "text-classification",model = "michellejieli/NSFW_text_classifier")
  return pipelines

pipelines = get_pipelines()

def get_detailed_tweets_of_topic(scrap_params,scrapper):
  tweets = scrapper.get_tweets(**scrap_params)['tweets']
  return tweets

def extract_tweet_text(tweets):
  tweet_texts = [tweet['text'] for tweet in tweets]
  tweet_users = [tweet['user']['name'] for tweet in tweets] 
  return (tweet_texts,tweet_users)

def get_tweet_texts_and_users(scrap_params,scrapper):
  (tweet_texts,tweet_users) = extract_tweet_text(get_detailed_tweets_of_topic(scrap_params,scrapper))
  return (tweet_texts,tweet_users)

def filter_texts(texts):
  filtered_texts = [text for text in texts if classify(text)[0] == 'en']
  return filtered_texts

def get_sentiments(texts,pipe):
  sentiments = pipe(texts)
  return sentiments

def organize_data(texts, sentiments, users): 
  l = len(texts)
  for i in range (l):
    sentiments[i]["text"] = texts[i]
    sentiments[i]["user"] = users[i]
    sentiments[i]["score"] = round(sentiments[i]["score"]*100, 2)
  return sentiments

def get_tweet_texts_and_model_labels(scrap_params,scrapper,pipe):
  (tweet_texts,tweet_users) = get_tweet_texts_and_users(scrap_params,scrapper)
  filtered_texts = filter_texts(tweet_texts)
  sentiments = get_sentiments(filtered_texts,pipe)
  text_sentiments = organize_data(filtered_texts,sentiments,tweet_users)
  return text_sentiments

def customize_filter_params(params):
  filter_params = scrap_params.copy()
  filter_keys = list(params.keys())
  for key in filter_keys:
    if (key == "terms"):
      filter_params[key] = params[key]
    elif (key == "number"):
      filter_params[key] = int(params[key][0])
    elif params[key][0]=='none':
        print(key)
        filter_params[key] = None
    else:
      filter_params[key] = params[key][0]
  return filter_params

def get_tweets_from_file(term):
  base_path = "./home/static/jsons"
  folder_name = term
  file_name = term + ".json"
  file_path = os.path.join(base_path,folder_name,file_name)
  f = open(file_path)
  data = f.read()
  data_dict = json.loads(data)
  return data_dict["predictions"]

def get_sentiment_metrics(analysed_tweets, analysis):
    if analysis=="sentiment":
      counts = {'positive': 0, 'negative': 0, 'neutral': 0}
      metric = 0
      l = len(analysed_tweets)
      for tweet in analysed_tweets:
        counts[tweet['label']]+=1
        if tweet['label']=='positive':
          metric += tweet["score"]
        elif tweet['label']=='neutral':
          metric += 0.5*tweet["score"]
        else:
          metric += 100-tweet["score"]  
      return counts, metric/(1+(counts['positive']+counts['negative']))
    elif analysis=="toxicity":
      counts = {'hate': 0, 'nothate': 0}
      metric = 0
      l = len(analysed_tweets)
      for tweet in analysed_tweets:
        counts[tweet['label']]+=1
        if tweet['label']=='hate':
          metric += tweet["score"]
        else:
          metric += 100-tweet["score"]
      return counts, metric/(1+(counts['hate']+counts['nothate']))    
    elif analysis=="depression":
      counts = {'moderate': 0, 'severe': 0, 'not depression': 0}
      metric = 0
      l = len(analysed_tweets)
      for tweet in analysed_tweets:
        counts[tweet['label']]+=1
        if tweet['label']=='severe':
          metric += tweet["score"]
        elif tweet['label']=='moderate':
          metric += tweet["score"]/2
      return counts, metric/(1+(counts['moderate']+counts['severe']+counts['not depression']))
    elif analysis=="spam":
      counts = {'LABEL_0': 0, 'LABEL_1': 0}
      metric = 0
      l = len(analysed_tweets)
      for tweet in analysed_tweets:
        counts[tweet['label']]+=1
        if tweet['label']=='LABEL_0':
          metric += tweet["score"]
        else:
          metric += 100-tweet["score"]
      return counts, metric/(1+(counts['LABEL_0']+counts['LABEL_1']))    

    else:
      return {'hate': 100, 'nohate': 0}, 3.1415



def fetch_and_analyse_tweets(analysis_type,params):
  pipe = pipelines[analysis_type]
  analysed_tweets = []
  try : 
    filtered_params = customize_filter_params(params)
    analysed_tweets = get_tweet_texts_and_model_labels(filtered_params,scrapper,pipe)
    if(analysed_tweets == []):
      raise NameError("Empty list")
  except Exception as e: 
    print(e)
    term = params["terms"][0]
    try : 
      analysed_tweets = get_tweets_from_file(term)
    except Exception as e: 
      print(e) 
      analysed_tweets = []
  return analysed_tweets

def display_list(lst):
  for elm in lst :
    print(elm)
    print("-"*20)

user_scrap_params = {
    "username":"imVkohli",
    "max_retries":5,
    "instance" : None,
}

def fetch_user_info(username):
  user_scrap_params["username"] = username
  profile = scrapper.get_profile_info(**user_scrap_params)
  return profile
