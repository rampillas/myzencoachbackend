# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from serializers import WellnessPlanSerializer
from models import WellnessPlan, Exercise, QuestionExercise
from users.permissions import IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly
from django.contrib.auth.models import User

class WellnessPlanViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly)
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'
    queryset = WellnessPlan.objects.all()
    serializer_class = WellnessPlanSerializer

    def get_queryset(self):
        queryset = super(WellnessPlanViewSet, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
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
                        "date": data.get("date",False),
                        "description": data.get("description",False)
                    }
                    #Create WellnessPlan
                    plan = WellnessPlan.objects.create(**validate_data)
                    if plan:
                        #Create Exercise
                        if data.get("exercises",False):
                            for exercise in data.get("exercises"):
                                validate_data = {
                                    "plans": plan,
                                    "week": exercise.get("week",False),
                                    "description": exercise.get("description",False),
                                    "audio_url": exercise.get("audio_url", False),
                                    "instructions": exercise.get("instructions", False),
                                    "feedback": ""
                                }
                                exercise_object = Exercise.objects.create(**validate_data)
                                #Create Questions Exercises
                                if exercise_object and "questions" in exercise:
                                    for question in exercise["questions"]:
                                        validate_data = {
                                            "exercises": exercise_object,
                                            "question": question.get("question"),
                                            "answer": False,
                                            "is_answered": False
                                        }
                                        question_object = QuestionExercise.objects.create(**validate_data)

                serializer = WellnessPlanSerializer(plan,context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        #Update survey for user
        data = request.data
        if data:
            plan = WellnessPlan.objects.get(user_id=request.user.id, description=data.get("description_plan", False))
            if plan:
                if data.get("exercises",False):
                    for exercise in data.get("exercises"):
                        exercise_object = Exercise.objects.get(plans=plan,description=exercise["description"])
                        if exercise_object:
                            exercise_object.feedback = exercise["feedback"]
                            exercise_object.save()

                            questions = QuestionExercise.objects.filter(exercises = exercise_object)
                            if questions:
                                for q in questions:
                                    q.answer = True
                                    q.is_answered = True
                                    q.save()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)