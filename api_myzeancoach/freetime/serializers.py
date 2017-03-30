# -*- coding: utf-8 -*-
from models import Events, CommentEvent, Interests
from rest_framework import serializers

class EventsSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )

    class Meta:
        model = Events
        fields = (
            'user', 'date', 'title', 'description', 'likes', 'category'
        )

class CommentEventSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )

    events = EventsSerializer(many=True, read_only=True)

    class Meta:
        model = CommentEvent
        fields = (
            'user', 'events', 'date', 'description'
        )

class InterestsSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )

    class Meta:
        model = Interests
        fields = (
            'user', 'name'
        )