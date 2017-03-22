# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from serializers import RemindersSerializer,RewardsSerializer, StressDetectionQuestionsSerializer,CoachFollowUpSerializer
from models import Reminders,Rewards,StressDetectionQuestions,StressDetectionAnswers,CoachFollowUp
from users.permissions import IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly
from django.contrib.auth.models import User

class RemindersViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly)
    lookup_value_regex = '[^/]+'
    queryset = Reminders.objects.all()
    serializer_class = RemindersSerializer

    def get_queryset(self):
        queryset = super(RemindersViewSet, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def create(self, request, *args, **kwargs):
        #Get body data form request
        data = request.data
        if data:
            #ALL USERS
            if data.get("type",False) in "all":
                users = User.objects.all()
                if users:
                    for user in users:
                        validate_data = {
                            'user': user,
                            'title': data.get("title",False),
                            'subtitle': data.get("subtitle",False),
                            'description': data.get("description",False),
                            'is_personal': data.get("is_personal",False),
                            'date': data.get("date",False),
                            'time': data.get("time",False),
                            'is_finished': False,
                            'is_observations_enabled': data.get("is_observations_enabled",False),
                            'observations': "",
                            'frequency': data.get("frequency",False)
                        }
                        reminder = Reminders.objects.create(**validate_data)

            else:
                #INDIVIDUAL USER
                user = User.objects.get(username=data.get("user",False))
                if user:
                    validate_data = {
                        'user': user,
                        'title': data.get("title", False),
                        'description': data.get("description", False),
                        'is_personal': data.get("is_personal", False),
                        'date': data.get("date", False),
                        'time': data.get("time", False),
                        'is_finished': False,
                        'is_observations_enabled': data.get("is_observations_enabled", False),
                        'observations': "",
                        'frequency': data.get("frequency", False)
                    }
                    reminder = Reminders.objects.create(**validate_data)

            if reminder:
                serializer = RemindersSerializer(reminder, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='updateReminder')
    def update_reminder(self, request, **kwargs):
        data = request.data
        if data:
            try:
                reminder = Reminders.objects.get(user_id=request.user.id,
                                             title=data.get("title", False))
                if reminder:
                    reminder.is_finished = data.get("is_finished",False)
                    reminder.save()
                    return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)


    @detail_route(methods=['post'], url_path='addObservation')
    def add_observation(self, request, **kwargs):
        data = request.data
        if data:
            try:
                reminder = Reminders.objects.get(user_id=request.user.id,
                                                 title=data.get("title", False))
                if reminder:
                    if reminder.is_observations_enabled:
                        reminder.observations = data.get("observations", False)
                        reminder.save()
                        return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='setObservation')
    def set_observation(self, request, **kwargs):
        data = request.data
        if data:
            try:
                reminders = Reminders.objects.filter(title=data.get("title", False))
                if reminders:
                    for reminder in reminders:
                        reminder.is_observations_enabled = data.get("is_observations_enabled", False)
                        reminder.save()
                    return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)


class RewardsViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly)
    lookup_value_regex = '[^/]+'
    queryset = Rewards.objects.all()
    serializer_class = RewardsSerializer

    def get_queryset(self):
        queryset = super(RewardsViewSet, self).get_queryset()
        return queryset

    def create(self, request, *args, **kwargs):
        #Get body data form request
        data = request.data
        if data:
            reminder = Reminders.objects.get(user_id=request.user.id,
                                             title=data.get("title", False))
            if reminder:
                validate_data = {
                    'reminder': reminder,
                    'points': data.get("points",False)
                }
                reward = Rewards.objects.create(**validate_data)

            if reward:
                serializer = RewardsSerializer(reward, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)



class StressDetectionQuestionsViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly)
    lookup_value_regex = '[^/]+'
    queryset = StressDetectionQuestions.objects.all()
    serializer_class = StressDetectionQuestionsSerializer

    def get_queryset(self):
        queryset = super(StressDetectionQuestionsViewSet, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def create(self, request, *args, **kwargs):
        #Get body data form request
        data = request.data
        if data:
            users = User.objects.all()
            if users:
                for user in users:
                    #Create Question
                    validate_data = {
                        'user': user,
                        'description': data.get("description",False),
                        'possible_answers': data.get("possible_answers",False),
                        'is_personal_question': data.get("is_personal_question",False),
                        'active': True,
                        'user_answer': ""
                    }
                    question = StressDetectionQuestions.objects.create(**validate_data)

                    if question:
                        #Create answers
                        if data.get("answers",False):
                            for answer in data.get("answers"):
                                validate_data = {
                                    'question': question,
                                    'description': answer.get("description",False),
                                    'color': answer.get("color",False),
                                    'popup_message': answer.get("popup_message",False)
                                }
                                answer_obj = StressDetectionAnswers.objects.create(**validate_data)


                serializer = StressDetectionQuestionsSerializer(question, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='registerAnswerUser')
    def register_answer_user(self, request, **kwargs):
        data = request.data
        if data:
            try:
                question = StressDetectionQuestions.objects.get(user_id=request.user.id,
                                                                description = data.get("description",False))
                if question:
                    question.user_answer = data.get("user_answer", False)
                    question.save()
                    return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CoachFollowUpViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly)
    lookup_value_regex = '[^/]+'
    queryset = CoachFollowUp.objects.all()
    serializer_class = CoachFollowUpSerializer

    def get_queryset(self):
        queryset = super(CoachFollowUpViewSet, self).get_queryset()
        queryset = queryset.filter(active=True).order_by('?')[:1]
        return queryset

    def create(self, request, *args, **kwargs):
        #Get body data form request
        data = request.data
        if data:
            validate_data = {
                'description': data.get("description"),
                'active': True
            }
            follow = CoachFollowUp.objects.create(**validate_data)

            if follow:
                serializer = CoachFollowUpSerializer(follow, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)