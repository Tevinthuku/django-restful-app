from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "token"
        ]

    # if you want to have request in your serializer
    # make sure in the view class you have the method below

    # def get_serializer_context(self, *args, **kwargs):
    #     return {"request": self.request}

    # context = self.context
    # request = context["request"]

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "user with this email already exists")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this username already exists")
        return value

    def get_token(self, user_object):
        payload = jwt_payload_handler(user_object)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, data):
        pw = data.get("password")
        pw2 = data.get("password2")

        if pw != pw2:
            raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, vallidated_data):
        user_object = User(username=vallidated_data.get(
            "username"), email=vallidated_data.get("email"))
        user_object.set_password(vallidated_data.get("password"))
        user_object.save()
        return user_object
