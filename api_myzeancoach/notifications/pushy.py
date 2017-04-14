# -*- coding: utf-8 -*-

import json
import urllib2

class PushyAPI:

    @staticmethod
    def sendPushNotification(data, tokens):
        # Insert your Pushy Secret API Key here
        apiKey = 'e551269887be1933e671e003441a62cc9409893215a7fabc028d386a03743743';

        # Set post variables
        postData = {
                'data': data,
                'tokens': tokens
        }

        # Set URL to Send Notifications API endpoint
        req = urllib2.Request('https://api.pushy.me/push?api_key=' + apiKey)

        # Set Content-Type header since we're sending JSON
        req.add_header('Content-Type', 'application/json')

        # Actually send the push
        response = urllib2.urlopen(req, json.dumps(postData))