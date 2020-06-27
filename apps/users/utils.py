from apps.users.api.v1.serializers import UserDetailSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserDetailSerializer(instance=user, context={'request': request}).data
    }
