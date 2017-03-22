# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include,url
from common import routers
from . import views

router = routers.SimpleRouter()
router.register(r'reminders', views.RemindersViewSet)
router.register(r'rewards', views.RewardsViewSet)
router.register(r'stress', views.StressDetectionQuestionsViewSet)
router.register(r'followup', views.CoachFollowUpViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)