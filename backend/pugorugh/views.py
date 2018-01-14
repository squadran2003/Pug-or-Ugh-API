from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from . import serializers
from .models import *


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()

    def post(self,format=None):
        serializer = serializers.UserSerializer(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserPref.objects.create_default_pref(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateUpdateUserPref(generics.ListCreateAPIView,
                                generics.UpdateAPIView):
    queryset = UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer
    

    def get_queryset(self):
        queryset = UserPref.objects.filter(user=self.request.user)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,user=self.request.user)
        return obj

    
class UserDoglikedView(generics.ListCreateAPIView,
                            generics.UpdateAPIView):
    queryset = UserDog.objects.all()
    serializer_class = serializers.UserDog

    def queryset(self):
        user_pref = UserPref.objects.get(user=self.request.user)
        dog = get_object_or_404(Dog,pk=self.kwargs.get('pk'))
        return UserDog.objects.filter(user=self.request.user,
                                        dog=dog,
                                        liked='l')
    def get_object(self):
        queryset = self.get_queryset()
        dog = get_object_or_404(Dog,pk=self.kwargs.get('pk'))
        obj = get_object_or_404(user=self.request.user,
                                dog=dog)
        return obj

class UserDoglikedNextView(generics.ListCreateAPIView,
                            generics.UpdateAPIView):
    queryset = UserDog.objects.all()
    serializer_class = serializers.UserDog

    def queryset(self):
        user_pref = UserPref.objects.get(user=self.request.user)
        dog = get_object_or_404(Dog,pk=self.kwargs.get('pk'))
        return UserDog.objects.filter(user=self.request.user,
                                        dog=dog,
                                        liked='l').order_by('id')[:1]







