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
PREF_AGE  = (
    ('b','baby'),
    ('y','young'),
    ('a','adult'),
    ('s','senior'),
)



class Dog(models.Model):
    name = models.CharField(max_length=50)
    image_filename = models.CharField(max_length=100)
    breed = models.CharField(max_length=50)
    age = models.IntegerField(default=12)
    gender = models.CharField(max_length=10, choices=DOG_GENDER_CHOICES, default='m')
    size = models.CharField(max_length=10, choices=DOG_SIZE_CHOICES, default='s')
    created_at = models.DateTimeField(default= timezone.now)


    def __str__(self):
        return self.name+str(self.age)
    
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
    
    @classmethod
    def load_user_dogs(cls,dogs,user):
        """loads all dogs into userdog model"""
        if dogs:
            for dog in dogs:
                cls.objects.create(
                        user=user,
                        dog=dog
                    )

    
    @classmethod
    def remove_user_dogs(cls, user):
        cls.objects.filter(user=user).delete()

    
class UserPref(models.Model):
    user = models.ForeignKey(User, related_name='user_pref')
    age = models.CharField(max_length=10,default='b')
    gender = models.CharField(max_length=10, choices= PREF_GENDER,default='m')
    size = models.CharField(max_length=10, choices= PREF_SIZE,default='s')
    created_at = models.DateTimeField(default= timezone.now)

    
    def __str__(self):
        return str(self.pk)
    
    class Meta:
        ordering = ('-created_at',)
    
    @classmethod
    def create_default_pref(cls, loggedin_user):
        """give a user default prefs when user registers"""
        user_pref = cls.objects.create(user=loggedin_user)
        return user_pref
    
    @classmethod
    def get_dogs(cls,user_pref):
        """get all dogs based on past in pref"""
        dogs = Dog.objects.filter(
            age__range=validate_dog_age(user_pref.age),
            gender=user_pref.gender,
            size=user_pref.size
        )
        return dogs
    



def validate_dog_age(letter):
    """this function takes a letter as age 
    and returns a tuple or range of ages"""
    if letter.lower() =='b':
        return (1,7)
    elif letter.lower() == 'y':
        return (7,13)
    elif letter.lower() == 'a':
        return (13,25)
    else:
        return (25,80)

    





