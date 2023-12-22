from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from user_auth.serializers import SignUpSerializer, TokenSerializer
from users.models import User


class APISignupViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = SignUpSerializer

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(
            username=request.data['username'],
            email=request.data['email']
        )
        conformation_code = default_token_generator.make_token(user)
        send_mail(
            f'Привет, {str(user.username)}! Код подтверждения:',
            conformation_code,
            settings.EMAIL,
            [request.data['email']],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APITokenViewSet(viewsets.ModelViewSet):
    serializer_class = TokenSerializer

    @action(detail=False, methods=['post'])
    def token(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=request.data['username'])
        token = AccessToken.for_user(user)
        response = {'token': str(token)}
        return Response(response, status=status.HTTP_200_OK)
