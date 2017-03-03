# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import NoReverseMatch
from django.utils import six
from rest_framework import serializers
from rest_framework.reverse import reverse


class CustomHyperlinkedIdentityField(serializers.RelatedField):
    """
    Customization to serializers.RelatedField
    """

    def __init__(self, url_source=None, **kwargs):
        kwargs['read_only'] = True
        kwargs['source'] = '*'
        self.url_source = url_source or 'get_complete_url'
        self.format = kwargs.pop('format', None)
        self.reverse = reverse

        super(CustomHyperlinkedIdentityField, self).__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def get_url(self, obj, request, format):
        if hasattr(obj, 'pk') and obj.pk is None:
            return None

        return getattr(obj, self.url_source)(request=request, format=format)

    def to_representation(self, value):
        request = self.context.get('request', None)
        format = self.context.get('format', None)

        assert request is not None, (
            "`%s` requires the request in the serializer"
            " context. Add `context={'request': request}` when instantiating "
            "the serializer." % self.__class__.__name__
        )

        # By default use whatever format is given for the current context
        # unless the target is a different type to the source.
        #
        # Eg. Consider a HyperlinkedIdentityField pointing from a json
        # representation to an html property of that representation...
        #
        # '/snippets/1/' should link to '/snippets/1/highlight/'
        # ...but...
        # '/snippets/1/.json' should link to '/snippets/1/highlight/.html'
        if format and self.format and self.format != format:
            format = self.format

        # Return the hyperlink, or error if incorrectly configured.
        try:
            url = self.get_url(value, request, format)
        except NoReverseMatch:
            msg = (
                'Could not resolve URL for hyperlinked identity using '
                'get_complete_url method. '
            )
            if value in ('', None):
                value_string = {'': 'the empty string', None: 'None'}[value]
                msg += (
                    " WARNING: The value of the field on the model instance "
                    "was %s, which may be why it didn't match any "
                    "entries in your URL conf." % value_string
                )
            raise ImproperlyConfigured(msg)

        if url is None:
            return None

        return serializers.Hyperlink(url, six.text_type(value))


class UUIDRelatedField(serializers.SlugRelatedField):

    """Returns a string representation of a UUID instance, where the relation is on a `uuid` field.
    This is required do to the way the UUIDField we depend on implements
    its to_python method.
    """

    def __init__(self, *args, **kwargs):
        super(UUIDRelatedField, self).__init__(*args, slug_field='uuid', **kwargs)

    def to_native(self, obj):
        return str(getattr(obj, self.slug_field))


class UUIDPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    """Returns a string representation of a UUID instance, where the `pk` is a UUID.
    This is required do to the way the UUIDField we depend on implements
    its to_python method.
    """

    def to_native(self, pk):
        if not pk:
            return None
        return str(pk)
