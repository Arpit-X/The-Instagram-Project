from django.urls import path
from.views import *
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm

urlpatterns = [
    path('login/', LoginFormView.as_view(), name="login_form"),
    path('signup/', SignUpFormView.as_view(), name="Signup_form"),
    path('profile/', view_profile, name="view_profile"),
    path('reset-password/', password_reset, name="password_reset"),
    path('reset-password/done/', password_reset_done, name='password_reset_done'),
    path('reset-password/confirm/', password_reset_confirm, name='password_reset_confirm')
]