from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime

DOG_GENDER_CHOICES = (
    ('m',"male"),
    ('f','female'),
    ('u','unknown')
)
DOG_SIZE_CHOICES = (
    ('s','small'),
    ('m','medium'),
    ('l','large'),
    ('xl','extra large'),
    ('u','unknown')
)
STATUS_CHOICES = (
    ('l','Liked'),
    ('d','disliked'),
    ('U','undicided')
)
PREF_AGE_CHOICES = (
    ('b','baby'),
    ('y','young'),
    ('a','adult'),
    ('s','senior')
)
PREF_GENDER = (
    ('m',"male"),
    ('f','female'),
)
PREF_SIZE = (
    ('s','small'),
    ('m','medium'),
    ('l','large'),
    ('xl','extra large')
)

class Dog(models.Model):
    name = models.CharField(max_length=50)
    image_filename = models.CharField(max_length=100)
    breed = models.CharField(max_length=50)
    age = models.CharField(max_length=10, choices=PREF_AGE_CHOICES, default='b')
    gender = models.CharField(max_length=10, choices=DOG_GENDER_CHOICES, default='m')
    size = models.CharField(max_length=10, choices=DOG_SIZE_CHOICES, default='s')
    created_at = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return self.name+str(self.pk)
    
    class Meta:
        ordering = ('-created_at',)

class UserDog(models.Model):
    user = models.ForeignKey(User,related_name='user')
    dog = models.ForeignKey(Dog,related_name='users_dog')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='U')
    created_at = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return "{} : {}".format(self.user, self.dog)
    
    class Meta:
        ordering = ('-created_at',)


class DefaultUserPref(models.Manager):
    def create_default_pref(self, loggedin_user):
        self.create(user=loggedin_user)
    

class UserPref(models.Model):
    user = models.ForeignKey(User, related_name='user_pref')
    age =  models.CharField(max_length=10, choices=PREF_AGE_CHOICES, default='b')
    gender = models.CharField(max_length=5, choices= PREF_GENDER,default='m')
    size = models.CharField(max_length=5, choices= PREF_SIZE,default='s')
    created_at = models.DateTimeField(default= timezone.now)

    objects = DefaultUserPref()
    
    def __str__(self):
        return str(self.pk)
    
    class Meta:
        ordering = ('-created_at',)
    





