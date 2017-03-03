# -*- coding: utf-8 -*-
from models import Videos
from rest_framework import serializers

class VideosSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )

    class Meta:
        model = Videos
        fields = (
            'user', 'name', 'url', 'new_attr', 'is_watched', 'date'
        )

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.get('context').pop('owner', kwargs.get('context')['request'].user)
        super(VideosSerializer, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = Videos.objects.filter(user=self.owner)

    def save(self, **kwargs):
        kwargs.update({'user': self.owner})
        return super(VideosSerializer, self).save(**kwargs)