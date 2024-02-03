from django.shortcuts import render
from django.http import JsonResponse
from .utils import * 

def homepage(req):
    response = JsonResponse({"message":"Homepage"})
    return response

def explore_tweets(req):
    response = JsonResponse({"message":"Tweets explorer page"})
    return response

def get_tweet_analysis(req,analysis_type):
    filter_params = dict(req.GET)
    tweet_analysis = fetch_and_analyse_tweets(analysis_type,filter_params)
    response = JsonResponse({"messsage":tweet_analysis})
    return response

def get_user_info(req):
    username = req.GET['username']
    info = fetch_user_info(username)
    response = JsonResponse({"info": info})
    return response