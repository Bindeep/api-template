from django.urls import path
from rest_framework import routers

from apps.users.api.v1.views import (
    UserViewSet,
    CustomTokenViewBase)

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='user')


urlpatterns = [
    path('get-token/', CustomTokenViewBase.as_view(), name='token_obtain'),
]

urlpatterns += router.urls
