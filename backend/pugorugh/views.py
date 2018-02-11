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
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer
    
    def get_object(self):
        dog = get_object_or_404(Dog,pk=self.kwargs.get('pk'))
        return dog
    
    def put(self,request, *args, **kwargs):
        dog = self.get_object()
        try:
            UserDog.objects.get(
                user=self.request.user,
                dog=dog,
            )
        except UserDog.DoesNotExist:
            "if the dog doesnt have a status create it"
            UserDog.objects.create(
                user = self.request.user,
                dog=dog,
                status='l'
            )
        else:
            "else update the status"
            UserDog.objects.filter(
                user=self.request.user,
                dog=dog,
            ).update(status='l')

        return Response("updated", status=status.HTTP_201_CREATED)

        

class UserDoglikedNextView(generics.UpdateAPIView):
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user,
            status='l',
        ).order_by('pk')
    
    def get_object(self):
        dog_id = self.kwargs.get('pk')
        # if the initial queryset is empty raise 404
        print(self.get_queryset())
        if not self.get_queryset():
            raise Http404
        user_dog= self.get_queryset().filter(dog_id__gt=dog_id).first()
        if user_dog is not None:
            return user_dog
        else:
            # go back to the first item in the quersets
            return self.get_queryset().first()
    
    def get(self, request, pk, format=None):
        user_dog = self.get_object()
        serializer = DogSerializer(user_dog.dog)
        return Response(serializer.data)




class UserDogUndecidedNextView(generics.RetrieveAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


    def get_queryset(self):
        user_pref = UserPref.objects.get(user=self.request.user)
        queryset = Dog.objects.filter(
            age__range=validate_dog_age(user_pref.age),
            gender__in=user_pref.gender,
            size__in=user_pref.size
        ).exclude(Q(users_dog__status='l')|Q(users_dog__status='d')).order_by('pk')
        return queryset

    def get_object(self):
        dog_id = self.kwargs.get('pk')
        # if the initial queryset is empty raise 404
        if not self.get_queryset():
            raise Http404
        dog= self.get_queryset().filter(id__gt=dog_id).first()
        if dog is not None:
            return dog
        else:
            # go back to the first item in the querset
            return self.get_queryset().first()
        

    def get(self, request, pk, format=None):
        dog = self.get_object()
        serializer = DogSerializer(dog)
        return Response(serializer.data)


def validate_dog_age(letter):
    """this function takes a letter as age 
    and returns a tuple or range of ages"""
    
    if "b,y,a,s" in letter:
        return (1,97)
    elif "b,y" in letter:
        return (1,26)
    elif "a,s" in letter:
        return (25,97)
    elif 'b' in letter:
        return (1,13)
    elif 'y' in letter:
        return (13,26)
    elif 'a' in letter:
        return (25,38)
    else:
        return (37,97)



        







