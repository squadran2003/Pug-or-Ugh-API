from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .models import Dog, UserPref, UserDog

# Create your tests here.
class TestDogModel(TestCase):
    def setUp(self):
        dog = Dog.objects.create(name='test_dog',
                                 image_filename='test_filename',
                                 breed='test_breed'
                                 )
    def test_dog_created(self):
        dog = Dog.objects.get(name='test_dog')
        self.assertEqual('test_dog',dog.name)

class TestUserPrefModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='tango',
            password='123'
        )
        UserPref.objects.create(
            user=self.user
        )
    
    def test_user_pref_created(self):
        user_pref = UserPref.objects.get(user=self.user)
        self.assertNotEqual(user_pref,None)

class TestUserDogModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='tango',
            password='123'
        )
        self.dog = Dog.objects.create(name='test_dog',
                            image_filename='test_filename',
                            breed='test_breed'
                            )
        UserDog.objects.create(
            user=self.user,
            dog = self.dog,
            status='l'
        )
    
    def test_user_dog_created(self):
        user_dog = UserDog.objects.get(
            user = self.user,
            dog = self.dog,
            status='l'
        )
        self.assertNotEqual(user_dog,None)

class TestApiViews(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_user_registration_view(self):
        response = self.client.post(reverse('register-user'),
                                    {'username':'tango',
                                    'password':'123'})
        #check if a newly registered user is getting default prefs
        user = User.objects.get(
                    username='tango'
                    )
        user_pref = UserPref.objects.get(user=user)
        self.assertEqual(response.status_code,201)
        self.assertNotEqual(user_pref,None)
    
    def test_create_update_user_pref(self):
        user = User.objects.create_user(
            username='tango',
            password='123'
            )
        data = {'id':user.id,'age':'a,s','gender':'m',
                'size':'xl,m'}
        response = self.client.put(reverse('userpref-detail'),
                                   data=data)
        self.assertNotEqual(response.status_code,400)
    
    def test_user_dog_liked_view(self):
        user = User.objects.create_user(username='tango',
                                        password='123')
        token = Token.objects.get_or_create(user=user)
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.put(reverse('dog-liked',kwargs={'pk':'-1'}),{},**header)
        self.assertEqual(response.status_code,201)



        





