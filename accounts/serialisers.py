from .models import *
from rest_framework import serializers


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ProfileSerialisers(serializers.ModelSerializer):
    user = UserSerialiser()

    class Meta:
        model = UserProfile
        fields = ('id', 'display_picture', 'user')
