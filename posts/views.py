from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from .forms import *
from accounts.models import *

# Create your views here.

class NewsFeed(ListView):
    model = Posts
    context_object_name = 'feeds'
    template_name = 'posts/feeds.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        follower_ids = Follow.objects.filter(follower=self.request.user).values_list('following_id')
        feeds = Posts.objects.filter(uploader_id__in=follower_ids)
        context.update({
            'feeds': feeds
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