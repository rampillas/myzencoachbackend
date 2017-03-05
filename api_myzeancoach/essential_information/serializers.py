# -*- coding: utf-8 -*-
from models import Videos, Survey, Question, Answer
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
            'user', 'name', 'url', 'new_attr', 'is_watched', 'date', 'photo_url'
        )

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.get('context').pop('owner', kwargs.get('context')['request'].user)
        super(VideosSerializer, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = Videos.objects.filter(user=self.owner)

    def save(self, **kwargs):
        kwargs.update({'user': self.owner})
        return super(VideosSerializer, self).save(**kwargs)

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = (
            'description','is_right'
        )

class QuestionSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'description', 'is_completed', 'answers'
        )

class SurveySerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )

    questions = QuestionSerializer(many=True,read_only=True)

    class Meta:
        model = Survey
        fields = (
            'user', 'description', 'score', 'is_completed','questions'
        )
