from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from .views import (UserDogDislikedNextView, UserDogDislikedView,
                    UserDoglikedNextView, UserDoglikedView,
                    UserDogUndecidedNextView, UserDogUndecidedView,
                    ListCreateUpdateUserPref, UserRegisterView)

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/dog/(?P<pk>-?\d+)/liked/$', UserDoglikedView.as_view(),
        name='dog-liked'),
    url(r'^api/dog/(?P<pk>-?\d+)/liked/next/$', UserDoglikedNextView.as_view(),
        name='dog-liked-next'),
    url(r'^api/dog/(?P<pk>-?\d+)/disliked/$', UserDogDislikedView.as_view(),
        name='dog-disliked'),
    url(r'^api/dog/(?P<pk>-?\d+)/disliked/next/$',
        UserDogDislikedNextView.as_view(),
        name='dog-disliked-next'),
    url(r'^api/dog/(?P<pk>-?\d+)/undecided/$',
        UserDogUndecidedView.as_view(),
        name='dog-undecided'),
    url(r'^api/dog/(?P<pk>-?\d+)/undecided/next/$',
        UserDogUndecidedNextView.as_view(),
        name='dog-undecided-next'),
    url(r'^api/user/preferences/$', ListCreateUpdateUserPref.as_view(),
        name='userpref-detail'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html'))
])
