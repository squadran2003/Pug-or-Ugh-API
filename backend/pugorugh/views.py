from django.contrib.auth import get_user_model
from rest_framework import generics, mixins
from rest_framework import permissions

from . import serializers
from .models import Dog, UserPref


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer

class UserPrefUpdateView(generics.ListCreateAPIView,
                        generics.UpdateAPIView):
    queryset = UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_queryset(self):
        return UserPref.objects.filter(user=self.request.user)

       

class DoglikedView(generics.CreateAPIView):
    queryset = Dog.objects.all()
    serializer_class = serializers.DogSerializer