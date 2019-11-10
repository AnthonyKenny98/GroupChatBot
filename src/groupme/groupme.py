"""Class for interfacing with GroupMe API."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 11:47:53
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-09 19:01:47

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

    def get_bots(self):
        """Return list of bots."""
        url = self.build_url('bots')
        return requests.get(url).json()['response']

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
        self.baseURL = 'https://api.groupme.com/v3'
        self.headers = {'content-type': 'application/json'}

    def build_url(self, endpoint):
        """Return URL for given endpoint."""
        url_path = {
            'bots': '/bots',
            'post': '/bots/post'
        }
        return self.baseURL + url_path[endpoint]

    def post_message(self, message):
        """Send message as bot."""
        url = self.build_url('post')
        payload = json.dumps({
            "bot_id": self.id,
            "text": message
        })
        return requests.post(url, headers=self.headers, data=payload)


def setup_bot(callback_url):
    """Set Up Bot in a particular GroupMe group chat. Return Bot ID."""
    groupme = GroupMe(ACCESS_TOKEN)

    # Get list of n groups
    groups = groupme.get_groups(20)

    bot_name = input("What would you like your bot to be named: ")

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
            "callback_url": callback_url
        }
    })
    url = groupme.build_url('bots')

    # Make Post request
    bot = requests.post(url, headers=groupme.headers, data=payload)
    print(bot.text)
    return bot.json()  # ['response']['bot']['bot_id']
