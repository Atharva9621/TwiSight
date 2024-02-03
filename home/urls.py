from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage,name="homepage"),
    path("explore-tweets/<str:analysis_type>", views.explore_tweets,name="explore_tweets"),
    # path("get-user",views.get_user_info,name="get-user-info"),
    # path('debug/', views.debug_view, name='debug')
]
# path("get-tweets/<str:analysis_type>",views.get_tweet_analysis,name="get-tweet-analysis"),
