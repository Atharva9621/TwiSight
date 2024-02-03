from django.shortcuts import render
from django.http import JsonResponse
from .utils import * 

def homepage(req):
    response = JsonResponse({"message":"Homepage"})
    return response

def explore_tweets(req):
    response = JsonResponse({"message":"Tweets explorer page"})
    return response

def get_tweet_sentiments(req):
    query_params = dict(req.GET)
    tweet_sentiments = fetch_tweets_and_check_sentiments(query_params)
    response = JsonResponse({"response":tweet_sentiments})
    return response

def debug_view(req):
    page_name = req.GET.get('page_name', '')
    template_name = f'{page_name}.html'  
    return render(req, template_name)