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

def debug_view(req):
    page_name = req.GET.get('page_name', '')
    template_name = f'{page_name}.html'  
    return render(req, template_name)