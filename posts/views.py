from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView
from .forms import *
from accounts.models import *
from .models import *

# Create your views here.


class NewsFeed(ListView):
    model = Posts
    context_object_name = 'feeds'
    template_name = 'posts/feeds.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        follower_ids = Follow.objects.filter(follower=self.request.user).values_list('following_id')
        feeds = Posts.objects.filter(uploader_id__in=follower_ids)
        liked_posts = Likes.objects.filter(liked_by=self.request.user).values_list('Liked_post_id')
        liked_posts = [value[0] for value in liked_posts]
        context.update({
            'feeds': feeds,
            'liked_posts': liked_posts
        })
        return context


class AddPost(CreateView):
    model = Posts
    form_class = PostForm
    template_name = "posts/create_post.html"

    def post(self, request, *args, **kwargs):
        post = PostForm(request.POST,request.FILES)
        if post.is_valid():
            post = post.save(commit=False)
            post.uploader = request.user
            post.save()
            return redirect('accounts:view_profile')
        else:
            return redirect("posts:add_post")

class LikesToggle(View):
    def get(self,*args,**kwargs):
        post = Posts.objects.get(id=self.kwargs.get('post_id'))
        user = self.request.user
        like_obj = Likes.objects.filter(liked_by=user,Liked_post=post)
        response = 0

        if like_obj.count():
            like_obj.delete()
        else:
            Likes.objects.create(liked_by=user,Liked_post=post)
            response = 1

        return HttpResponse(response)