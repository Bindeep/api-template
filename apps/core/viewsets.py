from rest_framework.mixins import (
    RetrieveModelMixin, ListModelMixin,
    UpdateModelMixin, CreateModelMixin,
    DestroyModelMixin
)

from rest_framework.viewsets import GenericViewSet


class BaseViewSet(GenericViewSet):
    """"
    :cvar serializer_include_fields:
        fields to include in serializer

        type -->  iterable

        set this value or override get_serializer_include_fields

    :cvar serializer_exclude_fields:
        fields to exclude in serializer

        type -->  iterable

        set this value or override get_serializer_exclude_fields

    """
    serializer_include_fields = None
    serializer_exclude_fields = None
    permission_class_mapper = {}

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        return [permission() for permission in self.get_permission_classes()]

    def get_permission_classes(self):
        if not self.permission_class_mapper:
            return self.permission_classes
        else:
            return self.permission_class_mapper.get(self.action, self.permission_classes)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()

        kwargs['fields'] = self.get_serializer_include_fields()
        kwargs['exclude_fields'] = self.get_serializer_exclude_fields()
        return serializer_class(*args, **kwargs)

    def get_serializer_include_fields(self):
        return self.serializer_include_fields

    def get_serializer_exclude_fields(self):
        return self.serializer_exclude_fields


class ListViewSet(ListModelMixin, BaseViewSet):
    pass


class CreateViewSet(CreateModelMixin, BaseViewSet):
    pass


class RetrieveViewSet(RetrieveModelMixin, BaseViewSet):
    pass


class UpdateViewSet(UpdateModelMixin, BaseViewSet):
    pass


class DestroyViewSet(DestroyModelMixin, BaseViewSet):
    pass


class ReadOnlyViewSet(ListViewSet, RetrieveViewSet):
    pass


class CreateRetrieveViewSet(CreateViewSet, RetrieveViewSet):
    pass


class ListUpdateViewSet(ListViewSet, UpdateViewSet):
    pass


class RetrieveUpdateViewSet(UpdateViewSet, RetrieveViewSet):
    pass


class ListRetrieveUpdateViewSet(ListViewSet,
                                RetrieveViewSet, UpdateViewSet):
    pass


class CreateListViewSet(CreateViewSet, ListViewSet):
    pass


class CreateUpdateViewSet(CreateViewSet, UpdateViewSet):
    pass


class CreateRetrieveUpdateViewSet(CreateViewSet,
                                  RetrieveViewSet, UpdateViewSet):
    pass


class CreateListRetrieveUpdateViewSet(CreateViewSet,
                                      ListViewSet,
                                      RetrieveViewSet,
                                      UpdateViewSet):
    pass


class CreateListUpdateViewSet(CreateViewSet, UpdateViewSet, ListViewSet):
    pass


class CreateListUpdateDestroyViewSet(CreateViewSet, ListViewSet, UpdateViewSet, DestroyViewSet):
    pass


class CreateListDestroyViewSet(CreateViewSet,
                               ListViewSet, DestroyViewSet):
    pass


class ListRetrieveUpdateDestroyViewSet(ListViewSet, RetrieveUpdateViewSet, DestroyViewSet):
    pass


class CustomModelViewSet(CreateViewSet,
                         ListViewSet,
                         RetrieveUpdateViewSet,
                         DestroyViewSet):
    pass
