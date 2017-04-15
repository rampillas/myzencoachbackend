# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from serializers import EventsSerializer, CommentEventSerializer, InterestsSerializer, UserEventLikeSerializer
from models import Events, CommentEvent, Interests, UserEventLike
from users.permissions import IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly
from django.contrib.auth.models import User

class EventsViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly)
    lookup_value_regex = '[^/]+'
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

    def get_queryset(self):
        queryset = super(EventsViewSet, self).get_queryset()
        return queryset

    def create(self, request, *args, **kwargs):
        #Get body data form request
        data = request.data
        if data:
            user = User.objects.get(pk=request.user.id)
            if user:
                validate_data = {
                    'user': user,
                    'date': data.get("date", False),
                    'title': data.get("title", False),
                    'description': data.get("description", False),
                    'likes': 0,
                    'category': data.get("category", False)
                }
                event = Events.objects.create(**validate_data)

            if event:
                serializer = EventsSerializer(event, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='getEvents')
    def get_events(self, request, **kwargs):
        try:
            res = []
            #Get interests from User
            interests = Interests.objects.filter(user_id=request.user.id)
            if interests:
                array_interests = []
                for interest in interests:
                    array_interests.append(interest.name)

            #Get all events
            events = Events.objects.all()
            if events:
                user = User.objects.get(pk=request.user.id)
                for event in events:
                    event_serializer = EventsSerializer(event, context={'request': request})
                    event_data = event_serializer.data
                    #Get comments from Event
                    comments = CommentEvent.objects.filter(event=event)
                    comments_data = []
                    if comments:
                        for comment in comments:
                            comment_serializer = CommentEventSerializer(comment, context={'request': request})
                            comments_data.append(comment_serializer.data)

                    if user:
                        event_data["user_like"] = {
                                        'user': user.username,
                                        'event': event.title,
                                        'is_liked': False
                                    }
                        user_like = UserEventLike.objects.filter(event=event,user=user)
                        if user_like:
                            for ul in user_like:
                                user_like_serializer = UserEventLikeSerializer(ul, context={'request': request})

                            event_data["user_like"] = user_like_serializer.data

                    event_data["comments"] = comments_data

                    if interests:
                        if event.category in array_interests:
                            res.append(event_data)
                    else:
                        res.append(event_data)

            return Response({"results": res},status=status.HTTP_200_OK)

        except Exception as e:
            pass

        return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        #Delete Event
        data = request.data
        if data:
            user = User.objects.get(pk=request.user.id)
            if user:
                event = Events.objects.get(title=data.get("title", False), user=user)
                if event:
                    event.delete()

                    return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    @detail_route(methods=['post'], url_path='addLikeToEvent')
    def add_like_to_event(self, request, **kwargs):
        data = request.data
        if data:
            try:
                user_owner = User.objects.get(username=data.get("user_owner", False))
                if user_owner:
                    event = Events.objects.get(title=data.get("title", False), user=user_owner)
                    if event:
                        user = User.objects.get(pk=request.user.id)
                        if user:
                            validated_data = {
                                    'user': user,
                                    'event': event,
                                    'is_liked': True
                            }

                            user_like = UserEventLike.objects.create(**validated_data)

                            likes = event.likes
                            event.likes = likes + 1
                            event.save()

                            serializer = EventsSerializer(event, context={'request': request})

                            return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='quitLikeToEvent')
    def quit_like_to_event(self, request, **kwargs):
        data = request.data
        if data:
            try:
                user_owner = User.objects.get(username=data.get("user_owner", False))
                if user_owner:
                    event = Events.objects.get(title=data.get("title", False), user=user_owner)
                    if event:
                        user = User.objects.get(pk=request.user.id)
                        if user:
                            user_like = UserEventLike.objects.get(user=user, event=event)
                            if user_like:
                                user_like.delete()

                                likes = event.likes
                                event.likes = likes - 1
                                event.save()

                            serializer = EventsSerializer(event, context={'request': request})

                            return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='addCommentToEvent')
    def add_comment_to_event(self, request, **kwargs):
        data = request.data
        if data:
            try:
                user = User.objects.get(username=data.get("user_owner", False))
                if user:
                    event = Events.objects.get(title=data.get("title", False), user=user)
                    if event:
                        validate_data = {
                            'user': user,
                            'event': event,
                            'date': data.get("date", False),
                            'description': data.get("description", False)
                        }
                        comment = CommentEvent.objects.create(**validate_data)

                        return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='addInterestsUser')
    def add_interests_user(self, request, **kwargs):
        data = request.data
        if data:
            try:
                user = User.objects.get(pk=request.user.id)
                if user and data.get("interests",False):
                    interests = Interests.objects.filter(user=user)
                    if interests:
                        for interest in interests:
                            interest.delete()

                    for interest in data.get("interests"):
                        validate_data = {
                            'user': user,
                            'name': interest["name"]
                        }
                        interest_user = Interests.objects.create(**validate_data)

                    return Response(status=status.HTTP_200_OK)
            except Exception as e:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='getInterestsUser')
    def get_interests_user(self, request, **kwargs):
        try:
            user = User.objects.get(pk=request.user.id)
            if user:
                interests = Interests.objects.filter(user=user)
                res = []
                if interests:
                    for interest in interests:
                        serializer = InterestsSerializer(interest, context={'request': request})
                        res.append(serializer.data)

                return Response({'results': res},status=status.HTTP_200_OK)
        except Exception as e:
            pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='deleteInterestsUser')
    def delete_interests_user(self, request, **kwargs):
        try:
            user = User.objects.get(pk=request.user.id)
            if user:
                interests = Interests.objects.filter(user=user)
                res = []
                if interests:
                    for interest in interests:
                        interest.delete()

                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            pass

        return Response(status=status.HTTP_400_BAD_REQUEST)