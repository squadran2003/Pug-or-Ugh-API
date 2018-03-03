from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .models import Dog, UserPref, UserDog


# Create your tests here.
class TestDogModel(TestCase):
    def setUp(self):
        Dog.objects.create(name='test_dog',
                           image_filename='test_filename',
                           breed='test_breed')

    def test_dog_created(self):
        dog = Dog.objects.get(name='test_dog')
        self.assertEqual('test_dog', dog.name)


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
        self.assertNotEqual(user_pref, None)


class TestUserDogModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
                                        username='tango',
                                        password='123'
                    )
        self.dog = Dog.objects.create(name='test_dog',
                                      image_filename='test_filename',
                                      breed='test_breed')
        UserDog.objects.create(
            user=self.user,
            dog=self.dog,
            status='l'
        )

    def test_user_dog_created(self):
        user_dog = UserDog.objects.get(
            user=self.user,
            dog=self.dog,
            status='l'
        )
        self.assertNotEqual(user_dog, None)


class TestApiViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        Dog.objects.bulk_create([
                            Dog(name='test_dog',
                                image_filename='test_filename',
                                breed='test_breed'
                                ),
                            Dog(name='test_dog2',
                                image_filename='test_filename2',
                                breed='test_breed2'
                                ),
                            Dog(name='test_dog3',
                                image_filename='test_filename3',
                                breed='test_breed3'
                                ),
                            Dog(name='test_dog4',
                                image_filename='test_filename4',
                                breed='test_breed4'
                                ),
                            ]

                        )

    def test_user_registration_view(self):
        response = self.client.post(reverse('register-user'),
                                    {'username': 'tango',
                                    'password': '123'})
        # check if a newly registered user is getting default prefs
        user = User.objects.get(
                    username='tango'
                    )
        user_pref = UserPref.objects.get(user=user)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(user_pref, None)

    def test_create_update_user_pref(self):
        user = User.objects.create_user(
            username='tango',
            password='123'
            )
        data = {'id': user.id, 'age': 'a,s', 'gender': 'm',
                'size': 'xl,m'}
        response = self.client.put(reverse('userpref-detail'),
                                   data=data)
        self.assertNotEqual(response.status_code, 400)

    def test_user_dog_liked_view(self):
        user = User.objects.create_user(username='tango',
                                        password='123')
        token, is_created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        # check for a 404 when pk is -1
        response = self.client.put(reverse('dog-liked', kwargs={'pk': '-1'}))
        self.assertEqual(response.status_code, 404)
        # check for a 201 when pk is 2
        response = self.client.put(reverse('dog-liked', kwargs={'pk': '2'}))
        self.assertEqual(response.status_code, 201)

    def test_user_dog_liked_next_view(self):
        user = User.objects.create_user(username='tango',
                                        password='123')
        token, is_created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        # check a 404 is returned if there are no liked dogs
        response = self.client.put(reverse('dog-liked-next',
                                           kwargs={'pk': '-1'}))
        self.assertEqual(response.status_code, 404)
        # set a dog with a liked status
        dog = Dog.objects.get(pk=1)
        UserDog.objects.create(
            user=user,
            dog=dog,
            status='l'

        )
        response = self.client.put(reverse('dog-liked-next',
                                           kwargs={'pk': '-1'}))
        # now i should not get a 404
        self.assertNotEqual(response.status_code, 404)

    def test_user_dog_disliked_view(self):
        user = User.objects.create_user(username='tango',
                                        password='123')
        token, is_created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        # check for a 404 when pk is -1
        response = self.client.put(reverse('dog-disliked',
                                           kwargs={'pk': '-1'}))
        self.assertEqual(response.status_code, 404)
        # check for a 201 when pk is 2
        response = self.client.put(reverse('dog-disliked', kwargs={'pk': '2'}))
        self.assertEqual(response.status_code, 201)

    def test_user_dog_disliked_next_view(self):
        user = User.objects.create_user(username='tango',
                                        password='123')
        token, is_created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        # check a 404 is returned if there are no liked dogs
        response = self.client.put(reverse('dog-disliked-next',
                                           kwargs={'pk': '-1'}))
        self.assertEqual(response.status_code, 404)
        # set a dog with a liked status
        dog = Dog.objects.get(pk=1)
        UserDog.objects.create(
            user=user,
            dog=dog,
            status='d'

        )
        response = self.client.put(reverse('dog-disliked-next',
                                           kwargs={'pk': '-1'}))
        # now i should not get a 404
        self.assertNotEqual(response.status_code, 404)

    def test_user_dog_undecided_view(self):
        user = User.objects.create_user(username='tango',
                                        password='123')
        token, is_created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        # check for a 404 when pk is -1
        response = self.client.put(reverse('dog-undecided',
                                           kwargs={'pk': '-1'}))
        self.assertEqual(response.status_code, 404)
        # check for a 201 when pk is 2
        response = self.client.put(reverse('dog-undecided',
                                           kwargs={'pk': '2'}))
        self.assertEqual(response.status_code, 201)

    def test_user_dog_undecided_next_view(self):
        user = User.objects.create_user(username='tango',
                                        password='123')
        token, is_created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        # check that the response coming back is not None
        response = self.client.put(reverse('dog-undecided-next',
                                           kwargs={'pk': '-1'}))
        self.assertNotEqual(response, None)
