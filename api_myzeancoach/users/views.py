import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from models import update_profile,Emoticon
from rest_framework import mixins,viewsets
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from users.permissions import IsAuthenticatedOrCreateOrRecoverOnly, IsOwnerOrReadOrRecoverOnly
from users.serializers import UserSerializer
from serializers import EmoticonSerializer
from users.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
import urllib2
from django.http import HttpResponse

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

    @detail_route(methods=['put'], url_path='password')
    def set_password(self, request, **kwargs):
        """
        Endpoint for setting user's password.
        """
        user = self.get_object()

        serializer = self.get_serializer(instance=user, data=request.data)
        from django.utils.http import urlsafe_base64_decode
        # VALIDATE TOKEN
        if request.data['password'] == "" and \
                        request.data['token'] != "" and \
                        request.data['uid'] != "":
            try:
                from django.contrib.auth import get_user_model
                user_model = get_user_model()
                user = user_model.objects.get(pk=urlsafe_base64_decode(request.data['uid']))
                if default_token_generator.check_token(user, request.data['token']):
                    # token ok
                    return Response({"detail": "ok"})
                else:
                    # wrong token
                    return Response({"detail": "error"})
            except:
                return Response({"detail": "bad request"})
        else:
            # CHANGE PASSWORD
            uidb64 = request.data['uid']
            token = request.data['token']
            token_generator = default_token_generator

            if uidb64 is not None and token is not None:
                uid = urlsafe_base64_decode(uidb64)
                try:
                    from django.contrib.auth import get_user_model
                    user_model = get_user_model()
                    user = user_model.objects.get(pk=uid)

                    if default_token_generator.check_token(user, token):
                        user.set_password(request.data['password'])
                        user.save()
                        return Response({"detail": "ok"})
                    else:
                        return Response({"error": "token used"})
                except:
                    return Response({"error": "io exception"})

            else:
                return Response({"error": "token expired"})

@csrf_exempt
def recover_password(request):
    """Endpoint for requesting user's password recovery."""
    data = request.body
    if data:
        try:
            data = json.loads(data)
            user = User.objects.get(username=data.get("username",False))
            if user:
                form = PasswordResetForm({'email': user.email})
                if form.is_valid():
                    opts = {
                        'use_https': request.is_secure(),
                        'token_generator': default_token_generator,
                        'from_email': None,
                        'email_template_name': 'password_reset_email.html',
                        'subject_template_name': 'password_reset_subject.txt',
                        'request': request,
                        'html_email_template_name': None,
                    }
                    form.save(**opts)
                    return HttpResponse(json.dumps({"detail": "ok"}), status=status.HTTP_200_OK,
                                        content_type="application/json")
        except Exception as e:
            pass
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def login(request):
    """Login for Users"""
    data = request.body
    if data:
        try:
            data = json.loads(data)
            client_id = data.get("client_id", False)
            client_secret = data.get("client_secret", False)
            username = data.get("username", False)
            password = data.get("password", False)
            grant_type = data.get("grant_type", False)
            scope = data.get("scope", False)

            url = '/oauth/token/' + "?client_id=" + client_id + "&client_secret=" + \
                  client_secret + "&username=" + username + "&password=" + password + \
                  "&grant_type=" + grant_type + "&scope=" + scope

            from oauth2_provider.settings import oauth2_settings
            server = oauth2_settings.OAUTH2_SERVER_CLASS(oauth2_settings.OAUTH2_VALIDATOR_CLASS())
            headers, body, status_res = server.create_token_response(url, "POST", "",{}, None)

            res = HttpResponse(content=body, status=status_res, content_type="application/json")
            for k, v in headers.items():
                res[k] = v
            if res:
                return res
        except Exception as e:
            pass
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

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