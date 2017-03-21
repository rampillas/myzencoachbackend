# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from serializers import RemindersSerializer
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

