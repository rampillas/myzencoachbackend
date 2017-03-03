import json
from django.contrib.auth.models import User
from models import update_profile,Emoticon
from rest_framework import mixins,viewsets
from rest_framework import status
from rest_framework.response import Response
from users.permissions import IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly
from users.serializers import UserSerializer
from serializers import EmoticonSerializer

class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly)
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('username', 'email')
    search_fields = ('first_name', 'last_name', 'username')

    def get_object(self):
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if self.kwargs[lookup_url_kwarg] == 'me':
            self.kwargs[lookup_url_kwarg] = self.request.user.username

        return super(UserViewSet, self).get_object()

    def create(self, request, *args, **kwargs):
        #Get body data form request
        data = request.data
        if data:
            validate_data = {
                "username": data.get("username",False),
                "email": data.get("email",False),
                "first_name": data.get("first_name",False),
                "last_name": data.get("last_name",False),
                "password": data.get("password",False)
            }
            #Create User and Profile
            user = User.objects.create(**validate_data)
            if user:
                #Update profile
                profile = update_profile(user, data)
                user = User.objects.get(username=user)
                if user:
                    #Set user password
                    user.set_password(data.get("password",False))
                    user.save()
                    #Get user serializer
                    serializer = UserSerializer(user,context={'request': request})
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({},status=status.HTTP_400_BAD_REQUEST)


class EmoticonViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly)
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'
    queryset = Emoticon.objects.all()
    serializer_class = EmoticonSerializer

    def get_queryset(self):
        queryset = super(EmoticonViewSet, self).get_queryset()
        emoticons = Emoticon.objects.filter(user_id=self.request.user.id).order_by('-date')[:1]
        if emoticons:
            queryset = queryset.filter(pk=emoticons)
        return queryset

    def create(self, request, *args, **kwargs):
        #Get body data form request
        data = request.data
        if data:
            validate_data = {
                "user": request.user,
                "name": data.get("name",False),
                "is_positive": data.get("is_positive",False),
                "date": data.get("date",False)
            }
            #Create Emoticon
            emoticon = Emoticon.objects.create(**validate_data)
            if emoticon:
                serializer = EmoticonSerializer(emoticon,context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({},status=status.HTTP_400_BAD_REQUEST)