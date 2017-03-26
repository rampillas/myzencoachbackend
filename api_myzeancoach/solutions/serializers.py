# -*- coding: utf-8 -*-
from models import Dilemma,CommentDilemma,CommentDilemmaCoach,ProCommentDilemma,ConCommentDilemma
from rest_framework import serializers

class DilemmaSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )

    class Meta:
        model = Dilemma
        fields = (
            'user', 'date', 'title', 'description', 'nick_user', 'type', 'state'
        )


class CommentDilemmaSerializer(serializers.ModelSerializer):

    dilemmas = DilemmaSerializer(many=True, read_only=True)

    class Meta:
        model = CommentDilemma
        fields = (
            'dilemmas', 'nick_user', 'date', 'description', 'like', 'feedback', 'date_feedback'
        )

class CommentDilemmaCoachSerializer(serializers.ModelSerializer):

    dilemmas_coach = DilemmaSerializer(many=True, read_only=True)

    class Meta:
        model = CommentDilemmaCoach
        fields = (
            'dilemmas_coach', 'date', 'description'
        )

class ProCommentDilemmaSerializer(serializers.ModelSerializer):

    pro_dilemmas = CommentDilemmaSerializer(many=True, read_only=True)

    class Meta:
        model = ProCommentDilemma
        fields = (
            'pro_dilemmas', 'description'
        )

class ConCommentDilemmaSerializer(serializers.ModelSerializer):

    con_dilemmas = CommentDilemmaSerializer(many=True, read_only=True)

    class Meta:
        model = ConCommentDilemma
        fields = (
            'con_dilemmas', 'description'
        )
