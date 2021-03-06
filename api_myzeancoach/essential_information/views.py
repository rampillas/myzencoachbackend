# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from serializers import VideosSerializer, SurveySerializer
from models import Videos, Survey, Question, Answer
from users.permissions import IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly
from django.contrib.auth.models import User

class VideosViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly)
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer

    def get_queryset(self):
        queryset = super(VideosViewSet, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id).order_by('-date')
        return queryset

    def create(self, request, *args, **kwargs):
        #Get body data form request
        data = request.data
        if data:
            users = User.objects.all()
            if users:
                for user in users:
                    validate_data = {
                        "user": user,
                        "name": data.get("name",False),
                        "url": data.get("url",False),
                        "new_attr": data.get("new_attr",False),
                        "is_watched": data.get("is_watched",False),
                        "date": data.get("date",False),
                        'photo_url': data.get("photo_url",False)
                    }
                    #Create Video
                    video = Videos.objects.create(**validate_data)
                if video:
                    serializer = VideosSerializer(video,context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        #Update user video to seen
        data = request.data
        if data:
            video = Videos.objects.get(user_id=request.user.id, name=data.get("name", False))
            if video:
                video.is_watched = data.get("is_watched",False)
                video.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        #Delete a video
        data = request.data
        if data:
            videos = Videos.objects.filter(name=data.get("name", False))
            if videos:
                for video in videos:
                    video.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class SurveyViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly)
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def get_queryset(self):
        queryset = super(SurveyViewSet, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def create(self, request, *args, **kwargs):
        #Get body data form request
        data = request.data
        if data:
            users = User.objects.all()
            if users:
                for user in users:
                    video = Videos.objects.get(name=data.get("name",False),user=user)
                    if video:
                        validate_data = {
                            "user": user,
                            "video": video,
                            "description": data.get("description",False),
                            "score": data.get("score",False),
                            "is_completed": False
                        }
                        #Create Survey
                        survey = Survey.objects.create(**validate_data)
                        if survey:
                            #Create Questions
                            if data.get("questions",False):
                                for question_item in data.get("questions"):
                                    validate_data = {
                                        "survey": survey,
                                        "description": question_item.get("description",False),
                                        "is_completed": False
                                    }
                                    question = Question.objects.create(**validate_data)
                                    #Create Answer
                                    if question and "answers" in question_item:
                                        for answer in question_item["answers"]:
                                            validate_data = {
                                                "question": question,
                                                "description": answer.get("description"),
                                                "is_right": answer.get("is_right")
                                            }
                                            answer = Answer.objects.create(**validate_data)

                serializer = SurveySerializer(survey,context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        #Update survey for user
        data = request.data
        if data:
            survey = Survey.objects.get(user_id=request.user.id, description=data.get("description", False))
            if survey:
                survey.is_completed = True
                survey.score = data.get("score", False)
                survey.save()
                questions = Question.objects.filter(survey=survey)
                if questions:
                    for question in questions:
                        question.is_completed = True
                        question.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'], url_path='ranking')
    def get_ranking(self, request, **kwargs):
        try:
            query = "select 1 as id, u.username,sum(eis.score) as score from essential_information_survey eis " \
                    "inner join auth_user u on u.id =  eis.user_id " \
                    "group by u.username order by sum(eis.score) desc limit 5"
            res = []
            for r in Survey.objects.raw(query):
                res.append({"username":r.username,"score":r.score})

            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            pass

        return Response(status=status.HTTP_400_BAD_REQUEST)