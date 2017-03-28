# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from serializers import DilemmaSerializer,CommentDilemmaSerializer,CommentDilemmaCoachSerializer,ProCommentDilemmaSerializer,ConCommentDilemmaSerializer
from models import Dilemma,CommentDilemma,CommentDilemmaCoach,ProCommentDilemma,ConCommentDilemma
from users.permissions import IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly
from django.contrib.auth.models import User

class DilemmaViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly)
    lookup_value_regex = '[^/]+'
    queryset = Dilemma.objects.all()
    serializer_class = DilemmaSerializer

    def get_queryset(self):
        queryset = super(DilemmaViewSet, self).get_queryset()
        return queryset

    def create(self, request, *args, **kwargs):
        #Get body data form request
        data = request.data
        if data:
            user = User.objects.get(username=data.get("username",False))
            if user:
                validate_data = {
                    'user': user,
                    'date': data.get("date", False),
                    'title': data.get("title", False),
                    'description': data.get("description", False),
                    'nick_user': data.get("username",False),
                    'type': data.get("type", False),
                    'state': data.get("state", False)
                }
                dilemma = Dilemma.objects.create(**validate_data)

            if dilemma:
                serializer = DilemmaSerializer(dilemma, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='getDilemmas')
    def get_dilemmas(self, request, **kwargs):
        data = request.data
        if data:
            try:
                dilemmas = Dilemma.objects.filter(state=data.get("state",False))
                res = []
                if dilemmas:
                    for dilemma in dilemmas:
                        serializer = DilemmaSerializer(dilemma, context={'request': request})
                        dilemma_data = serializer.data

                        #Comments from users
                        comments_data = []
                        comments = CommentDilemma.objects.filter(dilemma=dilemma)
                        if comments:
                            for comment in comments:
                                comment_serializer = CommentDilemmaSerializer(comment,context={'request': request})
                                comments_data.append(comment_serializer.data)

                        # Comments from coach
                        comments_coach_data = []
                        comments_coach = CommentDilemmaCoach.objects.filter(dilemma_coach=dilemma)
                        if comments_coach:
                            for comment in comments_coach:
                                comment_coach_serializer = CommentDilemmaCoachSerializer(comment,context={'request': request})
                                comments_coach_data.append(comment_coach_serializer.data)

                        dilemma_data["comments"] = comments_data
                        dilemma_data["comments_coach"] = comments_coach_data
                        res.append(dilemma_data)
                    return Response({"results": res}, status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='changeDilemma')
    def change_dilemma(self, request, **kwargs):
        data = request.data
        if data:
            try:
                user = User.objects.get(username=data.get("username", False))
                if user and data.get("coach",False):
                    dilemma = Dilemma.objects.get(title=data.get("title", False), user=user)
                    if dilemma:
                        dilemma.state = data.get("state",False)
                        dilemma.save()

                        validate_data = {
                            "dilemma_coach": dilemma,
                            "date": data["coach"]["date"],
                            "description": data["coach"]["description"]
                        }

                        comment_dilema_coach = CommentDilemmaCoach.objects.create(**validate_data)
                        return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='getCoachSuggestion')
    def get_coach_suggestion(self, request, **kwargs):
        data = request.data
        if data:
            try:
                user = User.objects.get(username=data.get("username", False))
                if user:
                    dilemma = Dilemma.objects.get(title=data.get("title", False), user=user)
                    if dilemma:
                        coach_suggestions = CommentDilemmaCoach.objects.filter(dilemma_coach=dilemma)
                        if coach_suggestions:
                            res = []
                            for suggestion in coach_suggestions:
                                serializer = CommentDilemmaCoachSerializer(suggestion,context={'request': request})
                                res.append(serializer.data)

                            return Response({'results': res},status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='changeDilemmaWithSuggestion')
    def change_dilemma_with_suggestion(self, request, **kwargs):
        data = request.data
        if data:
            try:
                user = User.objects.get(username=data.get("username", False))
                if user:
                    dilemma = Dilemma.objects.get(title=data.get("title", False), user=user)
                    if dilemma:
                        dilemma.date = data.get("date",False)
                        dilemma.title = data.get("new_title",False)
                        dilemma.description = data.get("description",False)
                        dilemma.state = data.get("state",False)
                        dilemma.save()

                        return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='updateDilemma')
    def update_dilemma(self, request, **kwargs):
        data = request.data
        if data:
            try:
                user = User.objects.get(username=data.get("username", False))
                if user:
                    dilemma = Dilemma.objects.get(title=data.get("title", False), user=user)
                    if dilemma:
                        dilemma.state = data.get("state", False)
                        dilemma.save()

                        return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='addCommentDilemma')
    def add_comment_dilemma(self, request, **kwargs):
        data = request.data
        if data:
            try:
                user = User.objects.get(username=data.get("username", False))
                if user and data.get("comment",False):
                    dilemma = Dilemma.objects.get(title=data.get("title", False), user=user)
                    if dilemma:
                        validate_data = {
                            "dilemma": dilemma,
                            "nick_user": data["comment"]["nick_user"],
                            "date": data["comment"]["date"],
                            "description": data["comment"]["description"],
                            "like": data["comment"]["like"],
                            "feedback": "",
                            "date_feedback": ""
                        }

                        comment_dilema = CommentDilemma.objects.create(**validate_data)
                        return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='addFeedbackDilemma')
    def add_feedback_dilemma(self, request, **kwargs):
        data = request.data
        if data:
            try:
                user = User.objects.get(username=data.get("username", False))
                if user and data.get("comment", False):
                    dilemma = Dilemma.objects.get(title=data.get("title", False), user=user)
                    if dilemma:
                        comment = CommentDilemma.objects.get(dilemma =dilemma,
                                                             description=data.get("description",False))
                        if comment:
                            comment.feedback = data["comment"]["feedback"]
                            comment.date_feedback = data["comment"]["date_feedback"]
                            comment.save()

                        return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='addProsCommentDilemma')
    def add_pros_comment_dilemma(self, request, **kwargs):
        data = request.data
        if data:
            try:
                if data.get("pro",False):
                    comment_dilemma = CommentDilemma.objects.get(nick_user=data.get("nick_user", False),
                                                                 description=data.get("description",False))
                    if comment_dilemma:
                        validate_data = {
                            "pro_dilemma": comment_dilemma,
                            "description": data["pro"]["description"]
                        }

                        pro_comment_dilema = ProCommentDilemma.objects.create(**validate_data)
                        return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='addConsCommentDilemma')
    def add_cons_comment_dilemma(self, request, **kwargs):
        data = request.data
        if data:
            try:
                if data.get("con", False):
                    comment_dilemma = CommentDilemma.objects.get(nick_user=data.get("nick_user", False),
                                                                 description=data.get("description", False))
                    if comment_dilemma:
                        validate_data = {
                            "con_dilemma": comment_dilemma,
                            "description": data["con"]["description"]
                        }

                        cons_comment_dilema = ConCommentDilemma.objects.create(**validate_data)
                        return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        #Delete dilemma
        data = request.data
        if data:
            user = User.objects.get(username=data.get("username",False))
            if user:
                dilemma = Dilemma.objects.get(user=user,
                                              title=data.get("title", False))
                if dilemma:
                    dilemma.delete()

                    return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='getAllTypeDilemmas')
    def get_all_type_dilemmas(self, request, **kwargs):
        data = request.data
        if data:
            try:
                dilemmas = Dilemma.objects.all()
                res = []
                if dilemmas:
                    for dilemma in dilemmas:
                        serializer = DilemmaSerializer(dilemma, context={'request': request})
                        dilemma_data = serializer.data

                        add_dilemma = True
                        #Get all dilemmas except form other users with state refused
                        if dilemma_data["nick_user"] != data.get("username",False):
                            if dilemma_data["state"] == "refused":
                                add_dilemma = False

                        # Comments from users
                        comments_data = []
                        comments = CommentDilemma.objects.filter(dilemma=dilemma)
                        if comments:
                            for comment in comments:
                                comment_serializer = CommentDilemmaSerializer(comment, context={'request': request})
                                comments_data.append(comment_serializer.data)

                        # Comments from coach
                        comments_coach_data = []
                        comments_coach = CommentDilemmaCoach.objects.filter(dilemma_coach=dilemma)
                        if comments_coach:
                            for comment in comments_coach:
                                comment_coach_serializer = CommentDilemmaCoachSerializer(comment,
                                                                                         context={'request': request})
                                comments_coach_data.append(comment_coach_serializer.data)

                        dilemma_data["comments"] = comments_data
                        dilemma_data["comments_coach"] = comments_coach_data

                        if add_dilemma:
                            res.append(dilemma_data)
                    return Response({"results": res}, status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)