from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from posts.models import *
# Create your views here.


class UserListView(ListView):
    model = UserProfile
    context_object_name = 'data'
    template_name = 'accounts/users_list.html'
    def get_queryset(self):
        return UserProfile.objects.filter(~Q(user=self.request.user))


class UserDetailView(DetailView):
    model = UserProfile
    def get_context_data(self, **kwargs):

        context = super(UserDetailView,self).get_context_data(**kwargs)
        profile = UserProfile.objects.get(pk=self.kwargs['pk'])
        user = profile.user
        followers = Follow.objects.filter(following=user).count()
        following = Follow.objects.filter(follower=user).count()
        isFollowing = Follow.objects.filter(follower=self.request.user,following=user ).count()
        posts = Posts.objects.filter(uploader=user)
        context.update({
            'followers': followers,
            'following': following,
            'user': user,
            'isFollowing': isFollowing,
            'posts':posts
        })
        return context


class FollowToggle(View):

    def get(self,*args,**kwargs):
        follower = self.request.user
        following = User.objects.get(id=self.kwargs.get('id'))
        following_obj = Follow.objects.filter(following=following,follower=follower)
        response = 0
        if following_obj.count():
            following_obj.delete()

        else:
            Follow.objects.create(follower=follower,following=following)
            response = 1

        return HttpResponse(response)


class LoginFormView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(
            request,
            template_name='accounts/login_form.html',
            context={
                'form': form
            }
        )

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:

                login(request,user)
                return redirect('posts:news_feed')
            else:
                return redirect('accounts:Signup_form')


class SignUpFormView(View):

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        return render(
            request,
            template_name='accounts/signup_form.html',
            context={
                'form': form
            }
        )

    def post(self, request, *args, **kwargs):
        # import ipdb
        # ipdb.set_trace()
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:

                login(request,user)
                return redirect('accounts:login_form')
            else:
                return redirect('accounts:SignUpform')
        else:
            return render(
                request,
                template_name='accounts/signup_form.html',
                context={
                    'form': form,
                    'errors':form.errors
                }
            )


def view_profile(request):
    user = request.user
    followers = Follow.objects.filter(following=user).count()
    following = Follow.objects.filter(follower=user).count()
    posts = Posts.objects.filter(uploader=user)
    args = {
        'user': user,
        'followers': followers,
        'following': following,
        'posts': posts
        }
    return render(request,'accounts/profile.html',args)


class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login_form')