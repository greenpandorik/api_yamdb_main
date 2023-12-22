from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from user_auth.serializers import SignUpSerializer, TokenSerializer
from users.models import User


class APISignup(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not User.objects.filter(
            username=request.data['username'],
            email=request.data['email']
        ).exists():
            serializer.save()
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


class APIToken(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=request.data['username'])
        token = AccessToken.for_user(user)
        response = {'token': str(token)}
        return Response(response, status=status.HTTP_200_OK)
