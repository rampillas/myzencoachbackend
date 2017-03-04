# -*- coding: utf-8 -*-
from models import WellnessPlan, Exercise, QuestionExercise
from rest_framework import serializers

class QuestionExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionExercise
        fields = (
            'question', 'answer', 'is_answered'
        )

class ExerciseSerializer(serializers.ModelSerializer):

    question_exercises = QuestionExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = (
            'week', 'description', 'audio_url', 'instructions', 'feedback', 'question_exercises'
        )

class WellnessPlanSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )

    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WellnessPlan
        fields = (
            'user', 'description' , 'date', 'exercises'
        )


