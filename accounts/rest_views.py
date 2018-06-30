from rest_framework import  generics
from .serialisers import *


class SearchApi(generics.ListCreateAPIView):
    serializer_class = ProfileSerialisers

    def get_queryset(self):
        return UserProfile.objects.filter(user__username__icontains=self.kwargs['slug'])