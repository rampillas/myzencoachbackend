# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include,url
from common import routers
from . import views

router = routers.SimpleRouter()
router.register(r'videos', views.VideosViewSet)
router.register(r'survey', views.SurveyViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)