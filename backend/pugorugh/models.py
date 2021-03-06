from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

GENDER_CHOICES = (
    ('m', "male"),
    ('f', 'female'),
    ('u', 'unknown')
)
SIZE_CHOICES = (
    ('s', 'small'),
    ('m', 'medium'),
    ('l', 'large'),
    ('xl', 'extra large'),
    ('u', 'unknown')
)
STATUS_CHOICES = (
    ('l', 'Liked'),
    ('d', 'disliked'),
    ('U', 'undicided')
)


class Dog(models.Model):
    name = models.CharField(max_length=50)
    image_filename = models.CharField(max_length=100)
    breed = models.CharField(max_length=50)
    age = models.IntegerField(default=12)
    gender = models.CharField(max_length=10,
                              choices=GENDER_CHOICES,
                              default='m')
    size = models.CharField(max_length=10,
                            choices=SIZE_CHOICES,
                            default='s')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name+str(self.age)

    class Meta:
        ordering = ('-created_at',)


class UserDog(models.Model):
    user = models.ForeignKey(User, related_name='user')
    dog = models.ForeignKey(Dog, related_name='users_dog')
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='U')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} : {}".format(self.user, self.dog)

    class Meta:
        ordering = ('-created_at',)


class UserPref(models.Model):
    user = models.ForeignKey(User, related_name='user_pref')
    age = models.CharField(max_length=10, default='b')
    gender = models.CharField(max_length=10, default='m')
    size = models.CharField(max_length=10, default='s')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ('-created_at',)

    @classmethod
    def create_default_pref(cls, user):
        cls.objects.create(user=user)
