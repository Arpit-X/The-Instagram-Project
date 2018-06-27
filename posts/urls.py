from django.urls import path
from .views import *
from .rest_views import *
app_name = "posts"

urlpatterns = [
    path('',NewsFeed.as_view(),name="news_feed"),
    path('add/',AddPost.as_view(),name="add_post"),
    path('likes/api/', LikesListApi.as_view(), name="user_likes_api"),
    path('like/<int:post_id>',LikesToggle.as_view(),name="like_toggle"),
]