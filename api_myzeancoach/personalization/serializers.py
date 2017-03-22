# -*- coding: utf-8 -*-
from models import Reminders,Rewards,StressDetectionQuestions,StressDetectionAnswers,CoachFollowUp
from rest_framework import serializers

class RemindersSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )

    class Meta:
        model = Reminders
        fields = (
            'user', 'title', 'subtitle', 'description', 'is_personal', 'date', 'time', 'is_finished',
            'is_observations_enabled', 'observations', 'frequency'
        )

class RewardsSerializer(serializers.ModelSerializer):

    reminders = RemindersSerializer(many=True, read_only=True)

    class Meta:
        model = Rewards
        fields = (
            'reminders', 'points'
        )


class StressDetectionAnswersSerializer(serializers.ModelSerializer):

    class Meta:
        model = StressDetectionAnswers
        fields = (
            'description', 'color', 'popup_message'
        )

class StressDetectionQuestionsSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )

    questions = StressDetectionAnswersSerializer(many=True, read_only=True)

    class Meta:
        model = StressDetectionQuestions
        fields = (
            'user', 'description', 'possible_answers', 'is_personal_question', 'active', 'user_answer',
            'questions'
        )

class CoachFollowUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoachFollowUp
        fields = (
            'description', 'active'
        )