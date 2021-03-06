from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework import generics, permissions
from django.contrib.auth import (authenticate, get_user_model)

from .serializers import (UserRegistrationSerializer,
                          UsersListWithStatusSerializer)
from .permissions import AnonPermissionOnly

from status.models import Status
from status.api.serializers import StatusSerializers

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


User = get_user_model()


class AuthViews(APIView):
    authentication_classes = []
    permission_classes = [AnonPermissionOnly]

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        qs = User.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username)
        ).distinct()

        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(
                    token, user, request=request)
                return Response(response)
            return Response({"detail": "Incorrect password"}, status=400)
        return Response({"detail": "You are not a user"}, status=400)


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AnonPermissionOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class UserListStatusView(generics.ListAPIView):
    serializer_class = StatusSerializers

    def get_queryset(self, *args, **kwargs):
        userid = self.kwargs.get("userid", None)
        if userid is None:
            return Status.objects.none()

        return Status.objects.filter(user=userid)


class UsersListView(generics.ListAPIView):
    permission_classes = [AnonPermissionOnly]
    serializer_class = UsersListWithStatusSerializer

    def get_queryset(self, *args, **kwargs):
        return User.objects.all()
