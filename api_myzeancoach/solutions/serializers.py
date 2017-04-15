# -*- coding: utf-8 -*-
from models import Dilemma,CommentDilemma,CommentDilemmaCoach,ProCommentDilemma,ConCommentDilemma
from rest_framework import serializers

class ProCommentDilemmaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProCommentDilemma
        fields = (
            'pro_dilemma','description'
        )

class ConCommentDilemmaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConCommentDilemma
        fields = (
            'con_dilemma','description'
        )

class CommentDilemmaCoachSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentDilemmaCoach
        fields = (
            'date', 'description'
        )

class CommentDilemmaSerializer(serializers.ModelSerializer):

    pro_dilemmas = ProCommentDilemmaSerializer(many=True, read_only=True)
    con_dilemmas = ConCommentDilemmaSerializer(many=True, read_only=True)

    class Meta:
        model = CommentDilemma
        fields = (
            'nick_user', 'date', 'description', 'like', 'feedback', 'date_feedback',
            'pro_dilemmas', 'con_dilemmas'
        )

class DilemmaSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )

    dilemmas = CommentDilemmaSerializer(many=True, read_only=True)
    dilemmas_coach = CommentDilemmaCoachSerializer(many=True, read_only=True)

    class Meta:
        model = Dilemma
        fields = (
            'user', 'date', 'title', 'description', 'nick_user', 'type', 'state', 'dilemmas',
            'dilemmas_coach'
        )