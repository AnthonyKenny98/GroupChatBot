"""Class for interfacing with GroupMe API."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 11:47:53
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-09 17:08:27

# '4a8cf510b7541a8a3c96eb17a5'


import random
import requests
import json

ACCESS_TOKEN = 'NCSnlZKP4kcnnkQXZd7SBql045OHQrOXYgHyYiim'
TEST_GROUP_ID = '55604032'


class GroupMe:
    """Class for interfacing with GroupMe API."""

    def __init__(self, access_token):
        """Initialize GroupMe Class Instance."""
        self.accessToken = access_token
        self.authString = '?token=' + self.accessToken
        self.baseURL = 'https://api.groupme.com/v3'
        self.headers = {'content-type': 'application/json'}

    def build_url(self, endpoint, **kwargs):
        """Return URL for given endpoint."""
        url_path = {
            'groups': '/groups',
            'messages': '/groups/' + kwargs.get('groupID', '') + '/messages',
            'bots': '/bots'
        }
        return self.baseURL + url_path[endpoint] + self.authString

    def get_groups(self, n=10):
        """Return JSON of groups."""
        url = self.build_url('groups')
        payload = {
            "per_page": n
        }
        return (requests.get(url, params=payload)).json()['response']

    def post_message(self, message):
        """Send message to Group."""
        url = self.build_url('messages', groupID=TEST_GROUP_ID)
        payload = json.dumps({
            "message": {
                "source_guid": str(random.randint(0, 10000)),
                "text": message
            }
        })
        return requests.post(url, headers=self.headers, data=payload)


class GroupMeBot:
    """Interface for GroupMe Bot."""

    def __init__(self, bot_id):
        """Initialize GroupMe Bot."""
        self.id = bot_id
        self.groupme = GroupMe(ACCESS_TOKEN)
        self.headers = self.groupme.headers

    def send_message(self, message):
        """Send message as bot."""
        url = self.groupme.baseURL + '/bots/post'
        payload = json.dumps({
            "bot_id": self.id,
            "text": message
        })
        return requests.post(url, headers=self.headers, data=payload)


def setup_bot(bot_name):
    """Set Up Bot in a particular GroupMe group chat. Return Bot ID."""
    groupme = GroupMe(ACCESS_TOKEN)

    # Get list of n groups
    groups = groupme.get_groups(20)

    # Seek user input on group for which bot should be created
    print("Select the group for which you would like to create this bot\n")
    for i in range(len(groups)):
        print(str(i) + ": " + groups[i]['name'])
    group_index = int(input("\nType Group Number: "))

    # Determine Group ID
    group_id = groups[group_index]['id']

    # Prepare payload to create bot
    payload = json.dumps({
        "bot": {
            "name": bot_name,
            "group_id": group_id,
            "callback_url": "https://example.com/bot_callback1"
        }
    })
    url = groupme.build_url('bots')

    # Make Post request
    bot = requests.post(url, headers=groupme.headers, data=payload)
    return bot.json()['response']['bot']['bot_id']
