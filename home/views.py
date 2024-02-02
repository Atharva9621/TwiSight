from django.shortcuts import render
from django.http import JsonResponse

def homepage(req):
    response = JsonResponse({"message":"Homepage"})
    return response

def explore_tweets(req):
    response = JsonResponse({"message":"Tweets explorer page"})
    return response

def get_tweets(req):
    response = JsonResponse({"message":"Get Tweets endpoint"})
    return response