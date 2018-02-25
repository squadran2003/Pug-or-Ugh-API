from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import Http404

from .serializers import DogSerializer, UserPrefSerializer, UserSerializer
from .models import Dog, UserDog, UserPref
from .utils import validate_dog_age


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()

    def post(self, format=None):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
            # set user with default preferences when account created
            UserPref.create_default_pref(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateUpdateUserPref(generics.RetrieveUpdateAPIView):

    queryset = UserPref.objects.all()
    serializer_class = UserPrefSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    def put(self, request, *args, **kwargs):
        user_pref = self.get_object()
        pref = UserPrefSerializer(user_pref, request.data)
        if pref.is_valid():
            pref.save()
            return Response(pref.data)
        return Response(pref.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDoglikedView(generics.UpdateAPIView):
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer

    def get_object(self):
        dog = get_object_or_404(Dog, pk=self.kwargs.get('pk'))
        return dog

    def put(self, request, *args, **kwargs):
        dog = self.get_object()
        obj, is_present = UserDog.objects.get_or_create(
            user=self.request.user,
            dog=dog,
            defaults={'user': self.request.user,
                      'dog': dog, 'status': 'l'}

        )
        if obj:
            obj.status = 'l'
            obj.save()
        return Response("updated to liked", status=status.HTTP_201_CREATED)


class UserDoglikedNextView(generics.UpdateAPIView):
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user,
            status='l',
        ).order_by('dog_id')

    def get_object(self):
        dog_id = self.kwargs.get('pk')
        # if the initial queryset is empty raise 404
        if not self.get_queryset():
            raise Http404
        user_dog = self.get_queryset().filter(dog_id__gt=dog_id).first()
        if user_dog is not None:
            return user_dog
        else:
            # go back to the first item in the quersets
            return self.get_queryset().first()

    def get(self, request, pk, format=None):
        user_dog = self.get_object()
        serializer = DogSerializer(user_dog.dog)
        return Response(serializer.data)


class UserDogDislikedView(generics.UpdateAPIView):
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer

    def get_object(self):
        dog = get_object_or_404(Dog, pk=self.kwargs.get('pk'))
        return dog

    def put(self, request, *args, **kwargs):
        dog = self.get_object()
        print(self.request.user)
        print(dog)
        obj,is_present = UserDog.objects.get_or_create(
            user=self.request.user,
            dog=dog,
            defaults={'user': self.request.user,
                      'dog': dog, 'status': 'd'}

        )
        if obj:
            obj.status = 'd'
            obj.save()
        return Response("updated to disliked", status=status.HTTP_201_CREATED)


class UserDogDislikedNextView(generics.UpdateAPIView):
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user,
            status='d',
        ).order_by('dog_id')

    def get_object(self):
        dog_id = self.kwargs.get('pk')
        # if the initial queryset is empty raise 404
        if not self.get_queryset():
            raise Http404
        user_dog = self.get_queryset().filter(dog_id__gt=dog_id).first()
        if user_dog is not None:
            return user_dog
        else:
            # go back to the first item in the quersets
            return self.get_queryset().first()

    def get(self, request, pk, format=None):
        user_dog = self.get_object()
        serializer = DogSerializer(user_dog.dog)
        return Response(serializer.data)


class UserDogUndecidedView(generics.UpdateAPIView):
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer

    def get_object(self):
        dog = get_object_or_404(Dog, pk=self.kwargs.get('pk'))
        return dog

    def put(self, request, *args, **kwargs):
        dog = self.get_object()
        UserDog.objects.filter(
            user=self.request.user,
            dog=dog,
        ).delete()
        return Response("deleted", status=status.HTTP_201_CREATED)


class UserDogUndecidedNextView(generics.RetrieveAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def get_queryset(self):
        user_pref = UserPref.objects.get(user=self.request.user)
        queryset = Dog.objects.filter(
            age__range=validate_dog_age(user_pref.age),
            gender__in=user_pref.gender,
            size__in=user_pref.size
        ).exclude(
            Q(users_dog__status='l') | Q(users_dog__status='d')
        ).order_by('pk')
        return queryset

    def get_object(self):
        dog_id = self.kwargs.get('pk')
        # if the initial queryset is empty raise 404
        if not self.get_queryset():
            raise Http404
        dog = self.get_queryset().filter(id__gt=dog_id).first()
        if dog is not None:
            return dog
        else:
            # go back to the first item in the querset
            return self.get_queryset().first()

    def get(self, request, pk, format=None):
        dog = self.get_object()
        serializer = DogSerializer(dog)
        return Response(serializer.data)
