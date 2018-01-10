from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from . import serializers
from .models import Dog, UserPref


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

    
class ListCreateDogView(generics.ListCreateAPIView,
                        generics.UpdateAPIView):
    queryset = Dog.objects.all()
    serializer_class = serializers.DogSerializer