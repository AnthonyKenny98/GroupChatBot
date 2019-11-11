"""Class for interfacing with GroupMe API."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-09 11:47:53
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 18:11:49

import os
import requests
import json
from ..chatbot import ChatBot

CREDENTIALS = ['access_token']


class GroupMeChatBot(ChatBot):
    """Master ChatBot Class for GroupMe."""

    @staticmethod
    def get_credentials():
        """Return dict of credentials from either secure or example folder.

        To change credentials update the CREDENTIALS constant at the top
        of this file.
        """
        # Get credentials filepath
        path = os.path.dirname(os.path.realpath(__file__))
        path += '/secure' if os.path.isdir(path + '/secure') else '/example'

        credentials = {}
        for credential in CREDENTIALS:
            with open(path + '/' + credential + '.credentials', 'r') as f:
                credentials[credential] = f.read()
        return credentials

    def __init__(self, data):
        """Initialize GroupMe Chat Bot Instance."""
        # Init GroupMeUser instance
        self.user = GroupMe(self.get_credentials()['access_token'])

        # Get correct bot for callback_data
        self.bot = GroupMeBot([
            b for b in self.user.get_bots()
            if b['group_id'] == data['group_id']
        ][0]['bot_id'])

        # Message that awoke the bot
        self.stimulus = {}
        self.stimulus.update({
            'data': data
        })

        super().__init__()

    def post_message(self, text):
        """Post message."""
        # UNCOMMENT FOR PRODUCTION
        # return self.bot.post_message(text)

        # PRINT FOR TESTING
        print(text)

    def api_pre_react_checks(self):
        """Go through API specific pre-react checks."""
        return self.stimulus['data']['sender_type'] != 'bot'


class GroupMe:
    """Class for interfacing with GroupMe API."""

    def __init__(self, access_token):
        """Initialize GroupMe Class Instance."""
        self.authString = '?token=' + access_token
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

    def get_groups(self):
        """Return JSON of groups."""
        return (requests.get(self.build_url('groups'))).json()['response']

    def get_bots(self):
        """Return list of bots."""
        return requests.get(self.build_url('bots')).json()['response']


class GroupMeBot:
    """Interface for GroupMe Bot."""

    def __init__(self, bot_id):
        """Initialize GroupMe Bot."""
        self.id = bot_id
        self.baseURL = 'https://api.groupme.com/v3/bots'
        self.headers = {'content-type': 'application/json'}

    def build_url(self, endpoint):
        """Return URL for given endpoint."""
        url_path = {
            'post': '/post'
        }
        return self.baseURL + url_path[endpoint]

    def post_message(self, text):
        """Send message as bot."""
        return requests.post(
            self.build_url('post'),
            headers=self.headers,
            data=json.dumps({
                "bot_id": self.id,
                "text": text
            })
        )


def setup_bot(callback_url):
    """Set Up Bot in a particular GroupMe group chat. Return Bot ID."""
    access_token = input("Please input your GroupMe Account Access Token: ")

    this_path = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(this_path + '/secure', exist_ok=True)
    with open(this_path + '/secure/access_token.credentials', 'w') as f:
        f.write(access_token)

    groupme = GroupMe(access_token)

    # Get list of groups
    groups = groupme.get_groups()

    bot_name = input("What would you like your bot to be named: ")

    # Seek user input on group for which bot should be created
    for i in range(len(groups)):
        print(str(i) + ": " + groups[i]['name'])
    group_index = int(input("\nInput Group Number For Bot: "))

    # Prepare payload to create bot
    payload = json.dumps({
        "bot": {
            "name": bot_name,
            "group_id": groups[group_index]['id'],
            "callback_url": callback_url
        }
    })
    url = groupme.build_url('bots')

    # Make Post request
    response = requests.post(url, headers=groupme.headers, data=payload)
    print('Success' if response.status_code == 201 else 'Failure')
