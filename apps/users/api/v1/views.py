from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.core.viewsets import CreateListUpdateDestroyViewSet
from apps.users.api.v1.serializers import (
    UserDetailSerializer,
    CustomTokenObtainPairSerializer, PasswordChangeSerializer
)

USER = get_user_model()


class CustomTokenViewBase(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(CreateListUpdateDestroyViewSet):
    serializer_class = UserDetailSerializer
    queryset = USER.objects.filter(is_active=True)
    permission_class_mapper = {
        'create': []
    }
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = ['full_name', 'email', 'phone_number']
    filter_fields = ['is_staff', ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['put', ],
        serializer_class=PasswordChangeSerializer,
        permission_classes=[IsAdminUser],
        url_name='change-password',
        url_path='password_change'
    )
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get('password1')
        user.set_password(password)
        user.save()
        return Response(serializer.data)

