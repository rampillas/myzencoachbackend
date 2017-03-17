# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
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
                        "description": data.get("description",False),
                        "is_finished": False
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
                                    "feedback": "",
                                    "appreciation": ""
                                }
                                exercise_object = Exercise.objects.create(**validate_data)
                                #Create Questions Exercises
                                if exercise_object and "questions" in exercise:
                                    for question in exercise["questions"]:
                                        validate_data = {
                                            "exercises": exercise_object,
                                            "question": question.get("question"),
                                            "answer": False,
                                            "is_answered": False,
                                            "response": ""
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
                            exercise_object.appreciation = exercise["appreciation"]
                            exercise_object.save()

                        for question in exercise["questions"]:
                            question_object = QuestionExercise.objects.get(exercises = exercise_object,
                                                                           question = question["question"])
                            if question_object:
                                question_object.answer = True
                                question_object.is_answered = True
                                question_object.response = question["response"]
                                question_object.save()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='getEjercise')
    def get_ejercise(self, request, **kwargs):
        data  = request.data
        if data:
            res = {
                    "user": "",
                    "description": "",
                    "date": "",
                    "exercises": [],
                    "is_finished": False
            }
            try:
                plan = WellnessPlan.objects.get(user_id = request.user.id,
                                                is_finished = False,
                                                description = data.get("description_plan",False))
                if plan:
                    serializer = WellnessPlanSerializer(plan,context={'request': request})
                    if serializer.data:

                        res["user"] = serializer.data["user"]
                        res["description"] = serializer.data["description"]
                        res["date"] = serializer.data["date"]
                        res["is_finished"] = serializer.data["is_finished"]

                        for item in serializer.data["exercises"]:
                            if item["week"] == int(data.get('week',False)):
                                res["exercises"].append({
                                      "week": item["week"],
                                      "description": item["description"],
                                      "audio_url": item["audio_url"],
                                      "instructions": item["instructions"],
                                      "feedback": item["feedback"],
                                      "appreciation": item["appreciation"],
                                      "question_exercises": item["question_exercises"]
                                    })
                    return Response(res, status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='finishPlan')
    def finish_plan(self, request, **kwargs):
        data = request.data
        if data:
            try:
                plan = WellnessPlan.objects.get(user_id=request.user.id,
                                                description=data.get("description_plan", False))
                if plan:
                    plan.is_finished = True
                    plan.save()
                    return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        #Delete a plan
        data = request.data
        if data:
            plans = WellnessPlan.objects.filter(description=data.get("description", False))
            if plans:
                for plan in plans:
                    plan.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)