# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from serializers import VideosSerializer
from models import Videos
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
                        "date": data.get("date",False)
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