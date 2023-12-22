from rest_framework import serializers

from user_auth.validators import check_token, correct_fields, validate_username

from users.models import User


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField(validators=[validate_username])

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        validators = [check_token]


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254, allow_blank=False)
    username = serializers.CharField(
        max_length=150, allow_blank=False, validators=[validate_username]
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        validators = [correct_fields]
