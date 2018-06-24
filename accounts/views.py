from django.shortcuts import render
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from .forms import *
from .models import  Follow
# Create your views here.


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
                return redirect('accounts:login_form')
            else:
                return redirect('accounts:SignUpform')

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
    args = {
        'user':user,
        'followers': followers,
        'following': following
        }
    return render(request,'accounts/profile.html',args)