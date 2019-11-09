"""Class for interfacing with GroupMe API."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 11:47:53
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-09 15:05:57


import random
import requests
import json

ACCESS_TOKEN = 'NCSnlZKP4kcnnkQXZd7SBql045OHQrOXYgHyYiim'
TEST_GROUP_ID = '55604032'


class GroupMe:
    """Class for interfacing with GroupMe API."""

    def __init__(self):
        """Initialize GroupMe Class Instance."""
        self.accessToken = ACCESS_TOKEN
        self.authString = '?token=' + self.accessToken
        self.baseURL = 'https://api.groupme.com/v3'
        self.headers = {'content-type': 'application/json'}

    def get_url(self, endpoint, **kwargs):
        """Return URL for given endpoint."""
        url_path = {
            'send_message': '/groups' + '/' + kwargs['groupID'] + '/messages'
        }
        return self.baseURL + url_path[endpoint] + self.authString

    def send_message(self, message):
        """Send message to Group."""
        url = self.get_url('send_message', groupID=TEST_GROUP_ID)
        payload = json.dumps({
            "message": {
                "source_guid": str(random.randint(0, 10000)),
                "text": message
            }
        })
        return requests.post(url, headers=self.headers, data=payload)
