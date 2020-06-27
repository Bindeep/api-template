from django.utils.functional import cached_property
from rest_framework.serializers import ModelSerializer, Serializer


class DynamicFieldsSerializer(Serializer):
    """
    A Serializer that takes an additional `fields` and 'exclude_fields'
    argument that controls which fields should be displayed and not to be
    displayed.
    """

    def __init__(self, instance=None, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)

        # Instantiate the superclass normally
        super().__init__(
            instance, *args, **kwargs
        )

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        # exclude fields
        if exclude_fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            exclude_fields = set(exclude_fields)
            for field_name in exclude_fields:
                self.fields.pop(field_name)

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        create_only_fields = getattr(self.Meta, 'create_only_fields', None)

        if self.instance and create_only_fields:
            for field_name in create_only_fields:
                kwargs = extra_kwargs.get(field_name, {})
                kwargs['read_only'] = True
                extra_kwargs[field_name] = kwargs

        return extra_kwargs

    @cached_property
    def request(self):
        return self.context.get("request")

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class DynamicFieldsModelSerializer(ModelSerializer, DynamicFieldsSerializer):
    """
    A ModelSerializer that takes an additional `fields` and 'exclude_fields'
    argument that controls which fields should be displayed and not to be
    displayed.
    """
    pass


class DummyObject:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class DummySerializer(DynamicFieldsSerializer):
    """
    Read only serializer for non model serializers
    Overrides create and update but does nothing in that
    """

    def create(self, validated_data):
        return DummyObject(**validated_data)

    def update(self, instance, validated_data):
        return instance
