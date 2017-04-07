# -*- coding: utf-8 -*-
from models import Events, CommentEvent, Interests, UserEventLike
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

class UserEventLikeSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )

    events_likes = EventsSerializer(many=True, read_only=True)

    class Meta:
        model = UserEventLike
        fields = (
            'user', 'events_likes', 'is_liked'
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