from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status, mixins
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .serializers import *
from .models import *


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()

    def post(self,format=None):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserPref.objects.create_default_pref(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateUpdateUserPref(generics.ListCreateAPIView,
                                generics.UpdateAPIView):
    queryset = UserPref.objects.all()
    serializer_class = UserPrefSerializer
    

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,user=self.request.user)
        return obj


class UserDoglikedView(generics.UpdateAPIView):
    queryset = UserDog.objects.all()
    serializer_class = UserDogSerializer

    def get_object(self):
        dog_id = self.kwargs.get('pk')
        if int(dog_id)< 1:
            dog_id = 1
        return get_object_or_404(Dog,pk=dog_id)

    def put(self, request, pk, format=None):
        print("put was called")
        print(self.request.user)
        print(self.get_object())
        print(self.request.data.get('status'))
        dog = self.get_object()
        self.update(request,user=self.request.user,
                    dog=dog,status=self.request.data.get('status'))
        return Response("Record updated",status=status.HTTP_200_OK)
        





    



        
        
class UserDogDislikedView(generics.ListCreateAPIView,
                            generics.UpdateAPIView):
    pass

class UserDogUndecidedView(generics.ListCreateAPIView,
                            generics.RetrieveUpdateDestroyAPIView):
    pass


class UserDogUndecidedNextView(APIView):
    pass


        







