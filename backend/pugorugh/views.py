from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.reverse import reverse
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
        pref = UserPrefSerializer(user_pref,request.data)
        if pref.is_valid():
            pref.save()
            return Response(pref.data)
        return Response(pref.errors, status=status.HTTP_400_BAD_REQUEST)




class UserDoglikedView(generics.UpdateAPIView):
    pass
        

class UserDogDislikedView(generics.UpdateAPIView):
    pass


class UserDogUndecidedView(generics.ListCreateAPIView,
                            generics.RetrieveUpdateDestroyAPIView):
    pass


class UserDogUndecidedNextView(generics.RetrieveAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


    def get_queryset(self):
        user_pref = UserPref.objects.get(user=self.request.user)
        queryset = Dog.objects.filter(
            age__range=validate_dog_age(user_pref.age),
            gender__in=user_pref.gender,
            size__in=user_pref.size
        )
        print(queryset)
        return queryset

    def get_object(self):
        dog_id = self.kwargs.get('pk')
        # if the initial queryset is empty raise 404
        if not self.get_queryset():
            raise Http404
        elif self.get_queryset()==[]:
            return reverse('UserDogUndecidedNextView',request=self.request)
        else:
            dog= self.get_queryset().filter(id__gt=dog_id).first()
        return dog
        

    def get(self, request, pk, format=None):
        dog = self.get_object()
        serializer = DogSerializer(dog)
        return Response(serializer.data)


def validate_dog_age(letter):
    """this function takes a letter as age 
    and returns a tuple or range of ages"""
    
    if "s,b,y,a" in letter:
        return (1,84)
    elif "s,b" in letter:
        return (1,24)
    elif "y,a" in letter:
        return (25,84)
    elif 'b' in letter:
        return (1,12)
    elif 's' in letter:
        return (12,24)
    elif 'y' in letter:
        return (25,36)
    else:
        return (45,80)



        







