from django.shortcuts import render
from django.http import JsonResponse
from .utils import * 

def homepage(req):
    return render(req, "index.html")

def explore_tweets(req, analysis_type="sentiment"):
    print(req.method)
    if req.method == "POST":
        filter_params = dict(req.POST)
        print(filter_params)
        tweet_analysis = fetch_and_analyse_tweets(analysis_type, filter_params)
        counts, metric = get_sentiment_metrics(tweet_analysis, analysis_type)
        labels = list(counts.keys())
        values = list(counts.values())
        context = {
        'empty_list': False,
        'first_visit': True,
        'tweets': tweet_analysis,
        'labels': labels,
        'values': values,
        'metric': metric
        }
        print("Tweets : ", tweet_analysis)
        if len(tweet_analysis)==0:
            print("Im so empty")
            context['empty_list'] = True
            print(context)
        return render(req, f"explore_{analysis_type}.html", context)   
    else:
        return render(req, f"explore_{analysis_type}.html", {'first_visit': False})  

# def get_tweet_analysis(req, analysis_type):
#     filter_params = dict(req.GET)
#     tweet_analysis, counts, metric = fetch_and_analyse_tweets(analysis_type,filter_params)
#     labels = list(counts.keys())
#     values = list(counts.values())
#     context = {
#         'tweets': tweet_analysis,
#         'labels': labels,
#         'values': values
#     }
#     return render(req, "explore.html", context)

def get_user_info(req):
    username = req.GET['username']
    info = fetch_user_info(username)
    response = JsonResponse({"info": info})
    return response

def debug_view(req):
    page_name = req.GET.get('page_name', '')
    template_name = f'{page_name}.html'  
    return render(req, template_name)
