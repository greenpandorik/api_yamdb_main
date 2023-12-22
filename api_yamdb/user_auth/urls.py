from django.urls import include, path
from rest_framework import routers

from user_auth.views import APISignupViewSet, APITokenViewSet

v1_router = routers.DefaultRouter()
v1_router.register('signup', APISignupViewSet, basename='signup')
v1_router.register('token', APITokenViewSet, basename='token')

urlpatterns = [
    path('', include(v1_router.urls)),
]
