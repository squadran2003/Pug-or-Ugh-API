from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status, mixins
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import Http404

from .serializers import *
from .models import *


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()

    def post(self,format=None):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
            # set user with default preferences when account created
            user_pref = UserPref.create_default_pref(user)
            dogs = UserPref.get_dogs(user_pref)
            UserDog.load_user_dogs(dogs,self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateUpdateUserPref(generics.RetrieveUpdateAPIView):
    
    queryset = UserPref.objects.all()
    serializer_class = UserPrefSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,user=self.request.user)
        return obj

    def put(self, request, *args, **kwargs):
        user_pref = self.get_object()
        dogs = UserPref.get_dogs(user_pref)
        UserDog.load_user_dogs(dogs,self.request.user)
        return self.update(request, *args, **kwargs)




class UserDoglikedView(generics.UpdateAPIView):
    pass
        

class UserDogDislikedView(generics.UpdateAPIView):
    pass


class UserDogUndecidedView(generics.ListCreateAPIView,
                            generics.RetrieveUpdateDestroyAPIView):
    pass


class UserDogUndecidedNextView(generics.RetrieveAPIView):
    #queryset = UserDog.objects.all()
    serializer_class = UserDogSerializer


    def get_queryset(self):
        return UserDog.objects.filter(status='U',user=self.request.user)

    def get_object(self):
        dog_id = self.kwargs.get('pk')
        # reverse relationship here
        record= self.get_queryset().filter(dog_id__gt=dog_id).first()
        return record

    def get(self, request, pk, format=None):
        record = self.get_object()
        if not record:
            # if last dog is reached, go back to the first one
            record = self.get_queryset().first()
        serializer = DogSerializer(record.dog)
        return Response(serializer.data)



        







