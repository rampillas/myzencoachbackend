# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include,url
from common import routers
from . import views

router = routers.SimpleRouter()
router.register(r'dilemmas', views.DilemmaViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)