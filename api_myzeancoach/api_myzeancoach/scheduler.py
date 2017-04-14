# -*- coding: utf-8 -*-
import os, sys
#sys.path.append("/Users/demendezr/Documents/UNIR/TRABAJO FIN DE MASTER/PROYECTOS/backend_myzeancoach/api_myzeancoach")
sys.path.append("/home/demendezr/TFM/backend_myzeancoach/api_myzeancoach")
os.environ["DJANGO_SETTINGS_MODULE"] = "api_myzeancoach.settings"

import django
django.setup()

from personalization.models import Reminders
from notifications import pushy

reminders = Reminders.objects.all()
if reminders:
    for reminder in reminders:
        if not reminder.is_finished:
            user = reminder.user
            if user:
                if user.profile.notification_token:
                    # Payload data you want to send to devices
                    data = {'message': user.username + ' ' + reminder.subtitle}
                    # The recipient device tokens
                    deviceTokens = [user.profile.notification_token]
                    # Send the push notification with Pushy
                    pushy.PushyAPI.sendPushNotification(data, deviceTokens)