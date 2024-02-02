from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage,name="homepage"),
    path("explore-tweets", views.explore_tweets,name="explore_tweets"),
    path("get-tweets",views.get_tweets,name="get-tweets")
]
