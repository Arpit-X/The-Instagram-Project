from django.urls import path
from .views import *

app_name = "posts"

urlpatterns = [
    path('',NewsFeed.as_view(),name="news_feed"),
    path('add/',AddPost.as_view(),name="add_post")
]